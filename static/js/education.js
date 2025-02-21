// Pyramide des âges
var dataPyramide1 = [
  { age: "25-29 ans", male: -50, female: 60 },
  { age: "20-24 ans", male: -100, female: 90 },
  { age: "15-19 ans", male: -120, female: 140 },
  { age: "10-14 ans", male: -180, female: 170 },
  { age: "5-9 ans", male: -150, female: 160 },
  { age: "0-4 ans", male: -200, female: 180 },

];

var ctx1 = document.getElementById("pyramideAgesChart").getContext("2d");
new Chart(ctx1, {
  type: "bar",
  data: {
      labels: dataPyramide1.map(d => d.age),
      datasets: [
          { label: "Hommes", data: dataPyramide1.map(d => d.male), backgroundColor: "#e09705" },
          { label: "Femmes", data: dataPyramide1.map(d => d.female), backgroundColor: "#006B45" },
      ],
  },
  options: {
      indexAxis: "y",
      scales: {
          x: { stacked: true, min: -250, max: 250 },
          y: { stacked: true },
      },
  },
});

// Taux de natalité
var dataNatalite = [
  { year: 2013, natalite: 20 },
  { year: 2014, natalite: 22 },
  { year: 2015, natalite: 18 },
  { year: 2016, natalite: 21 },
  { year: 2017, natalite: 19 },
  { year: 2018, natalite: 24 },
  { year: 2019, natalite: 23 },
  { year: 2020, natalite: 22 },
  { year: 2021, natalite: 25 },
  { year: 2022, natalite: 26 },
  { year: 2023, natalite: 27 },
];

var ctx2 = document.getElementById("tauxNataliteChart").getContext("2d");
new Chart(ctx2, {
  type: "line",
  data: {
      labels: dataNatalite.map(d => d.year),
      datasets: [
          {
              label: "Taux de natalité",
              data: dataNatalite.map(d => d.natalite),
              borderColor: "orange",
              backgroundColor: "rgba(255,165,0,0.2)",
              fill: true,
          },
      ],
  },
  options: {
      scales: {
          x: { type: "category", labels: dataNatalite.map(d => d.year) },
          y: { beginAtZero: true },
      },
  },
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
        label: "IDF",
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
        label: "Taux de Chômage (%)",
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
  labels: ["Population Urbaine", "Population Rurale"],
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
      },
      tooltip: {
        callbacks: {
          label: function (tooltipItem) {
            let label = tooltipItem.label || "";
            let value = tooltipItem.raw;
            return `${label}: ${value.toLocaleString()} habitants`;
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
      label: 'Taux brut de scolarité (%)',
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
      label: 'Taux d\'électrification (%)',
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





