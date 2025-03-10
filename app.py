from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
import os
import logging
import pandas as pd
import random
import time
import json
import urllib
from io import StringIO
from datetime import datetime
from unidecode import unidecode
import folium
import branca.colormap as cm 
import mysql.connector
import redis
from itertools import chain
import my_queries as qr
import data as dt
import config as cf
import io
global region_publication
region_publication="PORO"# Cette variable va nous permettre 
print(" Région détectée par défaut",region_publication )
#https://colab.research.google.com/drive/1oBqwcSMb4YTrn0NFUiQzJCiZ65uIay_S?hl=fr#scrollTo=CJAQGVAWNNPw
#brew services restart elastic/tap/elasticsearch-full
#redis-server
# -*- coding: utf-8 -*-
app = Flask(__name__)
# Configuration du logger pour le débogage
logging.basicConfig(level=logging.DEBUG)
# Configuration de la clé secrète pour les sessions Flask
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379)

Session(app)
app.secret_key = 'podmqjx128979po098RnhTRDX(7809908765bT'

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', '')}@"
    f"{os.getenv('MYSQL_HOST', 'localhost')}/{os.getenv('MYSQL_DATABASE', 'mydatabase')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données et de la migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#import de elastic
es=cf.es
#Mapper les colonnes  pour les recherches des indicateurs
index_name = 'requete_elastic'
mapping = {
    "mappings": {
        "properties": {
            "Sous_domaine": {"type": "text"},
            "indicateur": {"type": "text"},
            "Mode_de_collecte": {"type": "text"},
            "Mode_de_calcul": {"type": "text"},
            "Definition": {"type": "text"},
            "mot_cles":{"type":"text"}
        }
    }
}
# Supprimer l'index s'il existe
"""
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"L'index '{index_name}' a été supprimé.")
"""    
    
# Vérifier si l'index n'existe pas, puis le créer
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print(f"L'index '{index_name}' a été créé.")
else:
    print(f"L'index '{index_name}' existe déjà.")


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
    
    



@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query') or request.args.get('query')  # Récupère 'query' de POST ou GET
    page = int(request.args.get('page', 1))  # Récupère le numéro de page à partir des arguments de l'URL
    
    if query:
        query = unidecode(query)  # Ne s'exécute que si query n'est pas None
        
        # Prépare la requête de recherche pour chercher des termes correspondants ou des préfixes dans 'definitions'
        body = {
            "from": (page - 1) * 10,  # Définit l'offset pour la pagination (10 résultats par page)
            "size": 10,  # Limite le nombre de résultats par page à 10
            "query": {
                "bool": {
                    "should": [
                        {
                            "wildcard": {
                                "mot_cles": {
                                    "value": f"{query.lower()}*",
                                    "case_insensitive": True
                                }
                            }
                        },
                        {
                            "match": {
                                "mot_cles": {
                                    "query": query.lower(),
                                    "fuzziness": "AUTO",
                                    "prefix_length": 2
                                }
                            }
                        }
                    ]
                }
            }
        }
        # Effectue la recherche
        search_result = es.search(index=index_name, body=body)
        hits = search_result['hits']['hits']
        # Utilisation d'un set pour éviter les doublons
        unique_results = []
        seen = set()
        for hit in hits:
            unique_key = (
                hit['_source']['indicateur'], 
                #hit['_source']['annee']
            )
            if unique_key not in seen:
                unique_results.append(hit)
                seen.add(unique_key)
        total_results = search_result['hits']['total']['value']  # Récupère le nombre total de résultats
        total_pages = (total_results + 9) // 10  # Calcul du nombre total de pages
        return render_template('resultats.html', results=unique_results, query=query, page=page, total_pages=total_pages)
    
#index_data_from_excel()
es.indices.put_settings(index='requete_elastic', body={
    "index.blocks.read_only_allow_delete": None
})
#index_data_from_excel()

 
"""
 Présentation de la population par minute 
"""
START_DATE = datetime(2022, 1, 1)
STORAGE_FILE = 'births_data.json'

def get_births_per_minute():
    moyenne_naissance =777556/525600  # naissances par seconde, c'est la pop 2024 avec 2025 et on fait un ratio par minute sur toute l'année
    variation = random.uniform(-0.034, 0.034)
    return int(moyenne_naissance + variation )  # Convertir en naissances par minute

# Fonction pour charger l'état actuel du compteur
def load_birth_data():
    # Fonction pour calculer les naissances par minute avec variation
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            data = json.load(f)
            return data
    return {'total_births':30153004, 'last_time': START_DATE.timestamp()}

# Fonction pour sauvegarder l'état actuel du compteur
def save_birth_data(total_births, last_time):
    data = {'total_births': total_births, 'last_time': last_time}
    with open(STORAGE_FILE, 'w') as f:
        json.dump(data, f)

# Fonction pour calculer les naissances accumulées depuis une date de départ
def calculate_accumulated_births():
    birth_data = load_birth_data()
    last_time = birth_data['last_time']
    total_births = birth_data['total_births']
    # Temps écoulé depuis la date de départ ou la dernière mise à jour (en secondes)
    current_time = time.time()
    elapsed_time = current_time - last_time
    # Calculer les naissances accumulées pendant ce temps
    births_per_minute = get_births_per_minute()
    accumulated_births = (births_per_minute / 60) * elapsed_time  # Convertir en naissances par seconde
    # Mettre à jour le total des naissances
    total_births += accumulated_births
    # Sauvegarder le nouvel état
    save_birth_data(total_births, current_time)
    return total_births

@app.route('/births_data')
def births_data():
    # Calculer les naissances accumulées
    total_births = calculate_accumulated_births()
    # Obtenir la date et l'heure actuelles
    now = datetime.now()
    # Extraire le jour, le mois et l'année
    day = now.day
    month = now.month
    year = now.year

    # Renvoie les données en JSON pour le frontend
    data = {
        'time': time.time(),
        'total_births': round(total_births, 0),  # Afficher comme un entier
        'births_per_minute': get_births_per_minute(),  # Renvoyer les naissances par minute
        'day': day,
        'month': month,
        'year': year
    }
    return jsonify(data)



#---------------------------------------------------Home page pour accueil
from datetime import datetime

def days_in_year(year):
    # Vérifier si l'année est bissextile
    is_leap_year = lambda year: year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    return 366 if is_leap_year(year) else 365

def minutes_in_year(year):
    # Vérifier si l'année est bissextile
    is_leap_year = lambda year: year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days_in_year = 366 if is_leap_year(year) else 365
    minutes_in_year = days_in_year * 24 * 60  # 24 heures × 60 minutes = 1 440 minutes par jour
    return minutes_in_year

def naissance_deces_pop():
    data_nais_deces_pop = {
        "population":[777556,797114,793064,787604,804768,796472],
        "population_add":[31719274,32496830,33293944 ,34087008, 34874612 ,35679380],
        "naissance": [1025716, 1047630, 1045355, 1041416, 1061168, 1054794],
        "deces": [248159, 250517, 252290, 253814, 256397, 258324],
        "year": [2025 + i for i in range(6)]  # Correction range(6)
    }

    # Récupérer l'année actuelle
    current_year = datetime.now().year
    

    # Vérifier si l'année est dans les données
    if current_year in data_nais_deces_pop["year"]:
        index = data_nais_deces_pop["year"].index(current_year)
        date_ref=datetime(current_year,1,1)
        date_ref_M= datetime(current_year, 1, 1, 0, 0, 0) 
        date_actu=datetime.now()
        nbre_jour=date_actu-date_ref
        nbre_jour=nbre_jour.days
        naissance_annuelle = data_nais_deces_pop["naissance"][index]
        deces_annuel = data_nais_deces_pop["deces"][index]
        population_annuelle=data_nais_deces_pop["population"][index]
        day_now=datetime
        # Minute de l'année
        minute=minutes_in_year(current_year)
        difference=date_actu-date_ref_M
        dif_total_minute=difference.total_seconds() / 60
        # Calcul du taux journalier
        days = days_in_year(current_year)
        naissance_journalier = int(naissance_annuelle / days)*nbre_jour
        deces_journalier =int( deces_annuel / days)*nbre_jour
        pop_minute=int(population_annuelle/ minute)*int(dif_total_minute)+data_nais_deces_pop["population_add"][index]

        return naissance_journalier, deces_journalier,pop_minute
    else:
        return "Données non disponibles pour l'année", current_year

# Exemple d'utilisation
print('Extrapolation naissance',naissance_deces_pop())

    
@app.route('/')
def list_regions():
    regions = qr.options_regions()
    naissance,deces,pop_minute=naissance_deces_pop()
    # Données
    years = [2019, 2020, 2021, 2022, 2023]
    population = [24.0, 27.0, 27.4, 29.8, 30.38]
    school_enrollment_rate = [75, 76, 78, 79, 80]
    age_groups = ['0-14 ans', '15-24 ans', '25-54 ans', '55 - 59 ans','60 -64 ','65-69','70-74 ans']
    age_distribution = [40, 20, 30, 10, 18, 20]
    liste_region=regions
    print(liste_region)
    return render_template('home.html',
                           naissance=naissance,
                           deces=deces,
                           pop_minute=pop_minute,
                           years=years,
                           population=population,
                           school_enrollment_rate=school_enrollment_rate,
                           age_groups=age_groups,
                           age_distribution=age_distribution,
                           regions=regions,
                           )




#Bloc du dashbord------------------------------------------Pour le tableau de bord par région




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
regions = qr.options_regions()
# Générer les données pour toutes les régions restantes
data = {region: generate_region_data() for region in regions}

# Afficher les premières données générées
#import json
#print(json.dumps(data, indent=4))

regions = list(data.keys())  
import plotly.graph_objs as go
@app.route('/region_vitrine/<region>')  
def region_vitrine(region):  
    if region not in regions:  
        return "Region not found", 404  # Handle invalid region  
    region_data = data[region]
    global region_publication
    region_publication=region
    print("Nouvelle région détectée",region_publication )
    return render_template('region_vitrine.html',  
                           indicateurs=region_data['indicateurs'],  
                           region_name=region_publication,  
                           all_regions=regions) 

print('la region issue des fonctions',region_publication)
#--------------------------------------------------Fin du tableau de bord

# Load Excel data (assuming the Excel file is named 'publications.xlsx' in a 'data' folder)


def load_publications():
    try:
        df = pd.read_excel('static/data/publications2.xlsx')  # Chemin vers le fichier Excel
        print("DataFrame chargé avec succès :")
        print(df)  # Affiche le contenu du DataFrame pour vérification

        # Convertit le DataFrame en dictionnaire avec des clés uniques basées sur le titre normalisé
        publications = {}
        for _, row in df.iterrows():
            # Normalise le titre pour la clé (minuscules, underscores)
            title_key = row['nom de la publication'].lower().replace(' ', '_')
            # Crée un dictionnaire pour chaque publication
            publications[title_key] = {
                'title': row['nom de la publication'],
                'region': row['Région'],
                'date': row['Date d\'édition'],
                'description': row['Description de la publication'],
                'year': row['Annee de publication']
            }
        return publications
    except FileNotFoundError:
        print("Erreur : Le fichier publications2.xlsx n'a pas été trouvé dans /static/data/")
        return {}  # Retourne un dictionnaire vide si le fichier n'est pas trouvé
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return {}  # Retourne un dictionnaire vide en cas d'erreur

# Cache les données des publications
publications_data = load_publications()

EXCEL_FILE='static/data/publications2.xlsx'
@app.route('/publications')
def publications_region():
    # Lire le fichier Excel (feuille 'publication')
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name='publications')
        # Limiter la description à 100 caractères
        df['Description'] = df['Description'].str[:100] + '...' if df['Description'].str.len().gt(100).any() else df['Description']
        # Préparer les données pour le template (convertir en liste de dictionnaires)
        publications = df.to_dict(orient='records')
        region_name = region_publication
        print('publications ', region_name)
        return render_template('publications.html', publications=publications, region_name=region_name)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier Excel : {e}")
        return "Erreur lors du chargement des publications", 500

@app.route('/publications/<title>')  # Changé de '/publications' à '/publication' pour correspondre à vos logs
def publication_detail(title):
    # Nettoie et normalise le titre pour correspondre (minuscules avec underscores, puis espaces pour la comparaison)
    normalized_title = title.lower().replace('_', ' ')  # Transforme "comptes_regionaux" en "comptes regionaux"
    # Recherche la publication dans les données
    publication = None
    for pub_title, data in publications_data.items():
        # Normalise pub_title en minuscules avec espaces pour correspondre à normalized_title
        normalized_pub_title = pub_title.replace('_', ' ').lower()
        if normalized_pub_title == normalized_title:
            publication = data
            break
    if not publication:
        abort(404, description=f"Publication '{normalized_title}' non trouvée")
    # Génère le numéro de publication en utilisant normalized_title pour être cohérent
    publication_number = f"P{list(publications_data.keys()).index(pub_title) + 1:03d}"
    print('vue de region dans publication',region_publication)
    return render_template('publications_detail.html',
                          publication_title=publication['title'],
                          publication_description=publication['description'],
                          publication_date=publication['date'],
                          publication_number=publication_number,  # Utilise la clé normalisée
                          region_name=region_publication)








""" 
Cette fonction permet d'acceder a la page de requête
search_indicators2=Page d'acces global
search_indicatorsR=Page d'acces spécifique à une region
"""
# Routes d'accès par requete cocher et le plus simple
@app.route('/search_indicators')
def search_indicators():
    indicateurs = qr.options_indicateur()  # Fonction qui récupère les indicateurs
    return render_template('search_indicateur.html',indicateurs=indicateurs)

# Route pour afficher en fonction de la région
@app.route('/search_indicatorsR')
def search_indicatorsR():
    indicateurs = qr.options_indicateur()  # Fonction qui récupère les indicateurs
    return render_template('search_indicateurR.html',indicateurs=indicateurs)




@app.route('/search_indicators2/<path:indicateur>') 
def request_indicateur2(indicateur):
    # Charger les données depuis MySQL
    df= qr.get_data_from_mysql_V1()
    indicateur_SELECT = urllib.parse.unquote(indicateur)
    definitions=None
    # Obtenir les options pour chaque filtre (indicateur, région, etc.
    df_filtered = pd.DataFrame()
    df_filtered =df
    # Appliquer le filtre si 'indicateur' existe et que la sélection d'indicateur est présente
    if indicateur_SELECT and 'Indicateurs' in df_filtered.columns:
        # Convertir la colonne 'indicateur' en chaînes de caractères
        df_filtered['Indicateurs'] = df_filtered['Indicateurs'].astype(str).str.strip().str.lower()
        definitions=qr.definition_indicateur(indicateur_SELECT)
        mode_calcul=qr.mode_calcul_indicateur(indicateur_SELECT)
        
        # Appliquer le filtre sur la colonne 'indicateur'
        df_filtered = df_filtered[df_filtered['Indicateurs'] == indicateur_SELECT.strip().lower()]
    else:
        print("Aucun filtre appliqué sur l'indicateur")
    # Supprimer les colonnes contenant uniquement des NaN
    df_filtered = df_filtered.dropna(axis=1, how='all')
    df_filtered = df_filtered.fillna('-')
    df_final = pd.DataFrame()
    for _, row in df_filtered.iterrows():
            dimension_cols = row['Dimension'].split(',')
            category_values = row['Modalites'].split('/')
            dimension_cols = [col.strip() for col in dimension_cols]
            category_values = [value.strip() for value in category_values]
            dimension_dict = dict(zip(dimension_cols, category_values))
            temp_row = pd.Series(dimension_dict)
            temp_row['Indicateurs'] = row['Indicateurs']
            temp_row["Valeur"] = row["Valeur"]
            temp_row["Annee"] = row["Annee"]
            cle_pivot_table = ",".join(dimension_cols) + ",Annee"
            temp_row["cle_pivot_table"] = cle_pivot_table
            # Ajouter cette ligne nettoyée au DataFrame final
            df_final = pd.concat([df_final, temp_row.to_frame().T], ignore_index=True)
            
    df_filtered = df_final.dropna(axis=1, how='all')
    if df_filtered.empty:
            return render_template('no_data.html')  # Rediriger vers la page 'Aucune donnée disponible'
    # Stocker le DataFrame filtré dans la session pour une utilisation ultérieure
    df_filtered_json = df_filtered.to_json(orient='split')  # Convertir en JSON pour le stockage
    session['df_filtered'] = df_filtered_json
    # Obtenir les colonnes valables pour les désagrégations
    existing_columns = df_filtered.columns.tolist()
    columns_to_exclude = ['Valeur', 'Indicateurs','cle_pivot_table']
    desaggregation_columns = [col for col in existing_columns if col not in columns_to_exclude]
    return render_template(
        'result.html',
        definitions=definitions,
        mode_calcul=mode_calcul,
        colonne_valable=desaggregation_columns,  # Colonnes à utiliser pour désagréger les données
        indicateur2=indicateur_SELECT,  # Indicateur sélectionné
        df_filtered=df_filtered_json  # Data JSON pour le filtrage
    )


# Accès spécefique à une région
@app.route('/search_indicatorsR/<path:indicateur>') 
def request_indicateurR(indicateur):
    # Charger les données depuis MySQL
    
    df= qr.get_data_from_mysql_VR(region_publication)
    indicateur_SELECT = urllib.parse.unquote(indicateur)
    definitions=None
    # Obtenir les options pour chaque filtre (indicateur, région, etc.
    df_filtered = pd.DataFrame()
    df_filtered =df
    # Appliquer le filtre si 'indicateur' existe et que la sélection d'indicateur est présente
    if indicateur_SELECT and 'Indicateurs' in df_filtered.columns:
        # Convertir la colonne 'indicateur' en chaînes de caractères
        df_filtered['Indicateurs'] = df_filtered['Indicateurs'].astype(str).str.strip().str.lower()
        definitions=qr.definition_indicateur(indicateur_SELECT)
        mode_calcul=qr.mode_calcul_indicateur(indicateur_SELECT)
        
        # Appliquer le filtre sur la colonne 'indicateur'
        df_filtered = df_filtered[df_filtered['Indicateurs'] == indicateur_SELECT.strip().lower()]
    else:
        print("Aucun filtre appliqué sur l'indicateur")
    # Supprimer les colonnes contenant uniquement des NaN
    df_filtered = df_filtered.dropna(axis=1, how='all')
    df_filtered = df_filtered.fillna('-')
    df_final = pd.DataFrame()
    for _, row in df_filtered.iterrows():
            dimension_cols = row['Dimension'].split(',')
            category_values = row['Modalites'].split('/')
            dimension_cols = [col.strip() for col in dimension_cols]
            category_values = [value.strip() for value in category_values]
            dimension_dict = dict(zip(dimension_cols, category_values))
            temp_row = pd.Series(dimension_dict)
            temp_row['Indicateurs'] = row['Indicateurs']
            temp_row["Valeur"] = row["Valeur"]
            temp_row["Annee"] = row["Annee"]
            cle_pivot_table = ",".join(dimension_cols) + ",Annee"
            temp_row["cle_pivot_table"] = cle_pivot_table
            # Ajouter cette ligne nettoyée au DataFrame final
            df_final = pd.concat([df_final, temp_row.to_frame().T], ignore_index=True)
            
    df_filtered = df_final.dropna(axis=1, how='all')
    if df_filtered.empty:
            return render_template('no_data.html')  # Rediriger vers la page 'Aucune donnée disponible'
    # Stocker le DataFrame filtré dans la session pour une utilisation ultérieure
    df_filtered_json = df_filtered.to_json(orient='split')  # Convertir en JSON pour le stockage
    session['df_filtered'] = df_filtered_json
    # Obtenir les colonnes valables pour les désagrégations
    existing_columns = df_filtered.columns.tolist()
    columns_to_exclude = ['Valeur', 'Indicateurs','cle_pivot_table']
    desaggregation_columns = [col for col in existing_columns if col not in columns_to_exclude]
    return render_template(
        'result.html',
        definitions=definitions,
        mode_calcul=mode_calcul,
        colonne_valable=desaggregation_columns,  # Colonnes à utiliser pour désagréger les données
        indicateur2=indicateur_SELECT,  # Indicateur sélectionné
        df_filtered=df_filtered_json  # Data JSON pour le filtrage
    )

#----------------Autocomplétion
from flask import jsonify, request

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify([])
    # Charger les données depuis MySQL
    df = qr.get_data_from_mysql_V1()
    # Vérifier que la colonne 'Indicateurs' existe
    if 'Indicateurs' not in df.columns:
        return jsonify([])
    # Convertir en minuscule pour une recherche insensible à la casse
    df['Indicateurs'] = df['Indicateurs'].astype(str).str.strip().str.lower()
    # Filtrer les indicateurs qui contiennent le texte saisi
    suggestions = df[df['Indicateurs'].str.contains(query, na=False)]['Indicateurs'].unique().tolist()
    return jsonify(suggestions)








"""
Cette fonction a pour rôle de permet le charger des données des requêtes
Aussi cette partie est dedié dans les requêtes utilisatrices.
Toutes les fonctions pour la requêtes sont écrites ici.
"""



@app.route('/request_indicateur', methods=['GET', 'POST'])
def request_indicateur():
    # Charger les données depuis MySQL
    data_mysql = qr.get_data_from_mysql_V1()
    # Obtenir les options pour chaque filtre (indicateur, région, etc.)
    indicateurs_options = qr.options_indicateur()
    indicateur_SELECT = None
    df_filtered = pd.DataFrame()
    definitions = None
    mode_calcul = None
    if request.method == 'GET':
        indicateur_SELECT = request.args.get('indicateur_elastic')
        df_filtered = data_mysql
        
        if indicateur_SELECT and 'Indicateurs' in df_filtered.columns:
            try:
                definitions = qr.definition_indicateur(indicateur_SELECT)
                mode_calcul = qr.mode_calcul_indicateur(indicateur_SELECT)
                
                df_filtered['Indicateurs'] = df_filtered['Indicateurs'].astype(str).str.strip().str.lower()
                df_filtered = df_filtered[df_filtered['Indicateurs'] == indicateur_SELECT.strip().lower()]
                
                if df_filtered.empty:
                    return render_template('no_data.html')  # Rediriger vers la page 'Aucune donnée disponible'
                    
            except Exception as e:
                print(f"Erreur lors de la récupération de l'indicateur: {e}")
                definitions = "Indicateur non disponible"
                mode_calcul = "Non défini"
        
        df_final = pd.DataFrame()
        df_filtered = df_filtered.fillna('-')
        for _, row in df_filtered.iterrows():
            dimension_cols = row['Dimension'].split(',')
            category_values = row['Modalites'].split('/')
            dimension_cols = [col.strip() for col in dimension_cols]
            category_values = [value.strip() for value in category_values]
            dimension_dict = dict(zip(dimension_cols, category_values))
            temp_row = pd.Series(dimension_dict)
            temp_row['Indicateurs'] = row['Indicateurs']
            temp_row["Valeur"] = row["Valeur"]
            temp_row["Annee"] = row["Annee"]
            cle_pivot_table = ",".join(dimension_cols) + ",Annee"
            temp_row["cle_pivot_table"] = cle_pivot_table
            df_final = pd.concat([df_final, temp_row.to_frame().T], ignore_index=True)
        
        df_filtered = df_final.dropna(axis=1, how='all')
        
        if df_filtered.empty:
            return render_template('no_data.html')  # Rediriger vers la page 'Aucune donnée disponible'
        
        df_filtered_json = df_filtered.to_json(orient='split')
        session['df_filtered'] = df_filtered_json
        existing_columns = df_filtered.columns.tolist()
        columns_to_exclude = ['Valeur', 'Indicateurs','cle_pivot_table']
        desaggregation_columns = [col for col in existing_columns if col not in columns_to_exclude]
    
    return render_template(
        'result.html',
        definitions=definitions,
        mode_calcul=mode_calcul,
        colonne_valable=desaggregation_columns,
        indicateurs=indicateurs_options,
        indicateur2=indicateur_SELECT,
        df_filtered=df_filtered_json
    )

#
    
@app.route('/process_columns', methods=['POST'])
def process_columns():
    # Récupérer les colonnes envoyées par la requête AJAX
    data = request.get_json()
    row_columns = data.get('row_columns', [])
    col_columns = data.get('col_columns', [])
    value_column = data.get('value_column', 'Valeur')
    my_index=[row_columns,col_columns]
    #print("Les choix utilisateurs",my_index)
    # Charger les données réelles depuis la session ou depuis MySQL si nécessaire
    df_filtered_json = session.get('df_filtered', None)
    if df_filtered_json:
        df_filtered = pd.read_json(io.StringIO(df_filtered_json), orient='split')
    else:
        return jsonify({"error": "Aucune donnée disponible dans la session"}), 400
    # Vérification et conversion de la colonne 'valeur' en numérique
    if value_column in df_filtered.columns:
        try:
            df_filtered[value_column] = pd.to_numeric(df_filtered[value_column], errors='coerce')
            df_filtered = df_filtered.dropna(subset=[value_column])
        except Exception as e:
            return jsonify({"error": f"La colonne '{value_column}' contient des données non numériques : {e}"}), 400
    try:

        my_index= list(chain.from_iterable(my_index))
        data_V1=my_index
        #Ordonnée la data
        df_filtered['cle_pivot_table'] = sorted(df_filtered['cle_pivot_table'])
        # Convertir my_index en un ensemble pour faciliter la comparaison
        my_index_set = set(my_index)

        # Filtrer les lignes de df_filtered où cle_pivot_table contient les mêmes éléments que my_index
        data = df_filtered[df_filtered['cle_pivot_table'].apply(lambda x: set(x.split(',')) == my_index_set)]
        data['Annee'] = df_filtered['Annee'].astype(str)

        # Afficher le DataFrame filtré pour vérification
        pivot_table = pd.pivot_table(
            data,
            index=row_columns,
            columns=col_columns,
            values=value_column,
            aggfunc='sum',
            fill_value=0
        )
        pivot_table = pivot_table 
        # Réinitialiser l'index pour convertir les données en format JSON structuré
        pivot_table.reset_index(inplace=True)
        result_data = {
            "columns": [list(map(str, col)) if isinstance(col, tuple) else [str(col)] for col in pivot_table.columns],
            "index": list(pivot_table.index),
            "data": pivot_table.values.tolist()
        }
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la création du tableau croisé dynamique : {e}"}), 400

    return jsonify(result_data)


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Charger les données filtrées depuis la session
        df_filtered_json = session.get('df_filtered', None)
        if df_filtered_json is None:
            return jsonify({"error": "Aucune donnée filtrée disponible."}), 404
        # Convertir le JSON en DataFrame et ensuite en dictionnaire
        df_filtered = pd.read_json(df_filtered_json, orient='split')
        data = df_filtered.to_dict(orient='records')
        # Affichage pour vérifier le contenu
        return jsonify(data)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return jsonify({"error": "Une erreur est survenue lors du chargement des données."}), 500








#Pour la liste des indicateur dans template domaine-sous-domaine-indicateur, pour la domaine indicateur
@app.route('/get_data2')
def get_data2():
    # Charger le fichier Excel
    df = pd.read_excel('search_indicateur.xlsx')
    # Grouper les données par Domaine et Thématique
    data = df.groupby(['Domaine', 'Thematique'])['Indicateurs'].apply(list).to_dict()
    data_str_keys = {f"{key[0]}, {key[1]}": value for key, value in data.items()}

    # Retourner les données en JSON
    return jsonify(data_str_keys)


# Generateur de données excel
@app.route('/generateur')
def generateur():
    return render_template('generateur_excel.html')





if __name__ == '__main__':
    app.run(debug=True)