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
  
  // Thème commun pour Chart.js
  const chartTheme = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                font: { size: 12, family: "'Montserrat', sans-serif", weight: '600' },
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
            ticks: { color: '#49655A', font: { size: 11, family: "'Montserrat', sans-serif" } },
            grid: { display: false },
            title: { display: true, color: '#49655A', font: { size: 12, family: "'Montserrat', sans-serif", weight: '600' } }
        },
        y: {
            ticks: { color: '#49655A', font: { size: 11, family: "'Montserrat', sans-serif" } },
            grid: { color: 'rgba(73, 101, 90, 0.2)', borderDash: [5, 5] },
            title: { display: true, color: '#49655A', font: { size: 12, family: "'Montserrat', sans-serif", weight: '600' } }
        }
    },
    animation: {
        duration: 1000,
        easing: 'easeInOutQuad'
    }
  };
  
  // Fonction pour ajuster les tailles de police sur mobile
  function adjustChartFontSizes(chart) {
    if (window.innerWidth <= 768) {
        chart.options.plugins.legend.labels.font.size = 10;
        chart.options.scales.x.ticks.font.size = 9;
        chart.options.scales.y.ticks.font.size = 9;
        chart.options.scales.x.title.font.size = 10;
        chart.options.scales.y.title.font.size = 10;
    } else {
        chart.options.plugins.legend.labels.font.size = 12;
        chart.options.scales.x.ticks.font.size = 11;
        chart.options.scales.y.ticks.font.size = 11;
        chart.options.scales.x.title.font.size = 12;
        chart.options.scales.y.title.font.size = 12;
    }
    chart.update();
  }
  
  // Graphique : Ratio élèves/enseignant
  var ctx1 = document.getElementById("pyramideAgesChart").getContext("2d");
  const pyramideAgesChart = new Chart(ctx1, {
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
  window.addEventListener('resize', () => adjustChartFontSizes(pyramideAgesChart));
  adjustChartFontSizes(pyramideAgesChart);
  
  // Graphique : Taux de natalité
  var ctx2 = document.getElementById("tauxNataliteChart").getContext("2d");
  const tauxNataliteChart = new Chart(ctx2, {
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
  window.addEventListener('resize', () => adjustChartFontSizes(tauxNataliteChart));
  adjustChartFontSizes(tauxNataliteChart);
  
  // Graphique : Effectif médical
  var ctxMedical = document.getElementById("effectifMedical").getContext("2d");
  const effectifMedicalChart = new Chart(ctxMedical, {
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
  window.addEventListener('resize', () => adjustChartFontSizes(effectifMedicalChart));
  adjustChartFontSizes(effectifMedicalChart);
  
  // Graphique : Indice synthétique de fécondité (ISF)
  var ctxIDH = document.getElementById("idhChart").getContext("2d");
  const idhChart = new Chart(ctxIDH, {
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
  window.addEventListener('resize', () => adjustChartFontSizes(idhChart));
  adjustChartFontSizes(idhChart);
  
  // Graphique : Taux de chômage
  var ctxTauxChomage = document.getElementById("tauxChomageChart").getContext("2d");
  const tauxChomageChart = new Chart(ctxTauxChomage, {
    type: "line",
    data: {
        labels: dataTauxChomage.map(d => d.region),
        datasets: [{
            label: "Taux",
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
  window.addEventListener('resize', () => adjustChartFontSizes(tauxChomageChart));
  adjustChartFontSizes(tauxChomageChart);
  
  // Graphique : Population urbaine vs rurale
  var ctxPopRuralUrbain = document.getElementById("popRuralUrbain").getContext("2d");
  const popRuralUrbainChart = new Chart(ctxPopRuralUrbain, {
    type: "doughnut",
    data: {
        labels: ["Urbaine", "Rurale"],
        datasets: [{
            label: "Répartition Population 2023 (Poro)",
            data: [150000, 250000],
            backgroundColor: ['#49655A', '#F39323'],
            hoverBackgroundColor: ['#3a4e45', '#e08500'],
            borderColor: '#ffffff',
            borderWidth: 2
        }]
    },
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
  window.addEventListener('resize', () => adjustChartFontSizes(popRuralUrbainChart));
  adjustChartFontSizes(popRuralUrbainChart);
  
  // Graphique : Taux d'alphabétisation
  var ctxAlphabetisationPoro = document.getElementById("alphabetisationChartPoro").getContext("2d");
  const alphabetisationChartPoro = new Chart(ctxAlphabetisationPoro, {
    type: "bar",
    data: {
        labels: ["2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
        datasets: [{
            label: "Taux d'Alphabétisation (%)",
            data: [45, 48, 50, 52, 55, 58, 60, 62],
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
  window.addEventListener('resize', () => adjustChartFontSizes(alphabetisationChartPoro));
  adjustChartFontSizes(alphabetisationChartPoro);
  
  // Graphique : Taux brut de scolarité
  var tauxBruteChart = new Chart(document.getElementById('tauxBruteChart'), {
    type: 'line',
    data: {
        labels: ['2018', '2019', '2020', '2021', '2022'],
        datasets: [{
            label: "Taux (%)",
            data: [85, 87, 89, 90, 92],
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
  window.addEventListener('resize', () => adjustChartFontSizes(tauxBruteChart));
  adjustChartFontSizes(tauxBruteChart);
  
  // Graphique : Taux d'électrification
  var tauxElectChart = new Chart(document.getElementById('tauxElectChart'), {
    type: 'bar',
    data: {
        labels: ['2018', '2019', '2020', '2021', '2022'],
        datasets: [{
            label: "Nombre",
            data: [60, 65, 70, 75, 80],
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
  window.addEventListener('resize', () => adjustChartFontSizes(tauxElectChart));
  adjustChartFontSizes(tauxElectChart);
  
  // Tableau : Population par département
  var tableauPop = document.getElementById("tableauPop");
  var headersRow = tableauPop.querySelector("thead tr");
  var thHommes = document.createElement("th"); thHommes.textContent = "Hommes"; headersRow.appendChild(thHommes);
  var thFemmes = document.createElement("th"); thFemmes.textContent = "Femmes"; headersRow.appendChild(thFemmes);
  var thTotal = document.createElement("th"); thTotal.textContent = "Total"; headersRow.appendChild(thTotal);
  var tbody = tableauPop.querySelector("tbody");
  dataPopulation.forEach(d => {
    var row = document.createElement("tr");
    row.innerHTML = `<td>${d.departement}</td><td>${d.hommes.toLocaleString()}</td><td>${d.femmes.toLocaleString()}</td><td>${(d.hommes + d.femmes).toLocaleString()}</td>`;
    tbody.appendChild(row);
  });
  
  // Fonction pour afficher/masquer la section publication
  function showPublicationFunction(event) {
    event.preventDefault();
    var publicationSection = document.getElementById('connexion');
    var dashboardSection = document.getElementById('dashbordId');
    if (publicationSection.style.display === "none" || publicationSection.style.display === "") {
        publicationSection.style.display = "block";
        dashboardSection.style.display = 'none';
    } else {
        publicationSection.style.display = "none";
    }
  }