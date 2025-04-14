from app import create_app, db
from models import Annee,Indicateur, Modalite, Dimension, Donnee, DonneeModalite  # Changé Annees en Annee, Donnees en Donnee
import pandas as pd

def get_id_from_table(model, id_field, **kwargs):
    """Fonction générique pour récupérer l'ID d'une ligne via SQLAlchemy"""
    result = db.session.query(model).filter_by(**kwargs).first()
    return getattr(result, id_field) if result else None

def insert_from_excel(file_path):
    app = create_app()
    erreurs = []  # Liste pour stocker les erreurs

    with app.app_context():
        excel_data = pd.read_excel(file_path, sheet_name=None)

        for sheet_name, df in excel_data.items():
            print(f"Traitement de la feuille : {sheet_name}")
            for index, row in df.iterrows():
                try:
                    # Vérifier que les colonnes nécessaires existent
                    required_columns = ["Dimension", "Modalites", "Indicateur", "Année", "Valeur"]
                    if not all(col in df.columns for col in required_columns):
                        raise ValueError(f"Colonnes manquantes dans la feuille {sheet_name}")

                    dimensions = row["Dimension"].split(",")
                    modalites = row["Modalites"].split("/")
                    indicateur_nom = row["Indicateur"]
                    annee_val = int(row["Année"])
                    valeur = float(row["Valeur"])

                    # Vérifier ou créer l'année
                    annee_id = get_id_from_table(Annee, "idAnnees", valAnnees=annee_val)  # Changé Annees en Annee
                    if not annee_id:
                        annee = Annee(idAnnees=f"AN{annee_val}", valAnnees=annee_val)  # Changé Annees en Annee
                        db.session.add(annee)
                        db.session.commit()
                        annee_id = annee.idAnnees

                    # Vérifier ou créer l'indicateur
                    indicateur_id = get_id_from_table(Indicateur, "idIndicateurs", nomIndicateur=indicateur_nom)
                    if not indicateur_id:
                        raise ValueError(f"Indicateur introuvable : {indicateur_nom}. Veuillez l'ajouter manuellement.")

                    # Insérer la donnée
                    donnee = Donnee(  # Changé Donnees en Donnee
                        f_idAnnees=annee_id,
                        f_idIndicateurs=indicateur_id,
                        valDonnees=valeur
                    )
                    db.session.add(donnee)
                    db.session.commit()
                    donnee_id = donnee.idDonnees

                    # Insérer les relations DonneeModalite
                    for i in range(len(modalites)):
                        nom_dim = dimensions[i].strip()
                        nom_mod = modalites[i].strip()

                        # Vérifier ou créer la dimension
                        dimension_id = get_id_from_table(Dimension, "idDimensions", nomDimension=nom_dim)
                        if not dimension_id:
                            dimension = Dimension(idDimensions=f"DIM{index}{i}", nomDimension=nom_dim)
                            db.session.add(dimension)
                            db.session.commit()
                            dimension_id = dimension.idDimensions

                        # Vérifier ou créer la modalité
                        modalite_id = get_id_from_table(Modalite, "idModalites", nomModalites=nom_mod, f_idDimensions=dimension_id)
                        if not modalite_id:
                            modalite = Modalite(idModalites=f"MOD{index}{i}", f_idDimensions=dimension_id, nomModalites=nom_mod)
                            db.session.add(modalite)
                            db.session.commit()
                            modalite_id = modalite.idModalites

                        # Créer la relation DonneeModalite
                        relation = DonneeModalite(f_idDonnees=donnee_id, f_idModalites=modalite_id)
                        db.session.add(relation)

                    db.session.commit()

                except Exception as e:
                    ligne_txt = f"[Feuille: {sheet_name} | Ligne: {index+2}] ERREUR: {str(e)} | Données: {row.to_dict()}\n"
                    erreurs.append(ligne_txt)
                    db.session.rollback()

        # Écrire les erreurs dans un fichier texte
        if erreurs:
            with open("erreurs_insertion.txt", "w", encoding="utf-8") as f:
                f.writelines(erreurs)
            print(f"{len(erreurs)} ligne(s) non insérée(s). Voir erreurs_insertion.txt")
        else:
            print("Toutes les lignes ont été insérées avec succès.")

if __name__ == "__main__":
    excel_file = "V1_indicateurs.xlsx"
    insert_from_excel(excel_file)