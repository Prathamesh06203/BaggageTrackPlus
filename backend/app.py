from flask import jsonify, request
from backend import create_app, db
from backend.models.sensor_data import SensorData, GPSData
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