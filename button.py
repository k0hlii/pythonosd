import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from osd import OSD
import time

def button_callback(channel):
    print("Button was pushed!")

GPIO.setwarnings(True) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
osd = OSD()

def start(channel):
    global last_button_press
    last_button_press = time.time()
    print("adsfklja")
    if osd.started:
        osd.cycle_tabs()
    else:
        osd.run()

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

try:
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(8, GPIO.RISING, callback=start)
    GPIO.add_event_detect(12, GPIO.RISING, callback=select)
    GPIO.add_event_detect(16, GPIO.RISING, callback=cycle_buttons_forward)
    GPIO.add_event_detect(18, GPIO.RISING, callback=cycle_buttons_backward)
    message = input("Press enter to quit\n\n")
finally:
    GPIO.cleanup()

