# backend/models/location.py
from datetime import datetime
from . import db

class LocationData(db.Model):
    __tablename__ = 'location_data'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_id': self.device_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp.isoformat()
        }

# backend/routes/location.py
from flask import Blueprint, request, jsonify
from ..models.location import LocationData, db

location_bp = Blueprint('location', __name__)

@location_bp.route('/location', methods=['POST'])
def add_location():
    data = request.json
    
    new_location = LocationData(
        device_id=data['device_id'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    
    db.session.add(new_location)
    db.session.commit()
    
    return jsonify(new_location.to_dict()), 201

@location_bp.route('/location/<device_id>', methods=['GET'])
def get_location(device_id):
    # Get latest location for device
    location = LocationData.query.filter_by(device_id=device_id)\
        .order_by(LocationData.timestamp.desc())\
        .first()
    
    if not location:
        return jsonify({'error': 'Device not found'}), 404
        
    return jsonify(location.to_dict())

@location_bp.route('/location/<device_id>/history', methods=['GET'])
def get_location_history(device_id):
    # Get location history with optional time range
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    limit = request.args.get('limit', 100, type=int)
    
    query = LocationData.query.filter_by(device_id=device_id)
    
    if start_time:
        query = query.filter(LocationData.timestamp >= start_time)
    if end_time:
        query = query.filter(LocationData.timestamp <= end_time)
        
    locations = query.order_by(LocationData.timestamp.desc())\
        .limit(limit).all()
        
    return jsonify([loc.to_dict() for loc in locations])
