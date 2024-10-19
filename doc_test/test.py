import pymysql  # Ou tout autre connecteur de base de données
import sys
sys.path.append('/Users/mac/Desktop/dashbord/dashbord2/')
import config as cf
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
app.secret_key = 'podmqjx128979po098RnhTRDIOU7809908765bT'

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}:{os.getenv('MYSQL_PASSWORD', '')}@"
    f"{os.getenv('MYSQL_HOST', 'localhost')}/{os.getenv('MYSQL_DATABASE', 'mydatabase')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données et de la migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    colonne_valable=['region', 'age', 'sexe', 'departement', 'commune', 'milieu']
    return render_template('index.html',colonne_valable=colonne_valable)


#Elle reste le protocole du Directeur
@app.route('/process_columns', methods=['POST'])
def process_columns():
    # Récupérer les colonnes envoyées par la requête AJAX
    data = request.get_json()
    columns = data.get('columns', [])

    # Simulation d'une base de données ou d'une source de données
    mock_data = [
        {'region': 'PORO', 'age': 17, 'sexe': 'Homme', 'total_population': 900},
        {'region': 'PORO', 'age': 18, 'sexe': 'Femme', 'total_population': 1670},
        {'region': 'PORO', 'age': 60,  'total_population': 800},
        {'region': 'PORO', 'sexe': 'Femme', 'total_population': 1200},
        {'region': 'PORO', 'total_population': 600},
        {'region': 'PORO', 'sexe': 'Homme', 'departement': 'Boundiali', 'total_population': 1500},
         {'region': 'PORO', 'commune': 'Kong', 'departement': 'Boundiali', 'total_population': 10},
          {'region': 'PORO', 'milieu': 'Urbain', 'departement': 'Boundiali', 'total_population': 45}
        
    ]

    # Convertir les données en DataFrame pour faciliter le traitement
    df = pd.DataFrame(mock_data)


    # Filtrer les colonnes pour créer desaggregation_columns
    existing_columns = df.columns.tolist()
    desaggregation_columns = [col for col in existing_columns if col != 'total_population']
    #desaggregation_columns=df.columns.tolist()
    
 
    # Initialiser les conditions pour ignorer les colonnes non pertinentes
    conditions = df['region'].notnull()  # Condition obligatoire sur 'region'

    # Ajouter des conditions pour ignorer les colonnes non pertinentes sauf 'sexe'
    for column in desaggregation_columns:
        if column in df.columns and column not in columns:  # Vérifier si la colonne existe et n'est pas dans les colonnes sélectionnées
            conditions &= (df[column].isnull() | (df[column] == ''))

    # Filtrer les données en fonction des conditions dynamiques
    filtered_df = df[conditions]

    # Agrégation : somme de la colonne 'total_population' en fonction des colonnes sélectionnées
    if 'total_population' not in columns:
        columns.append('total_population')
    aggregated_data = filtered_df.groupby(columns).sum().reset_index()

    # Transformer en dictionnaire pour renvoyer en JSON
    result_data = aggregated_data.to_dict(orient='records')

    # Retourner les données sous forme de JSON
    return jsonify(result_data)




if __name__ == '__main__':
    app.run(debug=True)