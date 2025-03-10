from mysql.connector import Error
import config as cf 
import pandas as pd

def options_regions():
    try:
        with cf.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nom_region FROM Region ORDER BY nom_region ASC")
            # Récupérer les résultats sous forme de liste de tuples
            regions = cursor.fetchall()
    except Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Exception in options_regions: {e}")
        return []
    
    regions=[row[0] for row in regions]
    return regions



#  La liste des indicateurs
def options_indicateur():
    try:
        with cf.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT indicateur FROM indicateur_v2 ")
            # Récupérer les résultats sous forme de liste de tuples
            indicateurs = cursor.fetchall()
    except Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Exception in options_regions: {e}")
        return []
    
    indicateurs =sorted([row[0] for row in indicateurs ])
    return indicateurs 



# Obtenir la définition associé à l'indicateur
# La fonction pour obtenir la définition en fonction de l'indicateur
def definition_indicateur(indicateur_choisi):
    try:
        with cf.create_connection() as conn:
            cursor = conn.cursor()
            indicateur_choisi = indicateur_choisi.strip().lower()
            # Requête pour obtenir la définition de l'indicateur choisi
            query = "SELECT definitions FROM indicateur_v2 WHERE indicateur = %s"
            cursor.execute(query, (indicateur_choisi,))
            # Récupérer le résultat
            result = cursor.fetchone()
            if result:
                return result[0]  # Retourne la définition si elle existe
            else:
                return f"Définition pour l'indicateur '{indicateur_choisi}' non trouvée."
    except Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Exception in definition_indicateur: {e}")
        return None


#Mode de calcul:
def mode_calcul_indicateur(indicateur_choisi):
    try:
        with cf.create_connection() as conn:
            cursor = conn.cursor()
            indicateur_choisi = indicateur_choisi.strip().lower()
            # Requête pour obtenir la définition de l'indicateur choisi
            query = "SELECT  mode_calcul FROM indicateur_v2 WHERE indicateur = %s"
            cursor.execute(query, (indicateur_choisi,))
            # Récupérer le résultat
            result = cursor.fetchone()
            if result:
                return result[0]  # Retourne la définition si elle existe
            else:
                return f"Mode de calcul pour l'indicateur '{indicateur_choisi}' non trouvée."
    except Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"Exception in definition_indicateur: {e}")
        return None



def get_data(filepath):
    df = pd.read_csv(filepath, sep=',')
    return df


def get_data_from_mysql():
    # Configurer les informations de connexion à la base de données MySQL
    conn = cf.create_connection()
    # Requête SQL pour sélectionner toutes les données
    query = "SELECT * FROM valeur_indicateur_libelle_ok"
    # Charger les données dans un DataFrame pandas
    df = pd.read_sql(query, conn)

    # Fermer la connexion
    conn.close()

    return df

def get_data_from_mysql_V1():
    # Configurer les informations de connexion à la base de données MySQL
    conn = cf.create_connection()
    # Requête SQL pour sélectionner toutes les données
    query = "SELECT Dimension,Modalites,Indicateurs,Annee,Valeur FROM V1_indicateur"
    # Charger les données dans un DataFrame pandas
    df = pd.read_sql(query, conn)

    # Fermer la connexion
    conn.close()

    return df

def get_data_from_mysql_VR(region_name):
    try:
        # Configurer les informations de connexion à la base de données MySQL
        conn = cf.create_connection()  # Je suppose que cf est votre module de configuration
        
        # Requête SQL avec paramètre sécurisé
        query = """
            SELECT Dimension, Modalites, Indicateurs, Annee, Valeur 
            FROM V1_indicateur 
            WHERE Region = %s
        """
        
        # Charger les données dans un DataFrame pandas avec le paramètre region_name
        df = pd.read_sql(query, conn, params=(region_name,))
        
        return df
    
    except mysql.connector.Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None
    
    finally:
        # Fermer la connexion même en cas d'erreur
        if conn.is_connected():
            conn.close()


# Pour la nouvelle base de données 
def insert_data_from_excel(file_path):
    # Charger le fichier Excel dans un DataFrame pandas
    df = pd.read_excel(file_path)
    # Renommer les colonnes si elles contiennent des accents ou espaces
    df.columns = ['Dimension', 'Modalites', 'Indicateurs', 'Année', 'Valeur']
    # Établir la connexion à la base de données
    conn =cf.create_connection()
    if conn is None:
        print("Connexion échouée. Impossible d'insérer les données.")
        return
    try:
        cursor = conn.cursor()
        # Requête d'insertion
        insert_query = """
        INSERT INTO V1_indicateur (Dimension, Modalites, Indicateurs, Annee, Valeur)
        VALUES (%s, %s, %s, %s, %s)
        """
        # Insérer chaque ligne du DataFrame dans la table
        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                row['Dimension'],
                row['Modalites'],
                row['Indicateurs'],
                row['Année'],
                row['Valeur']
            ))
        
        # Valider les changements
        conn.commit()
        print("Données insérées avec succès dans la table V1_indicateur.")
    
    except Error as e:
        print(f"Erreur lors de l'insertion des données : {e}")
    
    finally:
        # Fermer la connexion
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connexion MySQL fermée.")

# Chemin du fichier Excel
#file_path = 'V1_indicateurs.xlsx'
#insert_data_from_excel(file_path)

