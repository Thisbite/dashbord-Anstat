// **Pyramide des âges : données et graphique**
var dataPyramide1 = [
    { age: '0-4 ans', male: -200, female: 180 },
    { age: '5-9 ans', male: -150, female: 160 },
    { age: '10-14 ans', male: -180, female: 170 },
    { age: '15-19 ans', male: -120, female: 140 },
    { age: '20-24 ans', male: -100, female: 90 },
    { age: '25-29 ans', male: -50, female: 60 },
];

// Dimensions du graphique
// Dimensions du graphique
var widthPyramide = 400;
var heightPyramide = 200;
var marginPyramide = { top: 20, right: 30, bottom: 40, left: 50 };

// Création des échelles pour les axes
var xPyramide = d3
  .scaleLinear()
  .domain([-250, 250]) // Domaine symétrique pour les hommes (négatif) et les femmes
  .range([0, widthPyramide]);

var yPyramide = d3
  .scaleBand()
  .domain(dataPyramide1.map(d => d.age)) // Référence à dataPyramide1
  .range([0, heightPyramide])
  .padding(0.1);

// Création de la zone SVG principale
var svgPyramide = d3
  .select("#pyramide-ages")
  .append("svg")
  .attr("width", widthPyramide + marginPyramide.left + marginPyramide.right)
  .attr("height", heightPyramide + marginPyramide.top + marginPyramide.bottom)
  .append("g")
  .attr("transform", `translate(${marginPyramide.left}, ${marginPyramide.top})`);

// Ajout des barres pour les hommes
svgPyramide
  .selectAll(".bar-male")
  .data(dataPyramide1) // Référence à dataPyramide1
  .enter()
  .append("rect")
  .attr("class", "bar-male")
  .attr("x", d => xPyramide(d.male))
  .attr("y", d => yPyramide(d.age))
  .attr("width", d => xPyramide(0) - xPyramide(d.male))
  .attr("height", yPyramide.bandwidth())
  .attr("fill", "#e09705");

// Ajout des barres pour les femmes
svgPyramide
  .selectAll(".bar-female")
  .data(dataPyramide1) // Référence à dataPyramide1
  .enter()
  .append("rect")
  .attr("class", "bar-female")
  .attr("x", xPyramide(0))
  .attr("y", d => yPyramide(d.age))
  .attr("width", d => xPyramide(d.female) - xPyramide(0))
  .attr("height", yPyramide.bandwidth())
  .attr("fill", "#006B45");

// Ajout des axes
svgPyramide.append("g").call(d3.axisLeft(yPyramide));
svgPyramide
  .append("g")
  .attr("transform", `translate(0, ${heightPyramide})`)
  .call(d3.axisBottom(xPyramide));

// Données de la légende
var legendData = [
  { label: "Hommes (Men)", color: "#e09705" },
  { label: "Femmes (Women)", color: "#006B45" },
];

// Dimensions et marges de la légende
var legendMargin = { top: 10, right: 10, bottom: 10, left: 10 };
var legendWidth = widthPyramide - legendMargin.left - legendMargin.right;
var legendHeight = legendData.length * 20; // Hauteur ajustée en fonction des éléments

// Création de la zone SVG pour la légende
var legendSvg = d3
  .select("#pyramide-ages")
  .append("svg")
  .attr("class", "legend")
  .attr("width", legendWidth + legendMargin.left + legendMargin.right)
  .attr("height", legendHeight + legendMargin.top + legendMargin.bottom);

// Fonction pour dessiner les éléments de la légende
var drawLegendItem = function(g, data, index) {
  var gItem = g.append("g").attr("transform", `translate(0, ${index * 20})`);

  gItem
    .append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 10)
    .attr("height", 10)
    .attr("fill", data.color);

  gItem
    .append("text")
    .attr("x", 15)
    .attr("y", 9) // Alignement vertical avec le rectangle
    .text(data.label);
};

// Ajout des éléments de la légende
var legendGroup = legendSvg
  .append("g")
  .attr("transform", `translate(${legendMargin.left}, ${legendMargin.top})`);

legendData.forEach((data, index) => drawLegendItem(legendGroup, data, index));







// **Taux de natalité sur 10 ans**
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

// Dimensions du graphique
var widthNatalite = 400;
var heightNatalite = 200;
var marginNatalite = { top: 20, right: 30, bottom: 40, left: 50 };

// Création des échelles
var xNatalite = d3
    .scalePoint() // Utilisation de scalePoint pour mieux espacer les années
    .domain(dataNatalite.map(d => d.year))
    .range([0, widthNatalite])
    .padding(0.5);

var yNatalite = d3
    .scaleLinear()
    .domain([0, d3.max(dataNatalite, d => d.natalite)])
    .range([heightNatalite, 0]);

// Ajout de la zone SVG
var svgNatalite = d3
    .select("#taux-natalite")
    .append("svg")
    .attr("width", widthNatalite + marginNatalite.left + marginNatalite.right)
    .attr("height", heightNatalite + marginNatalite.top + marginNatalite.bottom)
    .append("g")
    .attr("transform", `translate(${marginNatalite.left}, ${marginNatalite.top})`);

// Ajout de la ligne
var line = d3
    .line()
    .x(d => xNatalite(d.year))
    .y(d => yNatalite(d.natalite));

svgNatalite
    .append("path")
    .datum(dataNatalite)
    .attr("fill", "none")
    .attr("stroke", "orange") // Couleur de la ligne
    .attr("stroke-width", 2)
    .attr("d", line);

// Ajout des cercles aux points de données
svgNatalite
    .selectAll(".point")
    .data(dataNatalite)
    .enter()
    .append("circle")
    .attr("class", "point")
    .attr("cx", d => xNatalite(d.year))
    .attr("cy", d => yNatalite(d.natalite))
    .attr("r", 4) // Taille des cercles
    .attr("fill", "orange");

// Ajout des axes
svgNatalite.append("g").call(d3.axisLeft(yNatalite));
svgNatalite
    .append("g")
    .attr("transform", `translate(0, ${heightNatalite})`)
    .call(d3.axisBottom(xNatalite));




// Données fictives pour le taux brut de scolarisation
var donnees = [
  { region: "Abidjan", taux: 85 },
  { region: "Bouaké", taux: 78 },
  { region: "Yamoussoukro", taux: 92 },
  { region: "San Pedro", taux: 75 },
  { region: "Korhogo", taux: 80 }
];

// Dimensions et marges
var marge = { top: 20, right: 30, bottom: 40, left: 50 };
var largeur = 500 - marge.left - marge.right;
var hauteur = 300 - marge.top - marge.bottom;

// Création du conteneur SVG
var svg = d3
    .select("#taux-brute")
    .append("svg")
    .attr("width", largeur + marge.left + marge.right)
    .attr("height", hauteur + marge.top + marge.bottom)
    .append("g")
    .attr("transform", `translate(${marge.left},${marge.top})`);

// Axes
var x = d3.scaleBand()
    .domain(donnees.map(d => d.region))
    .range([0, largeur])
    .padding(0.2);

var y = d3.scaleLinear()
    .domain([0, 100])
    .range([hauteur, 0]);

// Ajout de l'axe X
svg.append("g")
    .attr("transform", `translate(0,${hauteur})`)
    .call(d3.axisBottom(x))
    .selectAll("text")
    .attr("transform", "rotate(-25)")
    .style("text-anchor", "end");

// Ajout de l'axe Y
svg.append("g")
    .call(d3.axisLeft(y));

// Barres du diagramme
svg.selectAll("rect")
    .data(donnees)
    .enter()
    .append("rect")
    .attr("x", d => x(d.region))
    .attr("y", d => y(d.taux))
    .attr("width", x.bandwidth())
    .attr("height", d => hauteur - y(d.taux))
    .attr("fill", "skyblue");
