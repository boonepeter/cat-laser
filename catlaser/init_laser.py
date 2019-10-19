import math
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
    def __init__(self, x_pins, y_pins, laser_pin, height=100, speed=0.001):
        if (len(x_pins) != 4) or (len(y_pins) != 4):
            raise ValueError("Pin length not correct")
        self.Is_Laser_On = False
        self.height = height
        self.Laser_Pin = laser_pin
        self.X_Pins = x_pins
        self.Y_Pins = y_pins
        self.Seq_Ind_X = 0
        self.Seq_Ind_Y = 0
        self.Cur_Step_X = 0
        self.Cur_Step_Y = 0
        self.Max_Step_X = 508
        self.Min_Step_X = 0
        self.Max_Step_Y = 508
        self.Min_Step_Y = -508
        self.Stop_X = False
        self.Stop_Y = False
        GPIO.setmode(GPIO.BCM)
        for i in range(4):
            GPIO.setup(self.X_Pins[i], GPIO.OUT)
            GPIO.output(self.X_Pins[i], False)
            GPIO.setup(self.Y_Pins[i], GPIO.OUT)
            GPIO.output(self.Y_Pins[i], False)
        GPIO.setup(self.Laser_Pin, GPIO.OUT)
        GPIO.output(self.Laser_Pin, False)
        self.position = Point(0, 0)
        self.speed = speed
        self.seq = [[True,False,False,True],
                    [True,False,False,False],
                    [True,True,False,False],
                    [False,True,False,False],
                    [False,True,True,False],
                    [False,False,True,False],
                    [False,False,True,True],
                    [False,False,False,True]]
    
    def _MoveUp(self):
        self.Stop_Y = False
        while(not self.Stop_Y):
            self._MoveRelSteps(0, -5)
    def _Stop_Y(self):
        self.Stop_Y = True
    def _MoveDown(self):
        self.Stop_Y = False
        while(not self.Stop_Y):
            self._MoveRelSteps(0, 5)
    
    def Laser_On(self):
        GPIO.output(self.Laser_Pin, True)
        self.Is_Laser_On = True
    def Laser_Off(self):
        GPIO.output(self.Laser_Pin, False)
        self.Is_Laser_On = False
    def _GoAbsSteps(self, new_x, new_Y):
        change_X = new_x - self.Cur_Step_X
        change_Y = new_y - self.Cur_Step_Y
    def Move(self, X, Y):
        self._MoveRelSteps(X, Y)
        self.Cur_Step_X = X
        self.Cur_Step_Y = Y
    def MoveAbsolute(self, X, Y):
        dif_x = X - self.position.X
        dif_y = Y - self.position.Y
        self.position.X = X
        self.position.Y = Y
        self.MoveRelative(dif_x, dif_y)
    def _MoveRelSteps(self, X, Y):
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
        countY = self.Seq_Ind_Y
        countX = self.Seq_Ind_X
        for i in range(bigrange):
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
            self.Seq_Ind_X = countX
            self.Seq_Ind_Y = countY
            print(countY)
            for j in range(4):
                if i < absX:
                    GPIO.output(self.X_Pins[j], self.seq[countX][j])
                if i < absY:
                    GPIO.output(self.Y_Pins[j], self.seq[countY][j])