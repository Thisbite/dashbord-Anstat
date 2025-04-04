from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text  # Importer text pour les requêtes SQL brutes
from dotenv import load_dotenv
import os
import pandas as pd

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Utiliser les variables d'environnement pour MySQL
host = os.getenv('MYSQL_HOST')
database = os.getenv('MYSQL_DATABASE')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')

# Configurer Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy et Migrate
db = SQLAlchemy()
db.init_app(app)  # Lier db à l'application Flask
migrate = Migrate(app, db)

# Fonction pour vider la table
def clear_v1_indicateur():
    with app.app_context():  # Contexte d'application requis pour db.session
        db.session.execute(text("DELETE FROM v1_indicateur"))  # Utiliser text()
        db.session.commit()
        print("La table v1_indicateur a été vidée avec succès.")

# Exécuter si le script est lancé directement

#-----------------------Insertion 
# Fonction pour insérer les données depuis un fichier Excel
def insert_from_excel(file_path):
    with app.app_context():
        # Lire toutes les feuilles du fichier Excel
        excel_data = pd.read_excel(file_path, sheet_name=None)
        
        # Parcourir chaque feuille (region, departement, sous_prefecture)
        for sheet_name, df in excel_data.items():
            print(f"Traitement de la feuille : {sheet_name}")
            
            # Renommer les colonnes pour correspondre à la table
            df = df.rename(columns={
                'Année': 'Annee',
                'Valeurs': 'Valeur'
            })
            
            # S'assurer que toutes les colonnes nécessaires sont présentes (sans Region)
            required_columns = ['Dimension', 'Modalites', 'Indicateurs', 'Annee', 'Valeur']
            df = df[required_columns]
            
            # Convertir le DataFrame en liste de dictionnaires pour l'insertion
            records = df.to_dict(orient='records')
            
            # Insérer les données dans la table V1_indicateur
            for record in records:
                db.session.execute(
                    text("""
                        INSERT INTO v1_indicateur (Dimension, Modalites, Indicateurs, Annee, Valeur)
                        VALUES (:Dimension, :Modalites, :Indicateurs, :Annee, :Valeur)
                    """),
                    record
                )
            db.session.commit()
            print(f"Données de la feuille '{sheet_name}' insérées avec succès.")
if __name__ == "__main__":
    clear_v1_indicateur()
    #excel_file = "data_v0.xlsx"
    #insert_from_excel(excel_file)