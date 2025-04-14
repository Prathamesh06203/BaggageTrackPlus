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