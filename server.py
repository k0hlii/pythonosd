from flask import Flask, jsonify
from flask_cors import CORS
import requests
import base64
import adafruit_dht
import board

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

dht_device = adafruit_dht.DHT11(board.D4)  # Use board.D4 for correct pin object

@app.route('/getTemperature', methods=['GET'])
def get_temperature():
    temperature_c = dht_device.temperature
    # while temperature_c is None:
    #     temperature_c = dht_device.temperature
    return jsonify({"temperature": str(temperature_c)})

@app.route('/getHumidity', methods=['GET'])
def get_humidity():
    humidity = dht_device.humidity
    # while humidity is None:
    #     humidity = dht_device.humidity

    return jsonify({"humidity": str(humidity)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
