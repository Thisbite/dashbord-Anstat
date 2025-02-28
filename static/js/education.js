// Données fictives pour le ratio élèves/enseignant (élèves par enseignant) de 2019 à 2024
var dataRatioEleveEnseignant = {
  Sinematiali: [
    { year: 2019, ratio: 45 }, { year: 2020, ratio: 43 }, { year: 2021, ratio: 42 },
    { year: 2022, ratio: 41 }, { year: 2023, ratio: 40 }, { year: 2024, ratio: 39 }
  ],
  Korhogo: [
    { year: 2019, ratio: 50 }, { year: 2020, ratio: 49 }, { year: 2021, ratio: 48 },
    { year: 2022, ratio: 47 }, { year: 2023, ratio: 46 }, { year: 2024, ratio: 45 }
  ],
  Mbengue: [
    { year: 2019, ratio: 38 }, { year: 2020, ratio: 37 }, { year: 2021, ratio: 36 },
    { year: 2022, ratio: 35 }, { year: 2023, ratio: 34 }, { year: 2024, ratio: 33 }
  ],
  Dikodougou: [
    { year: 2019, ratio: 42 }, { year: 2020, ratio: 41 }, { year: 2021, ratio: 40 },
    { year: 2022, ratio: 39 }, { year: 2023, ratio: 38 }, { year: 2024, ratio: 37 }
  ]
};

// Configuration du graphique
var ctx1 = document.getElementById("pyramideAgesChart").getContext("2d");
new Chart(ctx1, {
  type: "line", // Changement de "bar" à "line" pour un graphique linéaire
  data: {
    labels: dataRatioEleveEnseignant.Sinematiali.map(d => d.year), // Années sur l'axe X
    datasets: [
      {
        label: "Sinematiali",
        data: dataRatioEleveEnseignant.Sinematiali.map(d => d.ratio),
        borderColor: "orange",
        backgroundColor: "rgba(255,165,0,0.2)",
        fill: false
      },
      {
        label: "Korhogo",
        data: dataRatioEleveEnseignant.Korhogo.map(d => d.ratio),
        borderColor: "blue",
        backgroundColor:  "white",
        fill: false
      },
      {
        label: "M'bengué",
        data: dataRatioEleveEnseignant.Mbengue.map(d => d.ratio),
        borderColor: "green",
        backgroundColor:  "white",
        fill: false
      },
      {
        label: "Dikodougou",
        data: dataRatioEleveEnseignant.Dikodougou.map(d => d.ratio),
        borderColor: "red",
        backgroundColor: "white",
        fill: false
      }
    ]
  },
  options: {
    scales: {
      x: { title: { display: true, text: "Année" } },
      y: { 
        beginAtZero: false, // Pas besoin de commencer à 0, les ratios sont généralement > 0
        min: 30, // Ajuste selon tes données
        max: 55, // Ajuste selon tes données
        title: { display: true, text: "Ratio élèves/enseignant" }
      }
    },
    plugins: {
      legend: { display: true } // Affiche la légende pour identifier les départements
    }
  }
});

// Données générées pour les quatre départements (taux de natalité en ‰)
var dataNatalite = {
  Sinematiali: [
    { year: 2013, natalite: 20 }, { year: 2014, natalite: 22 }, { year: 2015, natalite: 18 },
    { year: 2016, natalite: 21 }, { year: 2017, natalite: 19 }, { year: 2018, natalite: 24 },
    { year: 2019, natalite: 23 }, { year: 2020, natalite: 22 }, { year: 2021, natalite: 25 },
    { year: 2022, natalite: 26 }, { year: 2023, natalite: 27 }
  ],
  Korhogo: [
    { year: 2013, natalite: 25 }, { year: 2014, natalite: 26 }, { year: 2015, natalite: 24 },
    { year: 2016, natalite: 23 }, { year: 2017, natalite: 25 }, { year: 2018, natalite: 27 },
    { year: 2019, natalite: 28 }, { year: 2020, natalite: 26 }, { year: 2021, natalite: 29 },
    { year: 2022, natalite: 30 }, { year: 2023, natalite: 31 }
  ],
  Mbengue: [
    { year: 2013, natalite: 18 }, { year: 2014, natalite: 19 }, { year: 2015, natalite: 17 },
    { year: 2016, natalite: 20 }, { year: 2017, natalite: 21 }, { year: 2018, natalite: 22 },
    { year: 2019, natalite: 23 }, { year: 2020, natalite: 21 }, { year: 2021, natalite: 24 },
    { year: 2022, natalite: 25 }, { year: 2023, natalite: 26 }
  ],
  Dikodougou: [
    { year: 2013, natalite: 22 }, { year: 2014, natalite: 23 }, { year: 2015, natalite: 20 },
    { year: 2016, natalite: 24 }, { year: 2017, natalite: 23 }, { year: 2018, natalite: 25 },
    { year: 2019, natalite: 26 }, { year: 2020, natalite: 24 }, { year: 2021, natalite: 27 },
    { year: 2022, natalite: 28 }, { year: 2023, natalite: 29 }
  ]
};

// Configuration du graphique, taux de natalité
var ctx2 = document.getElementById("tauxNataliteChart").getContext("2d");
new Chart(ctx2, {
  type: "line",
  data: {
    labels: dataNatalite.Sinematiali.map(d => d.year), // Les années sont les mêmes pour tous
    datasets: [
      {
        label: "Sinematiali",
        data: dataNatalite.Sinematiali.map(d => d.natalite),
        borderColor: "orange",
        backgroundColor: "rgba(255,165,0,0.2)",
        fill: false // Désactive le remplissage sous la courbe
      },
      {
        label: "Korhogo",
        data: dataNatalite.Korhogo.map(d => d.natalite),
        borderColor: "blue",
        backgroundColor: "rgba(0,0,255,0.2)",
        fill: false
      },
      {
        label: "M'bengué",
        data: dataNatalite.Mbengue.map(d => d.natalite),
        borderColor: "green",
        backgroundColor: "rgba(0,255,0,0.2)",
        fill: false
      },
      {
        label: "Dikodougou",
        data: dataNatalite.Dikodougou.map(d => d.natalite),
        borderColor: "red",
        backgroundColor: "rgba(255,0,0,0.2)",
        fill: false
      }
    ]
  },
  options: {
    scales: {
      x: { title: { display: true, text: "Année" } },
      y: { 
        beginAtZero: true,
        title: { display: true, text: "Taux de natalité (‰)" }
      }
    },
    plugins: {
      legend: { display: true } // Affiche la légende pour identifier les courbes
    }
  }
});

// Taux brut de scolarité
var dataTauxBrut = [
  { year: 2013, taux: 85 },
  { year: 2014, taux: 87 },
  { year: 2015, taux: 89 },
  { year: 2016, taux: 90 },
  { year: 2017, taux: 88 },
  { year: 2018, taux: 92 },
  { year: 2019, taux: 94 },
  { year: 2020, taux: 91 },
  { year: 2021, taux: 93 },
  { year: 2022, taux: 95 },
  { year: 2023, taux: 96 },
];


// Données fictives pour la population par département et par sexe
// Données fictives pour la population par département et par sexe
var dataPopulation = [
  { departement: "Korhogo", hommes: 60000, femmes: 60000 },
  { departement: "Sinematiali", hommes: 45000, femmes: 50000 },
  { departement: "Dikodougou", hommes: 55000, femmes: 55000 },
  { departement: "M'bengué", hommes: 40000, femmes: 45000 },
];

// Sélectionner le tableau
var tableauPop = document.getElementById("tableauPop");
var headersRow = tableauPop.querySelector("thead tr"); // Ligne d'en-têtes

// Ajouter les colonnes pour les modalités de sexe et le total
var thHommes = document.createElement("th");
thHommes.textContent = "Hommes";
headersRow.appendChild(thHommes);

var thFemmes = document.createElement("th");
thFemmes.textContent = "Femmes";
headersRow.appendChild(thFemmes);

var thTotal = document.createElement("th");
thTotal.textContent = "Total";
headersRow.appendChild(thTotal);

// Ajouter les lignes des départements et les données correspondantes
var tbody = tableauPop.querySelector("tbody");
dataPopulation.forEach(function(d) {
    var row = document.createElement("tr");

    // Ajouter le nom du département
    var tdDepartement = document.createElement("td");
    tdDepartement.textContent = d.departement;
    row.appendChild(tdDepartement);

    // Ajouter les effectifs pour les hommes
    var tdHommes = document.createElement("td");
    tdHommes.textContent = d.hommes;
    row.appendChild(tdHommes);

    // Ajouter les effectifs pour les femmes
    var tdFemmes = document.createElement("td");
    tdFemmes.textContent = d.femmes;
    row.appendChild(tdFemmes);

    // Ajouter le total
    var tdTotal = document.createElement("td");
    tdTotal.textContent = d.hommes + d.femmes;
    row.appendChild(tdTotal);

    // Ajouter la ligne au tableau
    tbody.appendChild(row);
});


// Données fictives pour les effectifs médicaux
var dataMedical = [
  { "Nombre hôpital":2,corps: "Infirmiers", Korhogo: 80, Sinematiali: 60, Dikodougou: 75, "M'bengué": 50 },
  { "Nombre hôpital":1,corps: "Sage-femmes", Korhogo: 40, Sinematiali: 30, Dikodougou: 35, "M'bengué": 25 },
  { "Nombre hôpital":2,corps: "Généralistes", Korhogo: 30, Sinematiali: 25, Dikodougou: 40, "M'bengué": 20 },
];
// Extraire les départements et corps médicaux
var labelsMedical = ["Korhogo", "Sinematiali", "Dikodougou", "M'bengué"];
var corpsMedical = ["Infirmiers", "Sage-femmes", "Généralistes"];

// Configuration du graphe pour les effectifs médicaux
var ctxMedical = document.getElementById("effectifMedical").getContext("2d");

new Chart(ctxMedical, {
  type: "bar",
  data: {
    labels: labelsMedical,
    datasets: corpsMedical.map((corps, index) => ({
      label: corps,
      data: labelsMedical.map(departement => {
        var corpsData = dataMedical.find(d => d.corps === corps);
        return corpsData ? corpsData[departement] : 0; // Retourne 0 si aucune donnée trouvée
      }),
      backgroundColor: ["#e09705", "#006B45", "white","#ddd"][index],
      borderColor: "#000",
      borderWidth: 1,
    })),
  },
  options: {
    scales: {
      x: { beginAtZero: true },
      y: { beginAtZero: true, max: 100 },
    },
  },
});




var dataIDH = [
  { region: "2016", idh: 0.55 },
  { region: "2020", idh: 0.72 },
  { region: "2022", idh: 0.60 },
  { region: "2023", idh: 0.65 },
];


var ctxIDH = document.getElementById("idhChart").getContext("2d");
new Chart(ctxIDH, {
  type: "line",
  data: {
    labels: dataIDH.map(d => d.region),
    datasets: [
      {
        label: "ISF(%)",
        data: dataIDH.map(d => d.idh),
        borderColor: "green",
        fill: false,
      },
    ],
  },
  options: {
    scales: {
      y: { beginAtZero: true, max: 1 },
    },
  },
});




var dataTauxChomage = [
  { region: "2008", taux: 12 },
  { region: "2010", taux: 8 },
  { region: "2018", taux: 10 },
  { region: "2023", taux: 9 },
];

var ctxTauxChomage = document.getElementById("tauxChomageChart").getContext("2d");
new Chart(ctxTauxChomage, {
  type: "line",
  data: {
    labels: dataTauxChomage.map(d => d.region),
    datasets: [
      {
        label: "Taux",
        data: dataTauxChomage.map(d => d.taux),
        borderColor: "#e09705", // Couleur de la ligne
        fill: false, // Pas de remplissage sous la courbe
        pointBackgroundColor: "#e09705", // Couleur des points
        pointBorderColor: "#e09705", // Bordure des points
      },
    ],
  },
  options: {
    scales: {
      y: {
        beginAtZero: true, // L'axe Y commence à zéro
        ticks: {
          stepSize: 2, // Intervalle entre les graduations
        },
        title: {
          display: true,
          text: "Taux (%)",
        },
      },
      x: {
        title: {
          display: true,
          text: "Régions",
        },
      },
    },
    plugins: {
      legend: {
        display: true, // Affiche la légende
        position: "top",
      },
    },
  },
});

var dataPopulationPoro = {
  labels: ["Urbaine", "Rurale"],
  datasets: [
    {
      label: "Répartition Population 2022 (Poro)",
      data: [150000, 250000], // Exemple de données
      backgroundColor: ["#4CAF50", "#FFC107"], // Couleurs pour les segments
      hoverBackgroundColor: ["#388E3C", "#FFA000"], // Couleurs au survol
    },
  ],
};

// Initialisation du graphique
var ctxPopRuralUrbain = document.getElementById("popRuralUrbain").getContext("2d");
new Chart(ctxPopRuralUrbain, {
  type: "doughnut",
  data: dataPopulationPoro,
  options: {
    responsive: true,
    plugins: {
     legend: {
        display: true,
        position: "top",
        labels: {
          generateLabels: function (chart) {
            const data = chart.data;
            const total = data.datasets[0].data.reduce((acc, val) => acc + val, 0);
            return data.labels.map((label, i) => {
              const value = data.datasets[0].data[i];
              const percentage = ((value / total) * 100).toFixed(1);
              return {
                text: `${label} (${percentage}%)`,
                fillStyle: data.datasets[0].backgroundColor[i],
                hidden: chart.isDatasetVisible(0) && !chart.getDataVisibility(i),
                lineWidth: 0,
                index: i,
              };
            });
          },
        },
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            let label = tooltipItem.label || "";
            let value = tooltipItem.raw;
            
            // Calculer le pourcentage total
            const dataset = tooltipItem.dataset;
            const total = dataset.data.reduce((acc, val) => acc + val, 0);
            const percentage = ((value / total) * 100).toFixed(1); // Pourcentage avec 1 décimale
            
            return `${label}: ${value.toLocaleString()} habitants (${percentage}%)`;
          },
        },
      },
    },
  },
});



var dataAlphabetisationPoro = {
  labels: ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"], // Années
  datasets: [
    {
      label: "Taux d'Alphabétisation (%)",
      data: [45, 48, 50, 52, 55, 58, 60, 62], // Exemple de données
      backgroundColor: "#4CAF50", // Couleur des barres
      borderColor: "#388E3C", // Couleur de bordure des barres
      borderWidth: 1,
    },
  ],
};

// Initialisation du graphique
var ctxAlphabetisationPoro = document
  .getElementById("alphabetisationChartPoro")
  .getContext("2d");
new Chart(ctxAlphabetisationPoro, {
  type: "bar",
  data: dataAlphabetisationPoro,
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: true,
        position: "top",
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            let value = tooltipItem.raw;
            return `Taux : ${value}%`;
          },
        },
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Année",
        },
      },
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: "Taux d'Alphabétisation (%)",
        },
      },
    },
  },
});



function showPublicationFunction(event) {
  event.preventDefault();  // Empêche le comportement par défaut

  var publicationSection = document.getElementById('connexion');
  var dashboardSection = document.getElementById('dashbordId');

  // Masquer ou afficher la section Publication
  if (publicationSection.style.display === "none" || publicationSection.style.display === "") {
      publicationSection.style.display = "block";
      dashboardSection.style.display = 'none';
  } else {
      publicationSection.style.display = "none";
  }
}


// Données fictives pour Taux brut de scolarité
var tauxBruteData = {
  labels: ['2018', '2019', '2020', '2021', '2022'],
  datasets: [{
      label: 'Taux (%)',
      data: [85, 87, 89, 90, 92],
      backgroundColor: '#e09705',
      borderColor: '#e09705',
      borderWidth: 2
  }]
};

// Configuration du graphique pour Taux brut de scolarité
var tauxBruteConfig = {
  type: 'line',
  data: tauxBruteData,
  options: {
      responsive: true,
      plugins: {
          legend: {
              position: 'top',
          }
      }
  }
};

// Création du graphique pour Taux brut de scolarité
var tauxBruteChart = new Chart(
  document.getElementById('tauxBruteChart'),
  tauxBruteConfig
);

// Données fictives pour Taux d'électrification
var tauxElectData = {
  labels: ['2018', '2019', '2020', '2021', '2022'],
  datasets: [{
      label: 'Nombre',
      data: [60, 65, 70, 75, 80],
      backgroundColor: '#006B45',
      borderColor: '#006B45',
      borderWidth: 1
  }]
};

// Configuration du graphique pour Taux d'électrification
var tauxElectConfig = {
  type: 'bar',
  data: tauxElectData,
  options: {
      responsive: true,
      plugins: {
          legend: {
              position: 'top',
          }
      }
  }
};

// Création du graphique pour Taux d'électrification
var tauxElectChart = new Chart(
  document.getElementById('tauxElectChart'),
  tauxElectConfig
);

// Pour la carte région***********************************************************************************





