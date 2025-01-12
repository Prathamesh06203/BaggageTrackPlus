let accelerationChart, temperatureChart, map, marker;
const DEVICE_ID = 'ESP32_001';

function initCharts() {
    // Initialize acceleration chart
    const accCtx = document.getElementById('accelerationChart').getContext('2d');
    accelerationChart = new Chart(accCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                { label: 'X', data: [], borderColor: 'red' },
                { label: 'Y', data: [], borderColor: 'blue' },
                { label: 'Z', data: [], borderColor: 'green' }
            ]
        }
    });

    // Initialize temperature chart
    const tempCtx = document.getElementById('temperatureChart').getContext('2d');
    temperatureChart = new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Temperature',
                data: [],
                borderColor: 'orange'
            }]
        }
    });
}

function initMap() {
    map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    marker = L.marker([0, 0]).addTo(map);
}

function updateData() {
    fetch(`http://localhost:5000/api/data?device_id=${DEVICE_ID}`)
        .then(response => response.json())
        .then(data => {
            if (data.sensor_data) {
                updateSensorCharts(data.sensor_data);
            }
            if (data.gps_data) {
                updateGPSMap(data.gps_data);
            }
        });
}

function updateSensorCharts(data) {
    const timestamp = new Date(data.timestamp).toLocaleTimeString();

    accelerationChart.data.labels.push(timestamp);
    accelerationChart.data.datasets[0].data.push(data.acceleration.x);
    accelerationChart.data.datasets[1].data.push(data.acceleration.y);
    accelerationChart.data.datasets[2].data.push(data.acceleration.z);
    accelerationChart.update();

    temperatureChart.data.labels.push(timestamp);
    temperatureChart.data.datasets[0].data.push(data.temperature);
    temperatureChart.update();
}

function updateGPSMap(data) {
    const position = [data.latitude, data.longitude];
    marker.setLatLng(position);
    map.setView(position, 15);
}

// Initialize everything
initCharts();
initMap();
setInterval(updateData, 1000);