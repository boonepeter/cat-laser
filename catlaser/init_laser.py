import sys
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

class Point:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
    def __repr__(self):
        return f"{self.X},{self.Y}"

class Laser:
    def __init__(self, x_pins, y_pins, speed=0.001):
        if (len(x_pins) != 4) or (len(y_pins) != 4):
            raise ValueError("Pin length not correct")
        self.XPins = x_pins
        self.YPins = y_pins
        GPIO.setmode(GPIO.BCM)
        for i in range(4):
            GPIO.setup(self.XPins[i], GPIO.OUT)
            GPIO.output(self.XPins[i], False)
            GPIO.setup(self.YPins[i], GPIO.OUT)
            GPIO.output(self.YPins[i], False)
        self.position = Point(0, 0)
        self.speed = speed
        self.seq = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]

    def MoveAbsolute(self, X, Y):
        print(self.position.X)
        print(self.position.Y)
        dif_x = X - self.position.X
        dif_y = Y - self.position.Y
        self.position.X = X
        self.position.Y = Y
        self.MoveRelative(dif_x, dif_y)
    def MoveRelative(self, X, Y):
        print(X)
        print(Y)
        absX = abs(X)
        absY = abs(Y)
        xdir = 1
        ydir = 1
        if (X < 0):
            xdir = -1
        if (Y < 0):
            ydir = -1
        if absX >= absY:
            bigrange = absX
        else:
            bigrange = absY
        countY = 0
        countX = 0
        for i in range(bigrange):
            for j in range(4):
                if i < absX:
                    GPIO.output(self.XPins[j], self.seq[countX][j] == 1)
                if i < absY:
                    GPIO.output(self.YPins[j], self.seq[countY][j] == 1)
            time.sleep(self.speed)
            countX += xdir
            countY += ydir
            if countX > 7:
                countX = 0
            elif countX == -1:
                countX = 7
            if countY > 7:
                countY = 0
            elif countY == -1:
                countY = 7
        for i in range(4):
            GPIO.output(self.XPins[i], False)
            GPIO.output(self.YPins[i], False)
