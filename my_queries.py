import pandas as pd
from dotenv import load_dotenv
import os
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from elasticsearch import Elasticsearch
from models import db, Region, IndicateurV2, V1Indicateur, Indicateur, DirectionStatistique  # Importer les modèles

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Region, Indicateur, V1Indicateur  # Importez vos modèles SQLAlchemy ici
import config as cf
from dotenv import load_dotenv
load_dotenv()

# Utiliser les variables d'environnement pour MySQL
host = os.getenv('MYSQL_HOST')
database = os.getenv('MYSQL_DATABASE')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
# Création de la session SQLAlchemy
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}/{database}"
)
Session = sessionmaker(bind=engine)
session = Session()

# Récupérer les régions sous forme de liste
def options_regions():
    try:
        # Récupérer les noms des régions avec SQLAlchemy
        regions = session.query(Region.nom_region).order_by(Region.nom_region.asc()).all()
        return [region[0] for region in regions]  # Liste des régions
    except Exception as e:
        print(f"Erreur lors de la récupération des régions : {e}")
        return []

# Récupérer les indicateurs sous forme de liste triée
def options_indicateur():
    try:
        # Récupérer les indicateurs avec SQLAlchemy
        indicateurs = session.query(Indicateur.indicateur).all()
        return sorted([indicateur[0] for indicateur in indicateurs])  # Liste triée
    except Exception as e:
        print(f"Erreur lors de la récupération des indicateurs : {e}")
        return []

from sqlalchemy import func
from models import IndicateurV2, db  # Importer le modèle et db depuis models.py

# Obtenir la définition d'un indicateur choisi
def definition_indicateur(indicateur_choisi):
    try:
        # Requête pour récupérer la définition de l'indicateur
        result = db.session.query(IndicateurV2.definitions).filter(
            func.lower(IndicateurV2.indicateur) == indicateur_choisi.lower()
        ).first()
        
        if result and result[0]:  # Vérifie si le résultat existe et n'est pas None
            return result[0]  # Retourne la définition
        else:
            return f"Définition pour l'indicateur '{indicateur_choisi}' non trouvée."
    except Exception as e:
        print(f"Erreur lors de la récupération de la définition : {e}")
        return None

# Obtenir le mode de calcul d'un indicateur choisi
def mode_calcul_indicateur(indicateur_choisi):
    try:
        # Requête pour récupérer le mode de calcul de l'indicateur
        result = db.session.query(IndicateurV2.mode_calcul).filter(
            func.lower(IndicateurV2.indicateur) == indicateur_choisi.lower()
        ).first()
        
        if result and result[0]:  # Vérifie si le résultat existe et n'est pas None
            return result[0]  # Retourne le mode de calcul
        else:
            return f"Mode de calcul pour l'indicateur '{indicateur_choisi}' non trouvé."
    except Exception as e:
        print(f"Erreur lors de la récupération du mode de calcul : {e}")
        return None

# Charger des données depuis un fichier CSV
def get_data(filepath):
    try:
        df = pd.read_csv(filepath, sep=',')
        return df
    except Exception as e:
        print(f"Erreur lors du chargement du fichier CSV : {e}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

# Récupérer des données depuis MySQL pour V1_indicateur
def get_data_from_mysql_V1():
    try:
        # Requête pour récupérer les données depuis V1_indicateur
        query = session.query(V1Indicateur.Dimension, V1Indicateur.Modalites, V1Indicateur.Indicateurs, V1Indicateur.Annee, V1Indicateur.Valeur)
        df = pd.read_sql(query.statement, engine)
        return df
    except Exception as e:
        print(f"Erreur lors de la récupération des données MySQL : {e}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

# Récupérer des données depuis MySQL pour une région spécifique
def get_data_from_mysql_VR(region_name):
    try:
        # Requête pour récupérer les données filtrées par région
        query = session.query(V1Indicateur.Dimension, V1Indicateur.Modalites, V1Indicateur.Indicateurs, V1Indicateur.Annee, V1Indicateur.Valeur).filter(V1Indicateur.Region == region_name)
        df = pd.read_sql(query.statement, engine)
        return df
    except Exception as e:
        print(f"Erreur lors de la récupération des données pour la région {region_name}: {e}")
        return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

# Insérer des données depuis un fichier Excel dans la base de données
def insert_data_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        df.columns = ['Dimension', 'Modalites', 'Indicateurs', 'Année', 'Valeur']
        
        # Insertion dans la base de données
        for _, row in df.iterrows():
            data = V1Indicateur(
                Dimension=row['Dimension'],
                Modalites=row['Modalites'],
                Indicateurs=row['Indicateurs'],
                Annee=row['Année'],
                Valeur=row['Valeur']
            )
            session.add(data)
        
        session.commit()  # Valider les changements
        print("Données insérées avec succès dans la table V1_indicateur.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")
        session.rollback()  # Annuler la transaction en cas d'erreur
    finally:
        session.close()  # Fermer la session
        
        

#Importer le fichier  excel _______________________________Excel
def index_data_from_excel():
    # Lire le fichier Excel
    data = pd.read_excel('lexique.xlsx')
    # Vérifie si les données sont récupérées correctement
    if data.empty:
        print("Aucune donnée récupérée du fichier Excel.")
    else:
        print(f"{len(data)} lignes récupérées depuis Excel.")
    # Nettoyer les données (remplacer les NaN par des chaînes vides)
    data = data.fillna('')
    # Convertir toutes les valeurs en minuscules
    data = data.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    # Indexer chaque ligne du fichier Excel
    for _, row in data.iterrows():
        document = row.to_dict()  # Convertir la ligne en dictionnaire
        print("Document à indexer:", document)  # Debug: affiche le document
        # Essayer d'indexer le document
        try:
            es.index(index=index_name, body=document)
            print(f"Indexing: {document}")
        except Exception as e:
            print(f"Erreur d'indexation pour le document {document}: {e}")
    print("Données indexées avec succès.")
    
    
import random
def generate_region_data():
    age_data = {
        "male": [random.randint(-200, -50) for _ in range(5)],
        "female": [random.randint(50, 220) for _ in range(5)],
        "ages": ['0-4', '5-9', '10-14', '15-19', '20-24']
    }
    
    production_data = {
        "years": [2010, 2012, 2014, 2016, 2018],
        "production": [random.randint(300, 900) for _ in range(5)]
    }
    
    indicateurs = {
        "ind1": random.randint(20, 60),
        "ind2": random.randint(40, 80),
        "ind3": random.randint(10, 40)
    }
    
    return {
        "age_data": age_data,
        "production_data": production_data,
        "indicateurs": indicateurs
    }
