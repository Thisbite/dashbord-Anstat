from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
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



#---------------------------------------------------Home page pour accueil
@app.route('/')
def list_regions():
    regions = qr.options_regions()
    # Données
    years = [2019, 2020, 2021, 2022, 2023]
    population = [24.0, 27.0, 27.4, 29.8, 30.38]
    school_enrollment_rate = [75, 76, 78, 79, 80]
    age_groups = ['0-14 ans', '15-24 ans', '25-54 ans', '55 - 59 ans','60 -64 ','65-69','70-74 ans']
    age_distribution = [40, 20, 30, 10, 18, 20]
    liste_region=regions
    print(liste_region)
    return render_template('home.html',
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
    return render_template('region_vitrine.html',  
                            
                           indicateurs=region_data['indicateurs'],  
                           region_name=region,  
                           all_regions=regions) 







#--------------------------------------------------Fin du tableau de bord





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
    indicateurs = qr.options_indicateur()  # Fonction qui récupère les indicateurs
    regions = qr.options_regions()  # Fonction qui récupère les régions
    return render_template('search_indicateur.html',indicateurs=indicateurs,regions=regions)



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



# Page de requête au niveau de l'accueil---- Pour la page requete
@app.route('/search_indicators2/<path:indicateur>') 
def request_indicateur2(indicateur):
    # Charger les données depuis MySQL
    df= qr.get_data_from_mysql_V1()
    indicateur_SELECT = urllib.parse.unquote(indicateur)
    definitions=None
    print('Indicateur de js:',indicateur_SELECT)
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
    print('Definitions associée:',definitions)
    print('Mode de calcul:',mode_calcul)
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
import io

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
        data_V1=sorted(data_V1)
        print('mes index:',data_V1)
        #Ordonnée la data
        df_filtered['cle_pivot_table'] = sorted(df_filtered['cle_pivot_table'])
        # Convertir my_index en un ensemble pour faciliter la comparaison
        my_index_set = set(my_index)

        # Filtrer les lignes de df_filtered où cle_pivot_table contient les mêmes éléments que my_index
        data = df_filtered[df_filtered['cle_pivot_table'].apply(lambda x: set(x.split(',')) == my_index_set)]
        data['Annee'] = df_filtered['Annee'].astype(str)

        # Afficher le DataFrame filtré pour vérification
        print('Data pour clé:',data )
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


#Page  de recherche
@app.route('/search_boostrap', methods=['GET', 'POST'])
def search_boostrap():
    return render_template('boostrap_search.html')



#Pour la liste des indicateur dans template domaine-sous-domaine-indicateur
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