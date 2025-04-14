class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/sensor_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key'  # Change in production
    DEBUG = True