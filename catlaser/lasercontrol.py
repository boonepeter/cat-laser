import RPi.GPIO as GPIO

LASER_PIN = 2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LASER_PIN, GPIO.OUT)


def On():
    GPIO.output(LASER_PIN, True)

def Off():
    GPIO.output(LASER_PIN, False)

