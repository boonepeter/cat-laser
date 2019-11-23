import RPi.GPIO as GPIO
import time

y_servo = 19
x_servo = 18

class Motors():
    def __init__(self, xpin, ypin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(xpin, GPIO.OUT)
        GPIO.setup(ypin, GPIO.OUT)
        self.x = GPIO.PWM(xpin, 50)
        self.y = GPIO.PWM(ypin, 50)
        self.x.start(0)
        self.y.start(0)
    def Move(self, percent):
        self.x.ChangeDutyCycle(percent)
        self.y.ChangeDutyCycle(percent)


motor = Motors(x_servo, y_servo)
for i in range(10):
    motor.Move(i * 10)
    time.sleep(1)