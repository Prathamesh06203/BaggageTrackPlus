# BMA Sensor Project Documentation
Created: January 8, 2025

## Table of Contents
1. Project Overview
2. System Requirements
3. Project Structure
4. Installation Steps
5. Code Implementation
6. Running the Project
7. Troubleshooting
8. References

## 1. Project Overview
This project implements a full-stack solution for collecting, storing, and visualizing BMA sensor data from baggage monitoring systems.

### Components:
- Sensor Client: Reads data from BMA sensor
- Backend Server: Stores and manages sensor data
- Frontend Dashboard: Visualizes sensor readings

## 2. System Requirements

### Hardware Requirements:
- BMA400 Sensor
- Development board with I2C support
- USB cable for programming

### Software Requirements:
- Python 3.8+
- Visual Studio Code
- Web browser (Chrome/Firefox recommended)
- Git (optional)

### Python Packages:
```
flask==2.0.1
flask-sqlalchemy==2.5.1
adafruit-circuitpython-bma400==1.1.0
requests==2.26.0
python-dotenv==0.19.0
```

## 3. Project Structure
```
bma_sensor_project/
│
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── sensor_data.py
│   ├── requirements.txt
│   └── instance/
│       └── sensor_data.db
│
├── sensor_client/
│   ├── __init__.py
│   ├── bma_sensor.py
│   ├── config.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── dashboard.js
│
└── README.md
```

## 4. Installation Steps

### Step 1: Set Up Project Structure
```bash
mkdir bma_sensor_project
cd bma_sensor_project
mkdir -p backend/models backend/instance sensor_client frontend/{css,js}
```

### Step 2: Install Dependencies
```bash
# Backend dependencies
cd backend
pip install flask flask-sqlalchemy python-dotenv requests

# Sensor client dependencies
cd ../sensor_client
pip install adafruit-circuitpython-bma400 requests python-dotenv
```

### Step 3: Hardware Connection
1. Connect BMA sensor to your device:
   - VCC → 3.3V
   - GND → Ground
   - SCL → SCL pin (GPIO 3)
   - SDA → SDA pin (GPIO 2)

## 5. Code Implementation

### Backend Server (app.py):
```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    acceleration_x = db.Column(db.Float, nullable=False)
    acceleration_y = db.Column(db.Float, nullable=False)
    acceleration_z = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    
    new_reading = SensorData(
        timestamp=datetime.fromisoformat(data['timestamp']),
        acceleration_x=data['acceleration']['x'],
        acceleration_y=data['acceleration']['y'],
        acceleration_z=data['acceleration']['z'],
        temperature=data['temperature']
    )
    
    db.session.add(new_reading)
    db.session.commit()
    
    return jsonify({"status": "success"})

@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    readings = SensorData.query.order_by(SensorData.timestamp.desc()).limit(100).all()
    
    data = [{
        'timestamp': reading.timestamp.isoformat(),
        'acceleration': {
            'x': reading.acceleration_x,
            'y': reading.acceleration_y,
            'z': reading.acceleration_z
        },
        'temperature': reading.temperature
    } for reading in readings]
    
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

### Sensor Client (bma_sensor.py):
```python
import time
import board
import busio
import adafruit_bma400
import requests
from datetime import datetime
import json

class BMASensor:
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bma400.BMA400_I2C(self.i2c)
        self.api_url = "http://localhost:5000/api/sensor-data"

    def read_data(self):
        try:
            x, y, z = self.sensor.acceleration
            temp = self.sensor.temperature
            
            data = {
                "timestamp": datetime.now().isoformat(),
                "acceleration": {
                    "x": round(x, 2),
                    "y": round(y, 2),
                    "z": round(z, 2)
                },
                "temperature": round(temp, 2)
            }
            return data
        except Exception as e:
            print(f"Error reading sensor: {e}")
            return None

    def send_data(self, data):
        try:
            response = requests.post(self.api_url, json=data)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending data: {e}")
            return False

    def start_monitoring(self, interval=1.0):
        print("Starting BMA sensor monitoring...")
        
        while True:
            data = self.read_data()
            if data:
                success = self.send_data(data)
                print(f"Data sent: {success}")
                print(f"Readings: {data}")
            time.sleep(interval)

if __name__ == "__main__":
    sensor = BMASensor()
    sensor.start_monitoring()
```

### Frontend Dashboard (index.html):
```html
<!DOCTYPE html>
<html>
<head>
    <title>BMA Sensor Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
    <style>
        .container {
            width: 80%;
            margin: auto;
            padding: 20px;
        }
        .chart-container {
            margin: 20px 0;
            height: 400px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BMA Sensor Dashboard</h1>
        <div class="chart-container">
            <canvas id="accelerationChart"></canvas>
        </div>
        <div class="chart-container">
            <canvas id="temperatureChart"></canvas>
        </div>
    </div>

    <script>
        let accelerationChart, temperatureChart;

        function initCharts() {
            const accCtx = document.getElementById('accelerationChart').getContext('2d');
            const tempCtx = document.getElementById('temperatureChart').getContext('2d');

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

        function updateCharts() {
            fetch('http://localhost:5000/api/sensor-data')
                .then(response => response.json())
                .then(data => {
                    const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString());
                    const accX = data.map(d => d.acceleration.x);
                    const accY = data.map(d => d.acceleration.y);
                    const accZ = data.map(d => d.acceleration.z);
                    const temps = data.map(d => d.temperature);

                    accelerationChart.data.labels = labels;
                    accelerationChart.data.datasets[0].data = accX;
                    accelerationChart.data.datasets[1].data = accY;
                    accelerationChart.data.datasets[2].data = accZ;
                    accelerationChart.update();

                    temperatureChart.data.labels = labels;
                    temperatureChart.data.datasets[0].data = temps;
                    temperatureChart.update();
                });
        }

        initCharts();
        setInterval(updateCharts, 1000);
    </script>
</body>
</html>
```

## 6. Running the Project

### Step 1: Start Backend Server
```bash
cd backend
python app.py
```

### Step 2: Start Sensor Client
```bash
cd sensor_client
python bma_sensor.py
```

### Step 3: Open Frontend Dashboard
Open `frontend/index.html` in your web browser

## 7. Troubleshooting

### Common Issues:
1. Sensor Connection Issues
   - Check I2C connections
   - Verify power supply
   - Check if I2C address is correct

2. Backend Server Issues
   - Verify Flask is running
   - Check database permissions
   - Ensure port 5000 is available

3. Frontend Issues
   - Check browser console for errors
   - Verify backend URL is correct
   - Ensure Chart.js is loading

## 8. References
- BMA400 Datasheet
- Flask Documentation
- Chart.js Documentation
- Adafruit CircuitPython BMA400 Library Documentation
