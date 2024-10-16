from flask import Flask, render_template,jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    min_year = 2019
    max_year = 2040

    # Initialisation des listes de données
    data_commercants = []
    data_esperance_vie = []
    data_ratio_eleve_primaire = []

    # Générer les valeurs pour chaque année
    annees = list(range(min_year, max_year + 1))
    for annee in annees:
        data_commercants.append({
            'indicateur': 'Nombre de commerçants',
            'annee': annee,
            'valeur': round(random.randint(200, 2000))
        })

        data_esperance_vie.append({
            'indicateur': 'Espérance de vie à la naissance',
            'annee': annee,
            'valeur': round(random.randint(40, 130))
        })

        data_ratio_eleve_primaire.append({
            'indicateur': 'Ratio élève par salle primaire',
            'annee': annee,
            'valeur': round(random.uniform(20, 80), 2)
        })

    # Passer les données au template
    return render_template('test.html', min=min_year, max=max_year, 
                           data_commercants=data_commercants, 
                           data_esperance_vie=data_esperance_vie,
                           data_ratio_eleve_primaire=data_ratio_eleve_primaire
                           )










# Route pour servir les données en format JSON
@app.route('/data')
def get_data():
    data = []
    
    min_year = 2019
    max_year = 2040

  

    # Générer les valeurs pour chaque année
    annees = list(range(min_year, max_year + 1))
    
    # Générer les données pour l'indicateur "Production de cultures"
    cultures = ['Cacao', 'Café', 'Coton']


    for annee in annees:
        for culture in cultures:
            data.append({
                'indicateur': 'Production',
                'produit': culture,
                'annee': annee,
                'valeur': random.randint(1000, 5000)  # Production en tonnes, valeur aléatoire
            })
            
    # Générer les données pour l'indicateur "Effectif de la population"
    sexes = ['M', 'F']
    groupes_age = ['0-4', '5-9', '10-14', '15-19', '20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64']

    for annee in annees:
        for groupe in groupes_age:
            data.append({
                'indicateur': 'Effectif de la population',
                'annee': annee,
              
                'groupe_age': groupe,
                'valeur': random.randint(50000, 150000)  # Génération aléatoire d'effectif
            })
    
    # Générer les données pour un autre indicateur "Effectif de la population 1"
    for annee in annees:
        for sexe in sexes:
            data.append({
                'indicateur': 'Effectif de la population1',
                'annee': annee,
                'sexe': sexe,
                'valeur': random.randint(1000000, 8000000)  # Génération aléatoire d'effectif
            })
            
    #Generer le taux de mortalité

    zones= ['Régional','National']

    for annee in annees:
 
        for zone in zones:
            data.append({
                'indicateur': 'Taux de mortalité',
                'annee': annee,
                'zone':zone,
                'valeur': round(random.uniform(60, 100), 2)  # Taux entre 60% et 100%
            })
            
            
    # Générer les données pour le taux de pauvreté
    zones = ['Régional','National']
    
    for annee in annees:
        for zone in zones:
            data.append({
                'indicateur': 'Taux de pauvreté',
                'annee': annee,
                'zone': zone,
                'valeur': round(random.uniform(0, 100), 2)  # Taux entre 0% et 100%
            })
                
    # Générer les données pour l'indicateur "Taux de scolarisation"
    cycles_scolaires = ['préscolaire', 'primaire', 'secondaire 1er cycle', 'secondaire 2ème cycle']

    for annee in annees:
    
            for cycle in cycles_scolaires:
                data.append({
                    'indicateur': 'Taux de scolarisation',
                    'annee': annee,
                   
                    'cycle_scolaire': cycle,
                    'valeur': round(random.uniform(60, 100), 2)  # Taux entre 60% et 100%
                })
    #Nombre de commercant 
    for annee in annees:
        data.append({
            'indicateur': 'Nombre de commerçants',
            'annee': annee,
            'valeur': round(random.uniform(60, 100), 2)  # Taux entre 60% et 100%
        })


    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
