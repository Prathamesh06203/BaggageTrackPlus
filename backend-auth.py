# backend/auth.py
from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your-secret-key'  # Should be stored securely

def create_token(device_id):
    payload = {
        'device_id': device_id,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.device_id = payload['device_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
            
        return f(*args, **kwargs)
    
    return decorated

# Updated location routes with authentication
@app.route('/api/location', methods=['POST'])
@requires_auth
def add_location():
    data = request.json
    
    if request.device_id != data.get('device_id'):
        return jsonify({'message': 'Device ID mismatch'}), 403
    
    new_location = LocationData(
        device_id=data['device_id'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        battery_voltage=data.get('battery_voltage'),
        low_battery_mode=data.get('low_battery_mode', False)
    )
    
    db.session.add(new_location)
    db.session.commit()
    
    return jsonify(new_location.to_dict()), 201
