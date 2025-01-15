from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask import send_from_directory



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    acceleration_x = db.Column(db.Float, nullable=False)
    acceleration_y = db.Column(db.Float, nullable=False)
    acceleration_z = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.String(50), nullable=False)

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
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Float, nullable=True)
    device_id = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'device_id': self.device_id
        }

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.json
    try:
        new_reading = SensorData(
            acceleration_x=data['acceleration']['x'],
            acceleration_y=data['acceleration']['y'],
            acceleration_z=data['acceleration']['z'],
            temperature=data['temperature'],
            device_id=data['device_id']
        )
        db.session.add(new_reading)
        db.session.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/gps-data', methods=['POST'])
def receive_gps_data():
    data = request.json
    try:
        new_gps = GPSData(
            latitude=data['latitude'],
            longitude=data['longitude'],
            altitude=data.get('altitude'),
            device_id=data['device_id']
        )
        db.session.add(new_gps)
        db.session.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/data', methods=['GET'])
def get_data():
    device_id = request.args.get('device_id')
    sensor_data = SensorData.query.filter_by(device_id=device_id).order_by(SensorData.timestamp.desc()).first()
    gps_data = GPSData.query.filter_by(device_id=device_id).order_by(GPSData.timestamp.desc()).first()
    return jsonify({
        "sensor_data": sensor_data.to_dict() if sensor_data else None,
        "gps_data": gps_data.to_dict() if gps_data else None
    })

@app.route('/api/sensor-data/history', methods=['GET'])
def get_sensor_data_history():
    device_id = request.args.get('device_id')
    limit = request.args.get('limit', 100, type=int)
    sensor_data_history = SensorData.query.filter_by(device_id=device_id).order_by(SensorData.timestamp.desc()).limit(limit).all()
    return jsonify([data.to_dict() for data in sensor_data_history])

@app.route('/api/gps-data/history', methods=['GET'])
def get_gps_data_history():
    device_id = request.args.get('device_id')
    limit = request.args.get('limit', 100, type=int)
    gps_data_history = GPSData.query.filter_by(device_id=device_id).order_by(GPSData.timestamp.desc()).limit(limit).all()
    return jsonify([data.to_dict() for data in gps_data_history])

@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
