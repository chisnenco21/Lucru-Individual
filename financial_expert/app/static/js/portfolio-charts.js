document.addEventListener('DOMContentLoaded', function() {
    // Grafic alocare active
    const allocationCtx = document.getElementById('allocationChart');
    if (allocationCtx) {
        new Chart(allocationCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(portfolioData.allocation),
                datasets: [{
                    data: Object.values(portfolioData.allocation),
                    backgroundColor: [
                        '#2563eb',  // Albastru - Acțiuni
                        '#059669',  // Verde - Obligațiuni
                        '#d97706',  // Portocaliu - Numerar
                        '#8b5cf6'   // Violet - Alternative
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Grafic evoluție portofoliu
    const performanceCtx = document.getElementById('performanceChart');
    if (performanceCtx) {
        new Chart(performanceCtx, {
            type: 'line',
            data: {
                labels: portfolioData.history.map(h => h.date),
                datasets: [{
                    label: 'Valoare Portofoliu',
                    data: portfolioData.history.map(h => h.value),
                    borderColor: '#2563eb',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString() + ' RON';
                            }
                        }
                    }
                }
            }
        });
    }
});