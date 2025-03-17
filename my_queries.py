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

# Obtenir la définition d'un indicateur choisi
def definition_indicateur(indicateur_choisi):
    try:
        # Requête pour récupérer la définition de l'indicateur
        result = session.query(Indicateur.definitions).filter(func.lower(Indicateur.indicateur) == indicateur_choisi.lower()).first()
        if result:
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
        result = session.query(Indicateur.mode_calcul).filter(func.lower(Indicateur.indicateur) == indicateur_choisi.lower()).first()
        if result:
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
