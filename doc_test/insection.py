import pandas as pd
import mysql.connector
import pymysql  # Ou tout autre connecteur de base de données
import sys
sys.path.append('/Users/mac/Desktop/dashbord/dashbord2/')
import config as cf

# Connexion à la base de données MySQL
conn = cf.create_connection()
cursor = conn.cursor()

# Lire le fichier Excel
df = pd.read_excel("IndicateurTest.xlsx")
# Nettoyer la colonne 'Valeur' en supprimant les espaces et en convertissant en float
df['Valeur'] = df['Valeur'].apply(lambda x: float(str(x).replace(' ', '')) if pd.notnull(x) else None)
# Préparer la requête SQL d'insertion
insert_query = """
    INSERT INTO `valeur_indicateur_libelle_ok` 
    (`id`, `indicateur`, `valeur`, `annee`, `region`, `departement`, `sousprefecture`, `statut_approbation`, 
     `cycle_scolaire`, `primaire`, `sexe`, `age`, `groupe_age`)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Boucler à travers les lignes du DataFrame et insérer dans MySQL
for index, row in df.iterrows():
    data = (
        row['id'], row['Indicateur'], row['Valeur'], row['Année de collecte'], 
        row['Région'], row['Département'], row['Sous-prefecture'], row['Statut'], 
        row['Cycle'], row['Niveau Primaire'], row['Sexe'], row['Age'], row['groupe age']
    )
    cursor.execute(insert_query, data)
print("Données inserées avec succès")
# Valider les changements
conn.commit()

# Fermer la connexion
cursor.close()
conn.close()
