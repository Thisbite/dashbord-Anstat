from dotenv import load_dotenv
import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from elasticsearch import Elasticsearch
from models import db, Region, IndicateurV2, V1Indicateur, Indicateur, DirectionStatistique  # Importer les modèles

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Utiliser les variables d'environnement pour MySQL
host = os.getenv('MYSQL_HOST')
database = os.getenv('MYSQL_DATABASE')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')

# Configurer Elasticsearch avec le schéma 'http'
es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
es_port = int(os.getenv('ELASTICSEARCH_PORT', '9200'))  # Conversion explicite en entier
es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])

# Vérifier la connexion à Elasticsearch
if es.ping():
    print("Connexion à Elasticsearch réussie")
else:
    print("Erreur lors de la connexion à Elasticsearch")

# Configurer Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser SQLAlchemy et Migrate
db.init_app(app)  # Initialisation liée à l'application Flask
migrate = Migrate(app, db)

# Supprimer les fonctions de connexion manuelle à MySQL (inutile avec SQLAlchemy)
# Plus besoin de create_connection(), get_db(), close_db(), teardown_db()

# Exemple de fonction pour récupérer des données avec SQLAlchemy
def get_v1_indicateur_data():
    """Récupérer les données de la table V1_indicateur avec SQLAlchemy"""
    with app.app_context():  # Nécessaire pour utiliser db.session dans un contexte Flask
        try:
            # Utiliser une session SQLAlchemy pour interroger la table
            result = db.session.query(V1Indicateur).all()
            # Convertir les résultats en DataFrame pandas
            data = [{
                'Dimension': row.Dimension,
                'Modalites': row.Modalites,
                'Indicateurs': row.Indicateurs,
                'Annee': row.Annee,
                'Valeur': float(row.Valeur) if row.Valeur is not None else None,
                'Region': row.Region
            } for row in result]
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None

# Exemple de fonction pour récupérer les régions
import pandas as pd

def get_regions():
    """Récupérer les noms des régions avec SQLAlchemy et les retourner sous forme de DataFrame"""
    with app.app_context():
        try:
            # Récupérer les résultats de la requête
            result = db.session.query(Region.nom_region).order_by(Region.nom_region.asc()).all()
            
            # Transformer les résultats en DataFrame
            regions = pd.DataFrame(result, columns=['nom_region'])
            
            return regions  # Retourner le DataFrame
        except Exception as e:
            print(f"Erreur lors de la récupération des régions : {e}")
            return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur


# Fonction pour nettoyer les données et créer le tableau croisé dynamique
def clean_create_pivot_table(df, row_dimensions, col_dimensions, Valeurs, Annee, row_label="-", col_label=""):
    df_final = pd.DataFrame()  # Initialiser un DataFrame final pour stocker les données nettoyées
    for i, row in df.iterrows():
        dimension_cols = row['Dimension'].split('/')
        category_values = row['Modalites'].split('/')
        dimension_cols = [col.strip() for col in dimension_cols]
        category_values = [value.strip() for value in category_values]
        dimension_dict = dict(zip(dimension_cols, category_values))
        temp_row = pd.Series(dimension_dict)
        temp_row['Indicateurs'] = row['Indicateurs']
        temp_row[Valeurs] = row[Valeurs]
        temp_row[Annee] = row[Annee]
        df_final = pd.concat([df_final, temp_row.to_frame().T], ignore_index=True)
    
    df_final.fillna('-', inplace=True)

    tableau_croise = pd.pivot_table(
        df_final,
        fill_value='-',
        values=Valeurs,
        index=row_dimensions,
        columns=[Annee] + col_dimensions,
        aggfunc='sum'
    )
    
    tableau_croise = tableau_croise.reset_index()
    tableau_croise.index.names = [row_label if i > 0 else None for i in range(len(tableau_croise.index.names))]
    tableau_croise.columns.names = [col_label if i > 0 else None for i in range(len(tableau_croise.columns.names))]
    
    tableau_croise_columns = tableau_croise.columns
    if isinstance(tableau_croise.columns, pd.MultiIndex):
        l = len(row_dimensions)
        nouvelle_colonne = [(' ',) * tableau_croise.columns.nlevels] * l + list(tableau_croise.columns[l:])
        tableau_croise_columns = pd.MultiIndex.from_tuples(nouvelle_colonne, names=tableau_croise.columns.names)
    elif isinstance(tableau_croise.columns, pd.Index):
        nouvelle_colonne = [' '] + list(tableau_croise.columns[1:])
        tableau_croise_columns = nouvelle_colonne

    tableau_croise.columns = tableau_croise_columns
    tableau_croise = tableau_croise.astype('object').fillna('-')
    tableau_croise = tableau_croise.applymap(str)

    return tableau_croise

# Fonction simplifiée pour le tableau croisé dynamique
def pivot_table_2(df, row_dimensions, col_dimensions, Valeurs, Annee, row_label="-", col_label=""):
    df_final = pd.DataFrame()
    for i, row in df.iterrows():
        dimension_cols = row['Dimension'].split('/')
        category_values = row['Modalites'].split('/')
        dimension_cols = [col.strip() for col in dimension_cols]
        category_values = [value.strip() for value in category_values]
        dimension_dict = dict(zip(dimension_cols, category_values))
        temp_row = pd.Series(dimension_dict)
        temp_row['Indicateurs'] = row['Indicateurs']
        temp_row[Valeurs] = row[Valeurs]
        temp_row[Annee] = row[Annee]
        df_final = pd.concat([df_final, temp_row.to_frame().T], ignore_index=True)
    
    df_final.fillna('-', inplace=True)
    tableau_croise = pd.pivot_table(
        df_final,
        fill_value='-',
        values=Valeurs,
        index=row_dimensions,
        columns=[Annee] + col_dimensions,
        aggfunc='sum'
    )
    return tableau_croise

