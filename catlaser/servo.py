import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pin_one = 17
pin_two = 27
GPIO.setup(pin_one, GPIO.OUT)
tilt_y = GPIO.PWN(pin_one, 50)
tilt_y = start(0)
tilt_y.ChangeDutyCycle(2)
tilt_y.ChangeDutyCycle(5)
tilt_y = stop()
GPIO.cleanup()
