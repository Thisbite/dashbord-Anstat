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

// Données fictives pour le taux de natalité
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
      { year: 2019, natalite: 26 }, { year: 2017, natalite: 23 }, { year: 2018, natalite: 25 },
      { year: 2019, natalite: 26 }, { year: 2020, natalite: 24 }, { year: 2021, natalite: 27 },
      { year: 2022, natalite: 28 }, { year: 2023, natalite: 29 }
  ]
};

// Données fictives pour les effectifs médicaux
var dataMedical = [
  { "Nombre hôpital": 2, corps: "Infirmiers", Korhogo: 80, Sinematiali: 60, Dikodougou: 75, "M'bengué": 50 },
  { "Nombre hôpital": 1, corps: "Sage-femmes", Korhogo: 40, Sinematiali: 30, Dikodougou: 35, "M'bengué": 25 },
  { "Nombre hôpital": 2, corps: "Généralistes", Korhogo: 30, Sinematiali: 25, Dikodougou: 40, "M'bengué": 20 }
];
var labelsMedical = ["Korhogo", "Sinematiali", "Dikodougou", "M'bengué"];
var corpsMedical = ["Infirmiers", "Sage-femmes", "Généralistes"];

// Données fictives pour l’indice synthétique de fécondité (ISF)
var dataIDH = [
  { region: "2016", idh: 0.55 }, { region: "2020", idh: 0.72 },
  { region: "2022", idh: 0.60 }, { region: "2023", idh: 0.65 }
];

// Données fictives pour le taux de chômage
var dataTauxChomage = [
  { region: "2008", taux: 12 }, { region: "2010", taux: 8 },
  { region: "2018", taux: 10 }, { region: "2023", taux: 9 }
];

// Données fictives pour le taux brut de scolarisation
var dataTauxBrut = [
  { year: 2018, taux: 85 }, { year: 2019, taux: 87 }, { year: 2020, taux: 89 },
  { year: 2021, taux: 90 }, { year: 2022, taux: 92 }
];

// Données fictives pour le taux d’électrification
var dataTauxElect = [
  { year: 2018, taux: 60 }, { year: 2019, taux: 65 }, { year: 2020, taux: 70 },
  { year: 2021, taux: 75 }, { year: 2022, taux: 80 }
];

// Données fictives pour le taux d’alphabétisation
var dataAlphabetisationPoro = [
  { year: "2016", taux: 45 }, { year: "2017", taux: 48 }, { year: "2018", taux: 50 },
  { year: "2019", taux: 52 }, { year: "2020", taux: 55 }, { year: "2021", taux: 58 },
  { year: "2022", taux: 60 }, { year: "2023", taux: 62 }
];

// Données fictives pour la population urbaine vs rurale
var dataPopRuralUrbain = {
  labels: ["Urbaine", "Rurale"],
  datasets: [{
      label: "Répartition Population 2023 (Poro)",
      data: [150000, 250000],
      backgroundColor: ['#49655A', '#F39323'],
      hoverBackgroundColor: ['#3a4e45', '#e08500'],
      borderColor: '#ffffff',
      borderWidth: 2
  }]
};

// Données fictives pour la population par département et par sexe
var dataPopulation = [
  { departement: "Korhogo", hommes: 60000, femmes: 60000 },
  { departement: "Sinematiali", hommes: 45000, femmes: 50000 },
  { departement: "Dikodougou", hommes: 55000, femmes: 55000 },
  { departement: "M'bengué", hommes: 40000, femmes: 45000 }
];

// Thème commun simplifié pour Chart.js
const chartTheme = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
      legend: {
          position: 'top',
          labels: {
              font: {
                  size: 12,
                  family: "'Montserrat', sans-serif",
                  weight: '600'
              },
              color: '#49655A',
              padding: 10
          }
      },
      tooltip: {
          backgroundColor: 'rgba(73, 101, 90, 0.9)',
          titleFont: { size: 14, family: "'Montserrat', sans-serif" },
          bodyFont: { size: 12, family: "'Montserrat', sans-serif" },
          cornerRadius: 6,
          padding: 10,
          borderColor: '#F39323',
          borderWidth: 1
      }
  },
  scales: {
      x: {
          ticks: {
              color: '#49655A',
              font: { size: 11, family: "'Montserrat', sans-serif" }
          },
          grid: { display: false },
          title: {
              display: true,
              color: '#49655A',
              font: { size: 12, family: "'Montserrat', sans-serif", weight: '600' }
          }
      },
      y: {
          ticks: {
              color: '#49655A',
              font: { size: 11, family: "'Montserrat', sans-serif" }
          },
          grid: { color: 'rgba(73, 101, 90, 0.2)', borderDash: [5, 5] },
          title: {
              display: true,
              color: '#49655A',
              font: { size: 12, family: "'Montserrat', sans-serif", weight: '600' }
          }
      }
  }
};

// Fonction pour ajuster les tailles de police sur mobile
function adjustChartFontSizes(chart) {
  if (!chart || !chart.options) return;

  const isMobile = window.innerWidth <= 768;
  const sizes = {
      legend: isMobile ? 10 : 12,
      ticks: isMobile ? 9 : 11,
      title: isMobile ? 10 : 12
  };

  // Mise à jour des tailles seulement si les propriétés existent
  if (chart.options.plugins.legend?.labels?.font) {
      chart.options.plugins.legend.labels.font.size = sizes.legend;
  }
  if (chart.options.scales.x?.ticks?.font) {
      chart.options.scales.x.ticks.font.size = sizes.ticks;
  }
  if (chart.options.scales.y?.ticks?.font) {
      chart.options.scales.y.ticks.font.size = sizes.ticks;
  }
  if (chart.options.scales.x?.title?.font) {
      chart.options.scales.x.title.font.size = sizes.title;
  }
  if (chart.options.scales.y?.title?.font) {
      chart.options.scales.y.title.font.size = sizes.title;
  }
  chart.update();
}

// Fonction pour créer un graphique avec vérification
function createChart(elementId, config) {
  const ctx = document.getElementById(elementId);
  if (!ctx) {
      console.error(`Élément HTML avec l'ID "${elementId}" non trouvé.`);
      return null;
  }
  if (typeof Chart === 'undefined') {
      console.error("Chart.js n'est pas chargé correctement.");
      return null;
  }
  const chart = new Chart(ctx.getContext("2d"), config);
  if (chart) {
      window.addEventListener('resize', () => adjustChartFontSizes(chart));
      adjustChartFontSizes(chart);
  }
  return chart;
}

// Graphique : Ratio élèves/enseignant
createChart("pyramideAgesChart", {
  type: 'line',
  data: {
      labels: dataRatioEleveEnseignant.Sinematiali.map(d => d.year),
      datasets: [
          { label: "Sinematiali", data: dataRatioEleveEnseignant.Sinematiali.map(d => d.ratio), borderColor: '#F39323', backgroundColor: 'rgba(243, 147, 35, 0.2)', fill: true, tension: 0.4, pointBackgroundColor: '#F39323' },
          { label: "Korhogo", data: dataRatioEleveEnseignant.Korhogo.map(d => d.ratio), borderColor: '#49655A', backgroundColor: 'rgba(73, 101, 90, 0.2)', fill: true, tension: 0.4, pointBackgroundColor: '#49655A' },
          { label: "M'bengué", data: dataRatioEleveEnseignant.Mbengue.map(d => d.ratio), borderColor: '#d9e6db', backgroundColor: 'rgba(217, 230, 219, 0.2)', fill: true, tension: 0.4, pointBackgroundColor: '#d9e6db' },
          { label: "Dikodougou", data: dataRatioEleveEnseignant.Dikodougou.map(d => d.ratio), borderColor: '#e08500', backgroundColor: 'rgba(224, 133, 0, 0.2)', fill: true, tension: 0.4, pointBackgroundColor: '#e08500' }
      ]
  },
  options: {
      ...chartTheme,
      scales: {
          x: { ...chartTheme.scales.x, title: { text: "Année" } },
          y: { ...chartTheme.scales.y, title: { text: "Ratio élèves/enseignant" }, min: 30, max: 55 }
      }
  }
});

// Graphique : Taux de natalité
createChart("tauxNataliteChart", {
  type: "line",
  data: {
      labels: dataNatalite.Sinematiali.map(d => d.year),
      datasets: [
          { label: "Sinematiali", data: dataNatalite.Sinematiali.map(d => d.natalite), borderColor: '#F39323', backgroundColor: 'rgba(243, 147, 35, 0.2)', fill: true, tension: 0.4, pointBackgroundColor: '#F39323' },
          { label: "Korhogo", data: dataNatalite.Korhogo.map(d => d.natalite), borderColor: '#49655A', backgroundColor: 'rgba(73, 101, 90, 0.2)', fill: true, tension: 0.4, pointBackgroundColor: '#49655A' },
          { label: "M'bengué", data: dataNatalite.Mbengue.map(d => d.natalite), borderColor: '#d9e6db', backgroundColor: 'rgba(217, 230, 219, 0.2)', fill: true, tension: 0.4, pointBackgroundColor: '#d9e6db' },
          { label: "Dikodougou", data: dataNatalite.Dikodougou.map(d => d.natalite), borderColor: '#e08500', backgroundColor: 'rgba(224, 133, 0, 0.2)', fill: true, tension: 0.4, pointBackgroundColor: '#e08500' }
      ]
  },
  options: {
      ...chartTheme,
      scales: {
          x: { ...chartTheme.scales.x, title: { text: "Année" } },
          y: { ...chartTheme.scales.y, title: { text: "Taux de natalité (‰)" }, beginAtZero: true }
      }
  }
});

// Graphique : Effectif médical
createChart("effectifMedical", {
  type: "bar",
  data: {
      labels: labelsMedical,
      datasets: corpsMedical.map((corps, index) => ({
          label: corps,
          data: labelsMedical.map(dept => dataMedical.find(d => d.corps === corps)[dept] || 0),
          backgroundColor: ['#49655A', '#F39323', '#d9e6db'][index],
          borderColor: '#ffffff',
          borderWidth: 1
      }))
  },
  options: {
      ...chartTheme,
      scales: {
          x: { ...chartTheme.scales.x, title: { text: "Départements" } },
          y: { ...chartTheme.scales.y, title: { text: "Effectif" }, beginAtZero: true, max: 100 }
      }
  }
});

// Graphique : Indice synthétique de fécondité (ISF)
createChart("idhChart", {
  type: "line",
  data: {
      labels: dataIDH.map(d => d.region),
      datasets: [{
          label: "ISF",
          data: dataIDH.map(d => d.idh),
          borderColor: '#49655A',
          backgroundColor: 'rgba(73, 101, 90, 0.2)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#49655A'
      }]
  },
  options: {
      ...chartTheme,
      scales: {
          x: { ...chartTheme.scales.x, title: { text: "Année" } },
          y: { ...chartTheme.scales.y, title: { text: "Indice" }, beginAtZero: true, max: 1 }
      }
  }
});

// Graphique : Taux de chômage
createChart("tauxChomageChart", {
  type: "line",
  data: {
      labels: dataTauxChomage.map(d => d.region),
      datasets: [{
          label: "Taux de chômage (%)",
          data: dataTauxChomage.map(d => d.taux),
          borderColor: '#F39323',
          backgroundColor: 'rgba(243, 147, 35, 0.2)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#F39323'
      }]
  },
  options: {
      ...chartTheme,
      scales: {
          x: { ...chartTheme.scales.x, title: { text: "Année" } },
          y: { ...chartTheme.scales.y, title: { text: "Taux (%)" }, beginAtZero: true, ticks: { stepSize: 2 } }
      }
  }
});

// Graphique : Taux brut de scolarisation
createChart("tauxBruteChart", {
  type: "line",
  data: {
      labels: dataTauxBrut.map(d => d.year),
      datasets: [{
          label: "Taux (%)",
          data: dataTauxBrut.map(d => d.taux),
          borderColor: '#F39323',
          backgroundColor: 'rgba(243, 147, 35, 0.2)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#F39323'
      }]
  },
  options: {
      ...chartTheme,
      scales: {
          x: { ...chartTheme.scales.x, title: { text: "Année" } },
          y: { ...chartTheme.scales.y, title: { text: "Taux (%)" }, beginAtZero: true }
      }
  }
});

// Graphique : Nombre de localités électrifiées
createChart("tauxElectChart", {
  type: "bar",
  data: {
      labels: dataTauxElect.map(d => d.year),
      datasets: [{
          label: "Nombre",
          data: dataTauxElect.map(d => d.taux),
          backgroundColor: '#49655A',
          borderColor: '#3a4e45',
          borderWidth: 1
      }]
  },
  options: {
      ...chartTheme,
      scales: {
          x: { ...chartTheme.scales.x, title: { text: "Année" } },
          y: { ...chartTheme.scales.y, title: { text: "Nombre" }, beginAtZero: true }
      }
  }
});

// Graphique : Taux d’alphabétisation
createChart("alphabetisationChartPoro", {
  type: "bar",
  data: {
      labels: dataAlphabetisationPoro.map(d => d.year),
      datasets: [{
          label: "Taux d'Alphabétisation (%)",
          data: dataAlphabetisationPoro.map(d => d.taux),
          backgroundColor: '#49655A',
          borderColor: '#3a4e45',
          borderWidth: 1
      }]
  },
  options: {
      ...chartTheme,
      scales: {
          x: { ...chartTheme.scales.x, title: { text: "Année" } },
          y: { ...chartTheme.scales.y, title: { text: "Taux (%)" }, beginAtZero: true }
      },
      plugins: {
          ...chartTheme.plugins,
          tooltip: {
              callbacks: {
                  label: function (tooltipItem) {
                      return `Taux : ${tooltipItem.raw}%`;
                  }
              }
          }
      }
  }
});

// Graphique : Population urbaine vs rurale
createChart("popRuralUrbain", {
  type: "doughnut",
  data: dataPopRuralUrbain,
  options: {
      ...chartTheme,
      plugins: {
          ...chartTheme.plugins,
          legend: {
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
                              hidden: !chart.getDataVisibility(i),
                              index: i
                          };
                      });
                  }
              }
          },
          tooltip: {
              callbacks: {
                  label: function (tooltipItem) {
                      const label = tooltipItem.label || "";
                      const value = tooltipItem.raw;
                      const total = tooltipItem.dataset.data.reduce((acc, val) => acc + val, 0);
                      const percentage = ((value / total) * 100).toFixed(1);
                      return `${label}: ${value.toLocaleString()} habitants (${percentage}%)`;
                  }
              }
          }
      }
  }
});

// Tableau : Population par département
const tableauPop = document.getElementById("tableauPop");
if (tableauPop) {
  const headersRow = tableauPop.querySelector("thead tr");
  if (headersRow) {
      headersRow.innerHTML = '<th>Département</th><th>Hommes</th><th>Femmes</th><th>Total</th>';
  }
  const tbody = tableauPop.querySelector("tbody");
  if (tbody) {
      dataPopulation.forEach(d => {
          const row = document.createElement("tr");
          row.innerHTML = `<td>${d.departement}</td><td>${d.hommes.toLocaleString()}</td><td>${d.femmes.toLocaleString()}</td><td>${(d.hommes + d.femmes).toLocaleString()}</td>`;
          tbody.appendChild(row);
      });
  }
} else {
  console.error("Tableau avec l'ID 'tableauPop' non trouvé.");
}

// Fonction pour afficher/masquer la section publication
function showPublicationFunction(event) {
  event.preventDefault();
  const publicationSection = document.getElementById('connexion');
  const dashboardSection = document.getElementById('dashbordId');
  if (publicationSection && dashboardSection) {
      if (publicationSection.style.display === "none" || publicationSection.style.display === "") {
          publicationSection.style.display = "block";
          dashboardSection.style.display = 'none';
      } else {
          publicationSection.style.display = "none";
      }
  } else {
      console.error("Section 'connexion' ou 'dashbordId' non trouvée.");
  }
}