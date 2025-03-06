import pandas as pd
import itertools

# Charger les données depuis un fichier Excel
df = pd.read_excel('questionnaire.xlsx')

# Récupérer les listes de régions et de groupes d'âges
regions = df['Région'].tolist()
groupes_ages = df['Groupe d\'âges'].tolist()
sexes=df['Sexe'].tolist()
# Créer toutes les combinaisons entre les régions et les groupes d'âges
comb_region_groupe_age = [f"{region}/{age_group}" for region, age_group in itertools.product(regions, groupes_ages)]
comb_region_sexe_groupe_age = [f"{region}/{sexes}/{age_group}" for region, sexe,age_group in itertools.product(regions,sexes,groupes_ages)]
comb_region_sexe = [f"{region}/{sexe}" for region, sexe in itertools.product(regions, sexes)]


# Créer un DataFrame avec une seule colonne contenant les combinaisons
df_region_groupe_age= pd.DataFrame(comb_region_groupe_age, columns=['Categories'])
df_region_sexe= pd.DataFrame(comb_region_sexe, columns=['Categories'])
df_region_sexe_groupe_age= pd.DataFrame(comb_region_sexe_groupe_age, columns=['Categories'])

# Afficher le DataFrame
print(df_region_sexe_groupe_age)