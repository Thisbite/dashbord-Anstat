from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging
import my_queries as qr
import data as dt
import config as cf
import pandas as pd
from io import StringIO
import folium
import json
import branca.colormap as cm 
import random
import time
from datetime import datetime
import mysql.connector
from unidecode import unidecode
import pandas as pd
from io import StringIO
from flask import Flask, session
from flask_session import Session
import redis
#https://colab.research.google.com/drive/1oBqwcSMb4YTrn0NFUiQzJCiZ65uIay_S?hl=fr#scrollTo=CJAQGVAWNNPw
#brew services restart elastic/tap/elasticsearch-full
#redis-server

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
    
    


    





#index_data_from_excel()
#index_data_from_excel()
#
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




    



# Date de départ pour le calcul des naissances (exemple : 1er janvier 2022)
START_DATE = datetime(2022, 1, 1)
STORAGE_FILE = 'births_data.json'
# Fonction pour calculer les naissances par minute avec variation
def get_births_per_minute():
    moyenne_naissance = 1.3  # naissances par seconde
    variation = random.uniform(-0.034, 0.034)
    return int(moyenne_naissance + variation )  # Convertir en naissances par minute

# Fonction pour charger l'état actuel du compteur
def load_birth_data():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            data = json.load(f)
            return data
    return {'total_births': 29090897, 'last_time': START_DATE.timestamp()} #Date de depart

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



















# Tableau de bord ------------------------------------------------------------------Tableau de bord

@app.route('/dashboard')
def dashboard():
    # Définir les années de 2018 à 2024
    region = request.args.get('region', session.get('region', 'DefaultRegion'))
    min_year = 2018
    max_year = 2024
    annees = list(range(min_year, max_year + 1))
    sexes = ['M', 'F']

    data = { 'M': [], 'F': [] }
    data_coton = []
    
    # Générer les données pour chaque année et sexe pour la région sélectionnée
    for sexe in sexes:
        for annee in annees:
            total_population = random.randint(50000, 1000000)
            data[sexe].append({'annee': annee, 'valeur': total_population})
            
    # Générer les données du coton pour chaque année
    for annee in annees:
        total_population = random.randint(50000, 1000000)
        data_coton.append(total_population)
    
    return render_template('pages/dashboard.html', region=region, data=data, annees=annees, data_coton=data_coton)

#--------------------------------------Fiche synoptique
#Fiche synoptique
@app.route('/fiche-synoptique')
def fiche_synoptique():
     # Définir les années de 2018 à 2024
    region = request.args.get('region', session.get('region'))
    
    if region is None:
        return "Veuillez choisir une région.", 400
    return render_template('pages/notifications.html',region=region)
    






#---------------------------------------------------Home page pour accueil
@app.route('/')
def list_regions():
    regions = qr.options_regions()
    #map_html = dt.statistiques()
    coord_list=[]
    # Données
    years = [2019, 2020, 2021, 2022, 2023]
    population = [24.0, 27.0, 27.4, 29.8, 30.38]
    school_enrollment_rate = [75, 76, 78, 79, 80]
    age_groups = ['0-14 ans', '15-24 ans', '25-54 ans', '55 - 59 ans','60 -64 ','65-69','70-74 ans']
    age_distribution = [40, 20, 30, 10, 18, 20]

    return render_template('home.html',
                           coord_list=coord_list,
                           years=years,
                           population=population,
                           school_enrollment_rate=school_enrollment_rate,
                           age_groups=age_groups,
                           age_distribution=age_distribution,
                           regions=regions,
                           )




#Affichage de pdf
@app.route('/region/<region>')
def show_region_pdf(region):
    pdf_path = f"static/pdfs/{region}.pdf"  # Chemin vers le fichier PDF
    try:
        return render_template('region_pdf.html', region=region)
    except FileNotFoundError:
        return f"PDF pour la région {region} non trouvé.", 404


# Route pour afficher la page avec les indicateurs et les régions
@app.route('/search_indicators')
def search_indicators():
    annee_debut = request.args.get('annee_debut')
    annee_fin = request.args.get('annee_fin')
    indicateurs = qr.options_indicateur()  # Fonction qui récupère les indicateurs
    regions = qr.options_regions()  # Fonction qui récupère les régions
    return render_template('search_indicateur.html',indicateurs=indicateurs,regions=regions)
#print(qr.options_indicateur())
# Route pour récupérer les départements en fonction de la région sélectionnée
@app.route('/get_departements', methods=['GET'])
def get_departements():
    region = request.args.get('region')
    df = qr.get_data_from_mysql()  # Récupère les données depuis la base de données
    departements = df[df['region'] == region]['departement'].sort_values().unique()
    return jsonify(list(departements))

# Route pour récupérer les sous-préfectures en fonction du département sélectionné
@app.route('/get_sous_prefectures', methods=['GET'])
def get_sous_prefectures():
    departement = request.args.get('departement')
    df = qr.get_data_from_mysql()  # Récupère les données depuis la base de données
    sous_prefectures = df[df['departement'] == departement]['sousprefecture'].sort_values().unique()
    return jsonify(list(sous_prefectures))


















# Page de requête au niveau de l'accueil
@app.route('/request_indicateur', methods=['GET', 'POST'])
def request_indicateur():
    # Charger les données depuis MySQL
    df = qr.get_data_from_mysql()
    
    # Obtenir les options pour chaque filtre (indicateur, région, etc.)
    indicateurs_options = qr.options_indicateur()
    indicateur_SELECT = None
    df_filtered = pd.DataFrame()

    if request.method == 'GET':
        indicateur_SELECT = request.args.get('indicateur_elastic')
        
        # Appliquer les filtres (indicateur, etc.)
        df_filtered = df.drop(columns=['statut_approbation', 'id'], errors='ignore')

        # Appliquer le filtre si 'indicateur' existe et que la sélection d'indicateur est présente
        if indicateur_SELECT and 'indicateur' in df_filtered.columns:
            # Convertir la colonne 'indicateur' en chaînes de caractères
            df_filtered['indicateur'] = df_filtered['indicateur'].astype(str).str.strip().str.lower()
            
            # Appliquer le filtre sur la colonne 'indicateur'
            df_filtered = df_filtered[df_filtered['indicateur'] == indicateur_SELECT.strip().lower()]
        else:
            print("Aucun filtre appliqué sur l'indicateur")
        
        # Supprimer les colonnes contenant uniquement des NaN
        df_filtered = df_filtered.dropna(axis=1, how='all')

        # Remplacer les valeurs manquantes par des chaînes vides
        df_filtered = df_filtered.fillna('-')

        # Stocker le DataFrame filtré dans la session pour une utilisation ultérieure
        df_filtered_json = df_filtered.to_json(orient='split')  # Convertir en JSON pour le stockage
        
        session['df_filtered'] = df_filtered_json

        # Obtenir les colonnes valables pour les désagrégations
        existing_columns = df_filtered.columns.tolist()
        columns_to_exclude = ['valeur', 'indicateur']
        desaggregation_columns = [col for col in existing_columns if col not in columns_to_exclude]
        print("Colonnes valables pour désagrégation :", desaggregation_columns)

    return render_template(
        'result.html',
        colonne_valable=desaggregation_columns,  # Colonnes à utiliser pour désagréger les données
        indicateurs=indicateurs_options,  # Options d'indicateurs pour le dropdown
        indicateur2=indicateur_SELECT,  # Indicateur sélectionné
        df_filtered=df_filtered_json  # Data JSON pour le filtrage
    )

import urllib
# Deuxieme bloc 
# Page de requête au niveau de l'accueil
@app.route('/search_indicators2/<path:indicateur>') 
def request_indicateur2(indicateur):
    # Charger les données depuis MySQL
    df = qr.get_data_from_mysql()
    indicateur_SELECT = urllib.parse.unquote(indicateur)
    print('Indicateur de js:',indicateur_SELECT)
    # Obtenir les options pour chaque filtre (indicateur, région, etc.
    df_filtered = pd.DataFrame()
    df_filtered = df.drop(columns=['statut_approbation', 'id'], errors='ignore')
    # Appliquer le filtre si 'indicateur' existe et que la sélection d'indicateur est présente
    if indicateur_SELECT and 'indicateur' in df_filtered.columns:
        # Convertir la colonne 'indicateur' en chaînes de caractères
        df_filtered['indicateur'] = df_filtered['indicateur'].astype(str).str.strip().str.lower()
        
        # Appliquer le filtre sur la colonne 'indicateur'
        df_filtered = df_filtered[df_filtered['indicateur'] == indicateur_SELECT.strip().lower()]
    else:
        print("Aucun filtre appliqué sur l'indicateur")
    # Supprimer les colonnes contenant uniquement des NaN
    df_filtered = df_filtered.dropna(axis=1, how='all')

    # Remplacer les valeurs manquantes par des chaînes vides
    df_filtered = df_filtered.fillna('-')

    # Stocker le DataFrame filtré dans la session pour une utilisation ultérieure
    df_filtered_json = df_filtered.to_json(orient='split')  # Convertir en JSON pour le stockage
    
    session['df_filtered'] = df_filtered_json
    # Obtenir les colonnes valables pour les désagrégations
    existing_columns = df_filtered.columns.tolist()
    columns_to_exclude = ['valeur', 'indicateur']
    desaggregation_columns = [col for col in existing_columns if col not in columns_to_exclude]
    return render_template(
        'result.html',
        colonne_valable=desaggregation_columns,  # Colonnes à utiliser pour désagréger les données
        indicateur2=indicateur_SELECT,  # Indicateur sélectionné
        df_filtered=df_filtered_json  # Data JSON pour le filtrage
    )
import io

@app.route('/process_columns', methods=['POST'])
def process_columns():
    # Récupérer les colonnes envoyées par la requête AJAX
    data = request.get_json()
    row_columns = data.get('row_columns', [])
    col_columns = data.get('col_columns', [])
    value_column = data.get('value_column', 'valeur')

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
    # Création du tableau croisé dynamique
    try:
        pivot_table = pd.pivot_table(
            df_filtered,
            index=row_columns,
            columns=col_columns,
            values=value_column,
            aggfunc='sum',
            fill_value=0
        )

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





# Données de test
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
        print(data)  # Ceci va afficher les données récupérées dans le terminal
        
        return jsonify(data)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return jsonify({"error": "Une erreur est survenue lors du chargement des données."}), 500



@app.route('/search_boostrap', methods=['GET', 'POST'])
def search_boostrap():
    return render_template('boostrap_search.html')


@app.route('/dash_region', methods=['GET', 'POST'])
def dash_region():
    return render_template('dash_region.html')







@app.route('/get_data2')
def get_data2():
    # Charger le fichier Excel
    df = pd.read_excel('search_indicateur.xlsx')

    # Grouper les données par Domaine et Thématique
    data = df.groupby(['Domaine', 'Thematique'])['Indicateurs'].apply(list).to_dict()
    data_str_keys = {f"{key[0]}, {key[1]}": value for key, value in data.items()}

    # Retourner les données en JSON
    return jsonify(data_str_keys)




# La liste des niveau de désagrégation
indicateurs_data = cf.load_excel_data("First.xlsx")

# Fonction pour récupérer la liste des niveaux de désagrégation
def get_niveaux_desagregation(indicateurs_data):
    return list(indicateurs_data.keys())


# Exemple d'utilisation
niveaux_desagregation = get_niveaux_desagregation(indicateurs_data)
print(niveaux_desagregation)


@app.route('/abou', methods=['POST', 'GET'])
def result_abou():
    global filtered_df, row_dimensions, column_dimensions  # Utilisation des variables globales
    liste_colonne = ["Index"]  # Initialisation par défaut avec 'Année'

    # Vérifier si des dimensions ont été définies
    if request.method == 'POST':
        data = request.get_json()
        if data:
            test = data.get('rowDimensions', [])
            print('Result abou ligne:', test)
    
    niveaux_desagregation = [key.strip() for key in indicateurs_data.keys() if key.strip()]

    if filtered_df is not None and not filtered_df.empty:
        ma_table = cf.clean_create_pivot_table(
            filtered_df, row_dimensions, column_dimensions, "Valeurs", "Année"
        )
        
        ma_table = pd.DataFrame(ma_table)
        ma_table=ma_table.astype('object').fillna('-')
        print(' première colonne:', ma_table.columns)



        # Ajouter les colonnes de 'column_dimensions' à 'liste_colonne', en évitant les doublons
        if column_dimensions:
            liste_colonne.extend([col for col in column_dimensions if col not in liste_colonne])

        ma_table_html = f"""
        <div style="overflow-x: auto;">
            {ma_table.to_html(
                classes="table table-bordered table-striped table-hover",  # Ajout de classes supplémentaires
                header=True,
                index=True,
                border=0  # Supprime les bordures par défaut pour un style plus léger
            )}
        </div>
        """
    else:
        ma_table_html = "<p>Aucune donnée à afficher. Veuillez effectuer une sélection.</p>"

    return render_template('result_abou.html', dimensions=niveaux_desagregation, ma_table_html=ma_table_html, liste_colonne=liste_colonne)



# Route pour récupérer les données des dimensions en fonction de la sélection (via AJAX)
@app.route('/get_dimension_data/')
def get_dimension_data():
    dimension = request.args.get('dimension')
    return jsonify(indicateurs_data.get(dimension, []))


# Variables globales pour stocker le DataFrame filtré et les dimensions
df = cf.wrangle('First.xlsx')
filtered_df = None
row_dimensions = []
column_dimensions = []

@app.route('/save_dimensions', methods=['POST'])
def save_dimensions():
    global filtered_df, row_dimensions, column_dimensions  # Utilisation des variables globales
    data = request.get_json()

    # Récupération des données envoyées par JavaScript
    row_dimensions = data.get('rowDimensions', [])
    column_dimensions = data.get('columnDimensions', [])
    index = column_dimensions + row_dimensions

    # Traitement des dimensions récupérées
    print("Dimensions de ligne:", row_dimensions)
    print("Dimensions de colonne:", column_dimensions)
    print("Ensemble choisi par l'utilisateur:", index)
    
    sorted_index = sorted(index)
    filter_value = '/'.join(sorted_index)
    filter_column = "Dimension"  # Nom explicite de la colonne

    # Filtrage du DataFrame en fonction du filtre
    filtered_df = df[df[filter_column] == filter_value]

    if filtered_df.empty:
        print(f"Aucune donnée trouvée pour la dimension '{filter_value}'.")
        response = {"status": "error", "message": "Aucune donnée trouvée avec le filtre spécifié"}
    else:
        print(f"Données filtrées pour la dimension '{filter_value}':")
        response = {"status": "success", "message": "Données filtrées prêtes à l'affichage"}

    # Retourne la réponse JSON
    return jsonify(response)



    
    
    

#Fin du das bord avec les régions de la CI

if __name__ == '__main__':
    app.run(debug=True)