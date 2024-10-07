// dashboard/static/js/scripts.js

document.addEventListener('DOMContentLoaded', function () {
    // Helper function to initialize or update a chart
    function initializeChart(chartId, config) {
        var canvas = document.getElementById(chartId);
        if (!canvas) {
            console.warn(`Canvas element with ID '${chartId}' not found.`);
            return;
        }
        var ctx = canvas.getContext('2d');
        // Destroy existing chart instance if it exists to prevent duplication
        if (Chart.getChart(ctx)) {
            Chart.getChart(ctx).destroy();
        }
        return new Chart(ctx, config);
    }

    // Sales by Product
    try {
        var salesByProductDataElement = document.getElementById('sales-by-product-data');
        if (salesByProductDataElement) {
            var salesByProductData = JSON.parse(salesByProductDataElement.textContent);
            var productLabels = salesByProductData.map(item => item.product__name);
            var productTotals = salesByProductData.map(item => Number(item.total));

            initializeChart('salesByProductChart', {
                type: 'bar',
                data: {
                    labels: productLabels,
                    datasets: [{
                        label: 'فروش به ریال',
                        data: productTotals,
                        backgroundColor: '#36a2eb'
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function (value) {
                                    return value.toLocaleString();
                                }
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error initializing Sales by Product Chart:', error);
    }

    // Sales by Category
    try {
        var salesByCategoryDataElement = document.getElementById('sales-by-category-data');
        if (salesByCategoryDataElement) {
            var salesByCategoryData = JSON.parse(salesByCategoryDataElement.textContent);
            var categoryLabels = salesByCategoryData.map(item => item.product__category);
            var categoryTotals = salesByCategoryData.map(item => Number(item.total));

            initializeChart('salesByCategoryChart', {
                type: 'pie',
                data: {
                    labels: categoryLabels,
                    datasets: [{
                        data: categoryTotals,
                        backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error initializing Sales by Category Chart:', error);
    }

    // Sales Over Time
    try {
        var salesOverTimeDataElement = document.getElementById('sales-over-time-data');
        if (salesOverTimeDataElement) {
            var salesOverTimeData = JSON.parse(salesOverTimeDataElement.textContent);
            var timeLabels = salesOverTimeData.map(item => item.month);
            var timeTotals = salesOverTimeData.map(item => Number(item.total));

            initializeChart('salesOverTimeChart', {
                type: 'line',
                data: {
                    labels: timeLabels,
                    datasets: [{
                        label: 'فروش به ریال',
                        data: timeTotals,
                        backgroundColor: '#36a2eb',
                        borderColor: '#36a2eb',
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'month',
                                tooltipFormat: 'yyyy-MM',
                                displayFormats: {
                                    month: 'yyyy-MM'
                                }
                            }
                        },
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function (value) {
                                    return value.toLocaleString();
                                }
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error initializing Sales Over Time Chart:', error);
    }

    // Sales per Branch
    try {
        var salesPerBranchDataElement = document.getElementById('sales-per-branch-data');
        if (salesPerBranchDataElement) {
            var salesPerBranchData = JSON.parse(salesPerBranchDataElement.textContent);
            var branchLabels = salesPerBranchData.map(item => item['branch_name'] || 'نامشخص');
            var branchTotals = salesPerBranchData.map(item => Number(item.total));

            initializeChart('salesPerBranchChart', {
                type: 'bar',
                data: {
                    labels: branchLabels,
                    datasets: [{
                        label: 'فروش به ریال',
                        data: branchTotals,
                        backgroundColor: '#4bc0c0'
                    }]
                },
                options: {
                    responsive: true,
                    indexAxis: 'y',
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: {
                                callback: function (value) {
                                    return value.toLocaleString();
                                }
                            }
                        }
                    }
                }
            });
        }
    } catch (error) {
        console.error('Error initializing Sales per Branch Chart:', error);
    }

    // Weekly Sales per Branch
    try {
        var salesPerBranchWeeklyDataElement = document.getElementById('sales-per-branch-weekly-data');
        if (salesPerBranchWeeklyDataElement) {
            var salesPerBranchWeeklyData = JSON.parse(salesPerBranchWeeklyDataElement.textContent);
            if (salesPerBranchWeeklyData.length > 0) {
                var weeklyBranchLabels = salesPerBranchWeeklyData.map(item => item['branch_name'] || 'نامشخص');
                var weeklyBranchTotals = salesPerBranchWeeklyData.map(item => Number(item.total));

                initializeChart('salesPerBranchWeeklyChart', {
                    type: 'bar',
                    data: {
                        labels: weeklyBranchLabels,
                        datasets: [{
                            label: 'فروش هفتگی به ریال',
                            data: weeklyBranchTotals,
                            backgroundColor: '#ff6384'
                        }]
                    },
                    options: {
                        responsive: true,
                        indexAxis: 'y',
                        scales: {
                            x: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function (value) {
                                        return value.toLocaleString();
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }
    } catch (error) {
        console.error('Error initializing Sales per Branch - Weekly Chart:', error);
    }

    // Monthly Sales per Branch
    try {
        var salesPerBranchMonthlyDataElement = document.getElementById('sales-per-branch-monthly-data');
        if (salesPerBranchMonthlyDataElement) {
            var salesPerBranchMonthlyData = JSON.parse(salesPerBranchMonthlyDataElement.textContent);
            if (salesPerBranchMonthlyData.length > 0) {
                var monthlyBranchLabels = salesPerBranchMonthlyData.map(item => item['branch_name'] || 'نامشخص');
                var monthlyBranchTotals = salesPerBranchMonthlyData.map(item => Number(item.total));

                initializeChart('salesPerBranchMonthlyChart', {
                    type: 'bar',
                    data: {
                        labels: monthlyBranchLabels,
                        datasets: [{
                            label: 'فروش ماهانه به ریال',
                            data: monthlyBranchTotals,
                            backgroundColor: '#36a2eb'
                        }]
                    },
                    options: {
                        responsive: true,
                        indexAxis: 'y',
                        scales: {
                            x: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function (value) {
                                        return value.toLocaleString();
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }
    } catch (error) {
        console.error('Error initializing Sales per Branch - Monthly Chart:', error);
    }
    // Sales by Country
try {
    var salesPerCountryDataElement = document.getElementById('sales-per-country-data');
    if (salesPerCountryDataElement) {
        var salesPerCountryData = JSON.parse(salesPerCountryDataElement.textContent);
        console.log('Sales per Country Data:', salesPerCountryData);

        var countryLabels = salesPerCountryData.map(item => item.country);
        var countryTotals = salesPerCountryData.map(item => Number(item.total));

        var salesPerCountryChart = initializeChart('salesPerCountryChart', {
            type: 'pie',
            data: {
                labels: countryLabels,
                datasets: [{
                    data: countryTotals,
                    backgroundColor: ['#ff6384', '#36a2eb', '#cc65fe', '#ffce56']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                family: 'Vazir',
                                size: 14,
                            }
                        }
                    }
                }
            }
        });
    } else {
        console.warn('Element with ID "sales-per-country-data" not found.');
    }
} catch (error) {
    console.error('Error initializing Sales by Country Chart:', error);
}

// Customers by Country
try {
    var customersPerCountryDataElement = document.getElementById('customers-per-country-data');
    if (customersPerCountryDataElement) {
        var customersPerCountryData = JSON.parse(customersPerCountryDataElement.textContent);
        console.log('Customers per Country Data:', customersPerCountryData);

        var countryLabels = customersPerCountryData.map(item => item.country);
        var countryCounts = customersPerCountryData.map(item => Number(item.count));

        var customersPerCountryChart = initializeChart('customersPerCountryChart', {
            type: 'pie',
            data: {
                labels: countryLabels,
                datasets: [{
                    data: countryCounts,
                    backgroundColor: ['#4bc0c0', '#ff9f40', '#9966ff', '#ffcd56']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                family: 'Vazir',
                                size: 14,
                            }
                        }
                    }
                }
            }
        });
    } else {
        console.warn('Element with ID "customers-per-country-data" not found.');
    }
} catch (error) {
    console.error('Error initializing Customers by Country Chart:', error);
}

    // Timeline Sales Chart
    try {
        var timelineSalesDataElement = document.getElementById('timeline-sales-data');
        if (timelineSalesDataElement) {
            var timelineSalesData = JSON.parse(timelineSalesDataElement.textContent);
            if (timelineSalesData.length > 0) {
                var timelineLabels = timelineSalesData.map(item => item.date || item.month);
                var timelineTotals = timelineSalesData.map(item => Number(item.total));

                initializeChart('timelineSalesChart', {
                    type: 'line',
                    data: {
                        labels: timelineLabels,
                        datasets: [{
                            label: 'فروش تایملاین به ریال',
                            data: timelineTotals,
                            backgroundColor: '#cc65fe',
                            borderColor: '#cc65fe',
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: {
                                type: 'time',
                                time: {
                                    unit: 'month',
                                    tooltipFormat: 'yyyy-MM-dd',
                                    displayFormats: {
                                        month: 'yyyy-MM'
                                    }
                                }
                            },
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function (value) {
                                        return value.toLocaleString();
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }
    } catch (error) {
        console.error('Error initializing Timeline Sales Chart:', error);
    }
});
