import pymysql  # Ou tout autre connecteur de base de données
import config as cf

# Chemin vers le fichier texte de sortie
output_file = "resultats_population.txt"

# Créer la connexion à la base de données
try:
    connection = cf.create_connection()

    # Créer un curseur à partir de la connexion
    cursor = connection.cursor()

    # Requête pour obtenir les colonnes de la table
    cursor.execute("SHOW COLUMNS FROM annuaire.valeur_indicateur_libelle_ok")
    columns = cursor.fetchall()

    # Liste des colonnes que l'on veut ignorer si elles sont nulles ou vides, sauf 'sexe'
    desaggregation_columns = ['groupe_age', 'departement', 'age', 'sexe']

    # Initialiser les conditions pour ignorer les colonnes non pertinentes
    conditions = ["region = 'PORO'"]  # Toujours avoir la région dans les conditions
    #conditions.append("sexe = 'T'")  # Condition pour le sexe masculin
    #conditions.append("age = '17'")  # Condition explicite pour l'âge 17

    # Sélectionner les colonnes pour l'agrégation (par exemple, 'region' et 'sousprefecture')
    aggregation_columns = ['region','age']

    # Boucler sur les autres colonnes et ajouter des conditions dynamiques, sauf celles déjà explicitement fixées
    for column in desaggregation_columns:
        if column in [col[0] for col in columns]:  # Vérifier si la colonne existe dans la table
            if column not in ['age']:  # Ignorer 'sexe' et 'age' pour les conditions null/vides
                conditions.append(f"({column} IS NULL OR {column} = '')")

    # Construire la requête SQL avec agrégation
    # Utiliser les colonnes d'agrégation dans la clause SELECT et GROUP BY
    aggregation_columns_str = ', '.join(aggregation_columns)  # Utilisation de virgules pour la sélection
    sql_query = f"""
        SELECT {aggregation_columns_str}, SUM(valeur) AS total_population 
        FROM annuaire.valeur_indicateur_libelle_ok 
        WHERE {' AND '.join(conditions)} 
        GROUP BY {aggregation_columns_str}
    """

    # Exécuter la requête
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Ouvrir le fichier texte pour écrire les résultats
    with open(output_file, 'w') as file:
        # Écrire l'en-tête du tableau dans le fichier
        file.write(f"{aggregation_columns_str}, Total_population\n")
        file.write("=" * 50 + "\n")  # Séparateur

        # Afficher les résultats et les écrire dans le fichier
        if results:
            for row in results:
                aggregation_values = ', '.join([str(value) for value in row[:-1]])  # Valeurs des colonnes d'agrégation
                line = f"{aggregation_values}, {row[-1]}\n"
                file.write(line)  # Écrire chaque ligne dans le fichier
                print(line.strip())  # Afficher la même ligne dans la console

            print(f"Résultats sauvegardés dans '{output_file}'")
        else:
            print("Aucun résultat trouvé.")
            file.write("Aucun résultat trouvé.\n")

except pymysql.MySQLError as e:
    print(f"Erreur MySQL : {e}")
finally:
    # Fermer le curseur et la connexion si elles sont ouvertes
    if cursor:
        cursor.close()
    if connection:
        connection.close()
