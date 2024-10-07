document.addEventListener('DOMContentLoaded', function () {
    let dataSourceChart;
    let currentSource = 'data_source_1';
    let currentTimeRange = 30;
    let historicalData;

    async function fetchHistoricalData(source, days) {
        // Replace with the actual URL to fetch the data
        const response = await fetch(`/api/data-source/${source}/?days=${days}`);
        const data = await response.json();
        return data;
    }

    function createDataSourceChart(data) {
        const ctx = document.getElementById('dataSourceChart').getContext('2d');
        if (dataSourceChart) {
            dataSourceChart.destroy();
        }
        dataSourceChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.date),
                datasets: [{
                    label: `Data for ${currentSource}`,
                    data: data.map(d => d.value),
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                }
            }
        });
    }

    function updateStatsDisplay(data) {
        const statsDiv = document.getElementById('stats');
        const latestValue = data[data.length - 1].value;
        const earliestValue = data[0].value;
        const valueChange = ((latestValue - earliestValue) / earliestValue) * 100;

        statsDiv.innerHTML = `
            <h3>Statistics for ${currentSource} (Last ${currentTimeRange} days):</h3>
            <p>Current Value: ${latestValue.toFixed(2)}</p>
            <p>Value Change: ${valueChange.toFixed(2)}%</p>
        `;
    }

    async function updateCharts() {
        try {
            historicalData = await fetchHistoricalData(currentSource, currentTimeRange);
            createDataSourceChart(historicalData);
            updateStatsDisplay(historicalData);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            currentSource = e.target.dataset.symbol;
            updateCharts();
        });
    });

    document.getElementById('timeRange').addEventListener('change', (e) => {
        currentTimeRange = e.target.value;
        updateCharts();
    });

    document.getElementById('refreshBtn').addEventListener('click', updateCharts);

    // Initial update
    updateCharts();
});
