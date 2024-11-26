const indicators = {
    Education: ['Taux de scolarisation', 'Nombre d’enseignants', 'Écoles construites', 'Diplômes obtenus', 'Taux de réussite', 'Dépenses en éducation', 'Matériel scolaire distribué'],
    Economie: ['PIB', 'Taux de chômage', 'Exportations', 'Importations', 'Investissements', 'Croissance économique', 'Inflation'],
};

function loadDashboard(theme) {
    const selectedIndicators = indicators[theme].slice(0, 5); // Les 5 premiers par défaut
    createCheckboxes(theme);
    generateCharts(selectedIndicators, theme);
}

function createCheckboxes(theme) {
    const checkboxContainer = document.getElementById('checkbox-container');
    checkboxContainer.innerHTML = ''; // Effacer les anciennes cases

    indicators[theme].forEach((indicator, index) => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `checkbox-${index}`;
        checkbox.value = indicator;
        checkbox.checked = index < 5; // Les 5 premiers cochés par défaut
        checkbox.addEventListener('change', () => updateCharts(theme));

        const label = document.createElement('label');
        label.htmlFor = `checkbox-${index}`;
        label.innerText = indicator;

        const div = document.createElement('div');
        div.appendChild(checkbox);
        div.appendChild(label);

        checkboxContainer.appendChild(div);
    });
}

function updateCharts(theme) {
    const checkedIndicators = Array.from(
        document.querySelectorAll('#checkbox-container input:checked')
    ).map(input => input.value);

    generateCharts(checkedIndicators, theme);
}

function generateCharts(selectedIndicators, theme) {
    // Effacer les anciens graphiques
    document.getElementById('charts').innerHTML = '';

    selectedIndicators.forEach((indicator, index) => {
        const chartContainer = document.createElement('div');
        chartContainer.style.marginBottom = '30px';

        const canvas = document.createElement('canvas');
        canvas.id = `chart-${index}`;
        chartContainer.appendChild(canvas);

        document.getElementById('charts').appendChild(chartContainer);

        // Exemple de données dynamiques
        const data = {
            labels: ['2012', '2013', '2014', '2015', '2016','2017','2018','2019','2020'],
            datasets: [{
                label: indicator,
                data: Array.from({ length: 9 }, () => Math.floor(Math.random() * 100)),
                backgroundColor: `rgba(${50 + index * 30}, ${150 + index * 20}, 200, 0.5)`,
                borderColor: `rgba(${50 + index * 30}, ${150 + index * 20}, 200, 1)`,
                borderWidth: 1,
            }]
        };
        //const chartType = index % 3 === 0 ? 'pie' : (index % 2 === 0 ? 'bar' : 'line'); // Alterne entre pie, bar, et line
        new Chart(canvas, {
            type: index % 2 === 0 ? 'bar' : 'line', // Alterner bar et line
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' },
                    title: { display: true, text: indicator }
                }
            }
        });
    });
}

// Initialisation avec le thème par défaut
loadDashboard('Education');


