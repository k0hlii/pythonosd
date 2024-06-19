import time
import RPi.GPIO as GPIO
from osd import OSD
import queue
import threading

GPIO.setmode(GPIO.BCM)
q = queue.Queue()

osd = OSD()
last_button_press = time.time()

def start(channel):
    global last_button_press
    global osd
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

def check_last_button_press(q):
    global last_button_press
    global osd
    while True:
        if osd.started:
            print(time.time() - last_button_press)
            if time.time() - last_button_press > 5:
                osd.please_stop()
        time.sleep(1)

# Start the button press checker thread
button_checker_thread = threading.Thread(target=check_last_button_press, args=(q,))
button_checker_thread.start()

try:
    while True:
        try:
            while not q.empty():
                message = q.get()
                if message == 'start':
                    osd.run()

        except RuntimeError as error:
            print("RuntimeError:", error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            raise error

except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()