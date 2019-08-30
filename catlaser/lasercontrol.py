import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)

for i in range(50):
    GPIO.output(2, True)
    time.sleep(0.5)
    GPIO.output(2, False)
    time.sleep(0.25)
