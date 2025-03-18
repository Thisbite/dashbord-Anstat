from datetime import datetime

def days_in_year(year):
    # Retourne 366 si bissextile, 365 sinon
    return 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365

def minutes_in_year(year):
    # Calcule le nombre total de minutes dans une année
    return days_in_year(year) * 24 * 60

def naissance_deces_pop():
    # Données démographiques prédéfinies
    data_nais_deces_pop = {
        "population": [777556, 797114, 793064, 787604, 804768, 796472],
        "population_add": [31719274, 32496830, 33293944, 34087008, 34874612, 35679380],
        "naissance": [1025716, 1047630, 1045355, 1041416, 1061168, 1054794],
        "deces": [248159, 250517, 252290, 253814, 256397, 258324],
        "year": [2025 + i for i in range(6)]  # 2025 à 2030
    }

    # Année actuelle
    current_year = datetime.now().year

    # Vérifier si l'année est dans les données
    if current_year not in data_nais_deces_pop["year"]:
        return f"Données non disponibles pour l'année {current_year}"

    # Index de l'année actuelle
    index = data_nais_deces_pop["year"].index(current_year)

    # Dates de référence et actuelle
    date_ref = datetime(current_year, 1, 1)  # Début de l'année
    date_actu = datetime.now()

    # Nombre de jours écoulés
    elapsed_days = (date_actu - date_ref).days

    # Nombre de minutes écoulées
    elapsed_minutes = (date_actu - date_ref).total_seconds() / 60

    # Données annuelles
    naissance_annuelle = data_nais_deces_pop["naissance"][index]
    deces_annuel = data_nais_deces_pop["deces"][index]
    population_annuelle = data_nais_deces_pop["population"][index]
    population_base = data_nais_deces_pop["population_add"][index]

    # Calculs
    days = days_in_year(current_year)
    minutes = minutes_in_year(current_year)

    # Naissances et décès cumulés jusqu'à maintenant
    naissance_cumulee = int(naissance_annuelle / days) * elapsed_days
    deces_cumule = int(deces_annuel / days) * elapsed_days
    pop_actuelle = population_base + int(population_annuelle / minutes * elapsed_minutes)

    return naissance_cumulee, deces_cumule, pop_actuelle

# Exemple d'utilisation
if __name__ == "__main__":
    naissances, deces, population = naissance_deces_pop()
    print(f"Naissances cumulées : {naissances}")
    print(f"Décès cumulés : {deces}")
    print(f"Population actuelle : {population}")