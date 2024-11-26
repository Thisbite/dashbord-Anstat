document.addEventListener("DOMContentLoaded", function () {
    const chartElement = document.getElementById("chartBar");
    const chartData = JSON.parse(chartElement.dataset.chart);

    // Bar Chart
    const ctxBar = chartElement.getContext("2d");
    new Chart(ctxBar, {
        type: "bar",
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                legend: { display: true },
                tooltip: { enabled: true },
            },
        },
    });

    // Pie Chart
    const ctxPie = document.getElementById("chartPie").getContext("2d");
    new Chart(ctxPie, {
        type: "pie",
        data: {
            labels: chartData.labels,
            datasets: [
                {
                    data: chartData.datasets.map(ds => ds.data.reduce((a, b) => a + b, 0)),
                    backgroundColor: chartData.datasets.map(ds => ds.backgroundColor),
                },
            ],
        },
        options: {
            responsive: true,
        },
    });
});