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
    def Move_X(self, percent):
        self.x.ChangeDutyCycle(percent)
    def Move_Y(self, percent):
        self.y.ChangeDutyCycle(percent)
    def Close(self):
        self.x.stop()
        self.y.stop()
        GPIO.cleanup()     

motor = Motors(x_servo, y_servo)
time.sleep(1)
for i in range(10):
    motor.Move_X(i * 10)
    time.sleep(1)
for i in range(10):
    motor.Move_Y(i * 10)
    time.sleep(1)

motor.Close()