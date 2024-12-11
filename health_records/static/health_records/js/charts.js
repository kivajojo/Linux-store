function initializeCharts(chartData) {
    // 血压趋势图
    new Chart(document.getElementById('bpChart'), {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [{
                label: '收缩压',
                data: chartData.blood_pressure.map(bp => bp.split('/')[0]),
                borderColor: '#FF6384',
                tension: 0.1
            }, {
                label: '舒张压',
                data: chartData.blood_pressure.map(bp => bp.split('/')[1]),
                borderColor: '#36A2EB',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
    
    // 初始化其他图表...
}

document.addEventListener('DOMContentLoaded', function() {
    // 获取图表数据
    const chartData = JSON.parse(document.getElementById('chartData').textContent);
    
    // 血压趋势图
    new Chart(document.getElementById('bpChart'), {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [
                {
                    label: '收缩压',
                    data: chartData.blood_pressure.systolic,
                    borderColor: '#FF6384',
                    tension: 0.1
                },
                {
                    label: '舒张压',
                    data: chartData.blood_pressure.diastolic,
                    borderColor: '#36A2EB',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });

    // 心率趋势图
    new Chart(document.getElementById('heartRateChart'), {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [{
                label: '心率',
                data: chartData.heart_rate,
                borderColor: '#4CAF50',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });

    // 血糖趋势图
    new Chart(document.getElementById('bloodSugarChart'), {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [{
                label: '血糖',
                data: chartData.blood_sugar,
                borderColor: '#FFA726',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });

    // 体重趋势图
    new Chart(document.getElementById('weightChart'), {
        type: 'line',
        data: {
            labels: chartData.dates,
            datasets: [{
                label: '体重',
                data: chartData.weight,
                borderColor: '#9C27B0',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
});
