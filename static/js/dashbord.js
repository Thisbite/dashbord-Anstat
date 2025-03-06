// Navigation entre sections
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault();

        // Désactiver les liens actifs précédents
        document.querySelectorAll('.nav-link').forEach(item => item.classList.remove('active'));
        this.classList.add('active');

        // Masquer toutes les sections
        document.querySelectorAll('.section').forEach(section => {
            if (section) section.classList.add('d-none');
        });

        // Afficher la section correspondante
        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        if (targetSection) targetSection.classList.remove('d-none');
    });
});

// Initialisation des graphiques avec Chart.js
const chartData = [
    {
        id: 'chart1',
        labels: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin'],
        data: [12, 19, 3, 5, 2, 3],
        color: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)'
    },
    {
        id: 'chart2',
        labels: ['Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
        data: [7, 11, 5, 8, 3, 7],
        color: 'rgba(153, 102, 255, 0.2)',
        borderColor: 'rgba(153, 102, 255, 1)'
    },
    {
        id: 'chart3',
        labels: ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'],
        data: [9, 6, 4, 7, 10],
        color: 'rgba(255, 159, 64, 0.2)',
        borderColor: 'rgba(255, 159, 64, 1)'
    }
];

// Création des graphiques dynamiquement
chartData.forEach(chart => {
    const ctx = document.getElementById(chart.id);
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chart.labels,
                datasets: [{
                    label: 'Données mensuelles',
                    data: chart.data,
                    backgroundColor: chart.color,
                    borderColor: chart.borderColor,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        enabled: true
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
});
