import time
import adafruit_dht
import requests
import json
import RPi.GPIO as GPIO
import board
from osd import OSD
import queue
import threading
from flask import Flask, jsonify


API_ENDPOINT = "http://localhost:3000/api/sendHumTemp"

# Initialize DHT11 device, with data pin connected to GPIO4 (BCM numbering, corresponds to physical pin 7)
dht_device = adafruit_dht.DHT11(board.D4)  # Use board.D4 for correct pin object

data = {"temperature": None, "humidity": None}

# Create a queue
q = queue.Queue()

# Define callback function for button press
def button_callback(channel):
    print("Button was pushed!")

osd = OSD()
last_button_press = time.time()

def start(channel):
    global last_button_press
    last_button_press = time.time()
    if osd.started:
        osd.cycle_tabs()
    else:
        q.put('start')

def select(channel):
    global last_button_press
    last_button_press = time.time()
    osd.call_button()
    print("Select Button pressed")

def cycle_buttons_forward(channel):
    global last_button_press
    last_button_press = time.time()
    osd.cycle_buttons_forward()
    print("Cycle forward button pressed")

def cycle_buttons_backward(channel):
    global last_button_press
    last_button_press = time.time()
    osd.cycle_buttons_backward()
    print("Cycle backward button pressed")

# Setup the GPIO pin for button input (BCM numbering)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(14, GPIO.RISING, callback=start, bouncetime=200)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(18, GPIO.RISING, callback=select, bouncetime=200)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(23, GPIO.RISING, callback=cycle_buttons_forward, bouncetime=200)

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=cycle_buttons_backward, bouncetime=200)

# Add a short delay to ensure the setup is completed before adding event detection
time.sleep(1)

@app.route('/getTemperature', methods=['GET'])
def get_temperature():
    return jsonify({"temperature": data["temperature"]})

@app.route('/getHumidity', methods=['GET'])
def get_humidity():
    return jsonify({"humidity": data["humidity"]})

def flask_thread():
    app.run(host='0.0.0.0', port=5000)

# Start the Flask server in a separate thread
flask_thread = threading.Thread(target=flask_thread)
flask_thread.start()

def check_last_button_press():
    global last_button_press
    global osd
    while True:
        if osd.started:
            print(time.time() - last_button_press)
            if time.time() - last_button_press > 10:
                print("Stopping OSD")
                osd.stop()
        time.sleep(0.1)

# Start the button press checker thread
button_checker_thread = threading.Thread(target=check_last_button_press)
button_checker_thread.start()

try:
    while True:
        try:
            # Check if there's a message in the queue
            while not q.empty():
                message = q.get()
                if message == 'start':
                    osd.run()

            # Get temperature and humidity from DHT11 sensor
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity

            if temperature_c is not None and humidity is not None:
                data = {"humidity": humidity, "temperature": temperature_c}
                print("Temp: {:.1f} C Humidity: {}%".format(temperature_c, humidity))
            else:
                print("Failed to retrieve data from sensor")

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print("RuntimeError:", error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dht_device.exit()
            raise error

        time.sleep(5)

except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()