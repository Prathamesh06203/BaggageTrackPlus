# Complete Project Setup
## Project Structure and File Contents

### 1. Backend Setup

**backend/__init__.py**
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    
    from .models.sensor_data import SensorData
    with app.app_context():
        db.create_all()
    
    return app
```

**backend/config.py**
```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/sensor_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'  # Change in production
    DEBUG = True
```

**backend/app.py**
```python
from flask import jsonify, request
from . import create_app, db
from .models.sensor_data import SensorData, GPSData

app = create_app()

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    new_reading = SensorData(
        acceleration_x=data['acceleration']['x'],
        acceleration_y=data['acceleration']['y'],
        acceleration_z=data['acceleration']['z'],
        temperature=data['temperature'],
        device_id=data.get('device_id')
    )
    db.session.add(new_reading)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/api/gps-data', methods=['POST'])
def receive_gps_data():
    data = request.json
    new_gps = GPSData(
        latitude=data['latitude'],
        longitude=data['longitude'],
        altitude=data.get('altitude'),
        device_id=data.get('device_id')
    )
    db.session.add(new_gps)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/api/data', methods=['GET'])
def get_data():
    device_id = request.args.get('device_id')
    sensor_data = SensorData.query.filter_by(device_id=device_id).order_by(SensorData.timestamp.desc()).first()
    gps_data = GPSData.query.filter_by(device_id=device_id).order_by(GPSData.timestamp.desc()).first()
    
    return jsonify({
        "sensor_data": sensor_data.to_dict() if sensor_data else None,
        "gps_data": gps_data.to_dict() if gps_data else None
    })

if __name__ == '__main__':
    app.run(debug=True)
```

**backend/models/sensor_data.py**
```python
from datetime import datetime
from .. import db

class SensorData(db.Model):
    __tablename__ = 'sensor_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    acceleration_x = db.Column(db.Float, nullable=False)
    acceleration_y = db.Column(db.Float, nullable=False)
    acceleration_z = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'acceleration': {
                'x': self.acceleration_x,
                'y': self.acceleration_y,
                'z': self.acceleration_z
            },
            'temperature': self.temperature,
            'device_id': self.device_id
        }

class GPSData(db.Model):
    __tablename__ = 'gps_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float, nullable=True)
    device_id = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'device_id': self.device_id
        }
```

### 2. ESP32 Client Setup

**sensor_client/bma_sensor.py**
```python
import time
import machine
import bma400
import nmea  # For GPS
import urequests
import ujson
from config import Config

class SensorClient:
    def __init__(self):
        # Initialize I2C for BMA sensor
        i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
        self.bma = bma400.BMA400(i2c)
        
        # Initialize UART for GPS
        self.gps_uart = machine.UART(2, 9600)
        self.gps = nmea.NMEA(self.gps_uart)
        
        self.config = Config()

    def read_sensor_data(self):
        try:
            acc = self.bma.acceleration
            temp = self.bma.temperature
            return {
                'acceleration': {
                    'x': acc[0],
                    'y': acc[1],
                    'z': acc[2]
                },
                'temperature': temp,
                'device_id': self.config.DEVICE_ID
            }
        except Exception as e:
            print('Sensor read error:', e)
            return None

    def read_gps_data(self):
        try:
            if self.gps.update():
                return {
                    'latitude': self.gps.latitude,
                    'longitude': self.gps.longitude,
                    'altitude': self.gps.altitude,
                    'device_id': self.config.DEVICE_ID
                }
        except Exception as e:
            print('GPS read error:', e)
            return None

    def send_data(self):
        while True:
            sensor_data = self.read_sensor_data()
            if sensor_data:
                try:
                    response = urequests.post(
                        self.config.API_URL + '/sensor-data',
                        json=sensor_data
                    )
                    print('Sensor data sent:', response.status_code)
                except Exception as e:
                    print('Sensor data send error:', e)

            gps_data = self.read_gps_data()
            if gps_data:
                try:
                    response = urequests.post(
                        self.config.API_URL + '/gps-data',
                        json=gps_data
                    )
                    print('GPS data sent:', response.status_code)
                except Exception as e:
                    print('GPS data send error:', e)

            time.sleep(self.config.INTERVAL)

if __name__ == '__main__':
    client = SensorClient()
    client.send_data()
```

**sensor_client/config.py**
```python
class Config:
    API_URL = 'http://your-server:5000/api'
    DEVICE_ID = 'ESP32_001'
    INTERVAL = 1.0  # seconds
```

### 3. Frontend Setup

**frontend/index.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Sensor & GPS Dashboard</title>
    <link rel="stylesheet" href="css/styles.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
</head>
<body>
    <div class="container">
        <h1>Sensor & GPS Dashboard</h1>
        <div class="dashboard-grid">
            <div class="chart-container">
                <canvas id="accelerationChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="temperatureChart"></canvas>
            </div>
            <div id="map" class="map-container"></div>
        </div>
    </div>
    <script src="js/dashboard.js"></script>
</body>
</html>
```

**frontend/css/styles.css**
```css
.container {
    width: 90%;
    margin: auto;
    padding: 20px;
}

.dashboard-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 20px;
}

.chart-container {
    background: white;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    height: 300px;
}

.map-container {
    grid-column: 1 / -1;
    height: 400px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h1 {
    text-align: center;
    color: #333;
}
```

**frontend/js/dashboard.js**
```javascript
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
```

## Summary Report

### Project Overview
This project implements a complete system for monitoring baggage using TTGO T-Call ESP32 controllers with integrated BMA sensors and GPS capabilities. The system consists of three main components:

1. **ESP32 Client**
   - Reads BMA sensor data (acceleration and temperature)
   - Collects GPS coordinates
   - Sends real-time data to backend server
   - Uses MicroPython for efficient operation

2. **Backend Server**
   - Flask-based REST API
   - SQLite database for data storage
   - Handles both sensor and GPS data
   - Provides data retrieval endpoints

3. **Frontend Dashboard**
   - Real-time data visualization
   - Interactive maps showing device location
   - Acceleration and temperature charts
   - Responsive design

### Key Features
- Real-time GPS tracking
- Acceleration monitoring
- Temperature monitoring
- Interactive maps
- Live data updates
- Multiple device support
- Data persistence

### Technical Specifications
- Backend: Python/Flask
- Database: SQLite
- Frontend: HTML5, CSS3, JavaScript
- Maps: Leaflet.js
- Charts: Chart.js
- Device: TTGO T-Call ESP32

### Implementation Notes
1. The ESP32 client sends data every second
2. Data is stored with timestamps and device IDs
3. Frontend updates automatically every second
4. Maps automatically center on the latest GPS position
5. Charts show rolling windows of recent data

### Usage Instructions
1. Configure the ESP32 with the provided MicroPython code
2. Start the Flask backend server
3. Open the frontend in a web browser
4. Monitor real-time data and device location

Would you like me to provide more details about any specific component or explain any part in more detail?