from app import create_app, db
from models import Annee, Indicateur, Modalite, Dimension, Donnee, DonneeModalite
import pandas as pd
import re

def generate_tableau_5(indicateur_nom, annee_val, row_dimensions, col_dimension):
    """
    Génère le Tableau 5 dynamiquement :
    - Lignes : Indicateur, Année, et modalités des row_dimensions
    - Colonnes : Modalités de col_dimension
    - Valeurs : valDonnees
    """
    app = create_app()
    with app.app_context():
        # Vérifier si les dimensions existent
        valid_dimensions = db.session.query(Dimension.nomDimension).all()
        valid_dimensions = [d[0] for d in valid_dimensions]
        requested_dimensions = row_dimensions + [col_dimension]
        missing_dims = [d for d in requested_dimensions if d not in valid_dimensions]
        if missing_dims:
            print(f"Dimensions introuvables dans la base : {missing_dims}")
            print(f"Dimensions disponibles : {valid_dimensions}")
            return None

        # Vérifier si l’indicateur existe
        if not db.session.query(Indicateur).filter_by(nomIndicateur=indicateur_nom).first():
            print(f"Indicateur introuvable : {indicateur_nom}")
            indicateurs = db.session.query(Indicateur.nomIndicateur).all()
            print(f"Indicateurs disponibles : {[i[0] for i in indicateurs]}")
            return None

        # Vérifier si l’année existe
        if not db.session.query(Annee).filter_by(valAnnees=annee_val).first():
            print(f"Année introuvable : {annee_val}")
            annees = db.session.query(Annee.valAnnees).all()
            print(f"Années disponibles : {[a[0] for a in annees]}")
            return None

        # Sous-requête pour trouver les idDonnees avec EXACTEMENT les dimensions demandées
        subquery = (
            db.session.query(DonneeModalite.f_idDonnees)
            .join(Modalite, DonneeModalite.f_idModalites == Modalite.idModalites)
            .join(Dimension, Modalite.f_idDimensions == Dimension.idDimensions)
            .filter(DonneeModalite.f_idDonnees == Donnee.idDonnees)
            .group_by(DonneeModalite.f_idDonnees)
            .having(
                db.func.count(Dimension.idDimensions.distinct()) == len(requested_dimensions)
            )
            .subquery()
        )

        # Requête principale
        result = (
            db.session.query(
                Indicateur.nomIndicateur,
                Annee.valAnnees,
                Modalite.nomModalites,
                Dimension.nomDimension,
                Donnee.valDonnees,
                Donnee.idDonnees
            )
            .join(Donnee, Donnee.f_idIndicateurs == Indicateur.idIndicateurs)
            .join(Annee, Donnee.f_idAnnees == Annee.idAnnees)
            .join(DonneeModalite, DonneeModalite.f_idDonnees == Donnee.idDonnees)
            .join(Modalite, DonneeModalite.f_idModalites == Modalite.idModalites)
            .join(Dimension, Modalite.f_idDimensions == Dimension.idDimensions)
            .filter(
                Indicateur.nomIndicateur == indicateur_nom,
                Annee.valAnnees == annee_val,
                Dimension.nomDimension.in_(requested_dimensions),
                Donnee.idDonnees.in_(subquery)  # Restreindre aux idDonnees valides
            )
            .all()
        )

        # Créer un DataFrame
        data = [
            {
                'indicateur': row.nomIndicateur,
                'annee': row.valAnnees,
                'modalite': row.nomModalites,
                'dimension': row.nomDimension,
                'valeur': row.valDonnees,
                'id_donnee': row.idDonnees
            } for row in result
        ]
        df = pd.DataFrame(data)

        if df.empty:
            print(f"Aucune donnée trouvée pour {indicateur_nom} en {annee_val} avec les dimensions {requested_dimensions}")
            for dim in requested_dimensions:
                modalites = db.session.query(Modalite.nomModalites).join(Dimension).filter(Dimension.nomDimension == dim).all()
                print(f"Modalités pour {dim} : {[m[0] for m in modalites]}")
            return None

        # Regrouper les modalités par id_donnee
        df_pivot = df.pivot_table(
            values='valeur',
            index=['indicateur', 'annee', 'id_donnee'],
            columns=['dimension', 'modalite'],
            aggfunc='sum'  # Sommer les valeurs pour éviter doublons
        ).reset_index()

        # Créer le tableau final
        df_final = pd.DataFrame()
        df_final['indicateur'] = df_pivot['indicateur']
        df_final['annee'] = df_pivot['annee']

        # Ajouter les colonnes pour les dimensions des lignes
        for dim in row_dimensions:
            modalites = df[df['dimension'] == dim]['modalite'].unique()
            col_name = re.sub(r'\s+', '_', dim.lower())  # Garder apostrophes, remplacer espaces
            df_final[col_name] = None
            for modalite in modalites:
                if (dim, modalite) in df_pivot.columns:
                    df_final.loc[df_pivot[(dim, modalite)].notnull(), col_name] = modalite

        # Ajouter les colonnes pour la dimension des colonnes
        modalites_col = df[df['dimension'] == col_dimension]['modalite'].unique()
        for modalite in modalites_col:
            if (col_dimension, modalite) in df_pivot.columns:
                df_final[modalite] = df_pivot[(col_dimension, modalite)]

        # Nettoyer les lignes incomplètes
        row_cols = [re.sub(r'\s+', '_', dim.lower()) for dim in row_dimensions]
        df_final = df_final.dropna(subset=row_cols)

        # Réorganiser les colonnes
        final_columns = ['indicateur', 'annee'] + row_cols + list(modalites_col)
        df_final = df_final[final_columns]

        return df_final

if __name__ == "__main__":
    # Exemple d’utilisation
    tableau_5 = generate_tableau_5(
        indicateur_nom="Effectif de la population",
        annee_val=2000,
        row_dimensions=["Sexe","Groupe d'âges"],
        col_dimension="Région"
    )
    if tableau_5 is not None:
        print(tableau_5)
        tableau_5.to_csv("tableau_R.csv", index=False, encoding='utf-8')