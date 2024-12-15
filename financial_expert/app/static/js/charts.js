// static/js/charts.js
function createPortfolioChart(data) {
    const ctx = document.getElementById('portfolioChart');
    if (!ctx) {
        console.error('Canvas element not found');
        return;
    }

    try {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(item => item.label),
                datasets: [{
                    data: data.map(item => item.value),
                    backgroundColor: [
                        '#2563eb',  // Albastru
                        '#059669',  // Verde
                        '#d97706',  // Portocaliu
                        '#8b5cf6',  // Violet
                        '#db2777'   // Roz
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: {
                                size: 14
                            },
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.raw}%`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true
                }
            }
        });
    } catch (error) {
        console.error('Error creating chart:', error);
    }
}