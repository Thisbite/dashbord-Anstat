from dotenv import load_dotenv
import os
import pandas as pd
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine, MetaData, Table, delete, or_, Float
from sqlalchemy.orm import sessionmaker
from elasticsearch import Elasticsearch
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
# Utiliser les variables d'environnement pour MySQL
host = os.getenv('MYSQL_HOST')
database = os.getenv('MYSQL_DATABASE')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')

# Configurer Elasticsearch avec le schéma 'http'
# Ajoute le schéma 'http' dans la configuration du nœud Elasticsearch
es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
es_port = int(os.getenv('ELASTICSEARCH_PORT', '9200'))  # Conversion explicite en entier


# Ajouter le schéma 'http' dans la configuration du nœud Elasticsearch
es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])

# Vérifier la connexion à Elasticsearch
if es.ping():
    print("Connexion à Elasticsearch réussie")
else:
    print("Erreur lors de la connexion à Elasticsearch")

def create_connection():
    """Créer une connexion à MySQL"""
    try:
        conn = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        if conn.is_connected():
            print("Connexion à la base de données MySQL réussie")
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")
        return None

def get_db():
    """Obtenir la connexion à la base de données pour la requête courante"""
    if 'db' not in g:
        g.db = create_connection()
    return g.db

def close_db(e=None):
    """Fermer la connexion à la base de données à la fin de la requête"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Configurer Flask et SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données et la migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Nettoyer les connexions MySQL après chaque requête
@app.teardown_appcontext
def teardown_db(exception):
    close_db()


# Fonction pour nettoyer les données et créer le tableau croisé dynamique sans afficher les noms de variables en lignes et colonnes
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
        # Ajouter cette ligne nettoyée au DataFrame final
        df_final = pd.concat([df_final, temp_row.to_frame().T], ignore_index=True)
    
    # Remplir les valeurs manquantes pour garder la structure propre
    df_final.fillna('-', inplace=True)

    # Créer le tableau croisé dynamique avec plusieurs niveaux de dimensions
    tableau_croise = pd.pivot_table(
        df_final,
        fill_value='-',
        values=Valeurs,
        index=row_dimensions,
        columns=[Annee] + col_dimensions,  # Ajouter l'année aux colonnes
        aggfunc='sum'
    )
    
    # Réinitialiser les index pour transformer les dimensions en colonnes et masquer les noms de variables
    tableau_croise = tableau_croise.reset_index()
    # Renommer les niveaux de colonnes
    tableau_croise.index.names = [row_label if i > 0 else None for i in range(len(tableau_croise.index.names))]
    
    tableau_croise.columns.names = [col_label if i > 0 else None for i in range(len(tableau_croise.columns.names))]
    
    # Supposons que tableau_croise.columns soit défini comme suit :
    tableau_croise_columns = tableau_croise.columns

    # Vérifier si `tableau_croise_columns` est un MultiIndex
    # Vérifier si `tableau_croise_columns` est un MultiIndex
    if isinstance(tableau_croise.columns, pd.MultiIndex):
        # Calculer la longueur de `row_dimensions`
        l = len(row_dimensions)
        # Créer dynamiquement une liste de tuples vides de longueur `l`
        nouvelle_colonne = [(' ',) * tableau_croise.columns.nlevels] * l + list(tableau_croise.columns[l:])
        print('longueur l:', l)
        # Affecter les nouvelles colonnes au DataFrame
        tableau_croise_columns = pd.MultiIndex.from_tuples(nouvelle_colonne, names=tableau_croise.columns.names)

    elif isinstance(tableau_croise.columns, pd.Index):
        nouvelle_colonne = [' '] + list(tableau_croise.columns[1:])
        tableau_croise_columns = nouvelle_colonne

    tableau_croise.columns = tableau_croise_columns

    # Convertir en 'object', remplir les NaN par '-' et finaliser le type d'objet
    tableau_croise = tableau_croise.astype('object').fillna('-')

    # Assurer que toutes les cellules sont des chaînes de caractères pour éviter les futurs avertissements
    tableau_croise = tableau_croise.applymap(str)

    return tableau_croise







#Pour traitement de données
def wrangle(path):
    df=pd.read_excel(path)
    # Supprimer les espaces autour des barres obliques dans la colonne 'Dimension'
    df['Dimension'] = df['Dimension'].str.replace(r'\s*/\s*', '/', regex=True)
    df['Dimension'] = df['Dimension'].apply(lambda x: '/'.join(sorted(x.split('/'))))
    return df


# Fonction pour charger et traiter les données depuis un fichier Excel
def load_excel_data(file_path):
    df = pd.read_excel(file_path)
    indicateurs_data = {}

    for _, row in df.iterrows():
        # Séparer les modalités et les dimensions en supposant qu'elles sont séparées par '/'
        dim_parts = row['Modalites'].split('/')
        dimensions = row['Dimension'].split('/')
        value = row['Valeurs']
        
        for dim, mod in zip(dimensions, dim_parts):
            dim = dim.strip()  # Enlever les espaces autour de la dimension
            mod = mod.strip()  # Enlever les espaces autour de la modalité
            
            # Créer l'entrée pour la dimension si elle n'existe pas
            if dim not in indicateurs_data:
                indicateurs_data[dim] = []
            
            # Ajouter la modalité uniquement si elle n'existe pas déjà pour cette dimension
            if not any(entry['nom'] == mod for entry in indicateurs_data[dim]):
                indicateurs_data[dim].append({'nom': mod, 'valeur': value})
    
    return indicateurs_data






# Fonction pour nettoyer les données et créer le tableau croisé dynamique sans afficher les noms de variables en lignes et colonnes
def pivot_table_2(df, row_dimensions, col_dimensions, Valeurs, Annee, row_label="-", col_label=""):
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
        # Ajouter cette ligne nettoyée au DataFrame final
        df_final = pd.concat([df_final, temp_row.to_frame().T], ignore_index=True)
    
    # Remplir les valeurs manquantes pour garder la structure propre
    df_final.fillna('-', inplace=True)

    # Créer le tableau croisé dynamique avec plusieurs niveaux de dimensions
    tableau_croise = pd.pivot_table(
        df_final,
        fill_value='-',
        values=Valeurs,
        index=row_dimensions,
        columns=[Annee] + col_dimensions,  # Ajouter l'année aux colonnes
        aggfunc='sum'
    )
    
    return tableau_croise