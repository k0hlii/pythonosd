import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

def button_callback(channel):
    print("Button was pushed!")

GPIO.setwarnings(True) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

try:
    GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(8, GPIO.RISING, callback=button_callback)
    GPIO.add_event_detect(12, GPIO.RISING, callback=button_callback)
    GPIO.add_event_detect(16, GPIO.RISING, callback=button_callback)
    GPIO.add_event_detect(18, GPIO.RISING, callback=button_callback)
    message = input("Press enter to quit\n\n")
finally:
    GPIO.cleanup()

