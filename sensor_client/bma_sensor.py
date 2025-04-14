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