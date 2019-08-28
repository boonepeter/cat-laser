import sys
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

XPins = [2, 3, 4, 17]
YPins = [10, 9, 11, 5]

for pin in XPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
for pin in YPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]

stepcount = len(Seq)

def GoRelative(X, Y, speed=0.005):
    try:
        absX = abs(X)
        absY = abs(Y)
        if (X < 0):
            xdir = -1
        else:
            xdir = 1
        if (Y < 0):
            ydir = -1
        else:
            ydir = 1
        if absX >= absY:
            bigrange = absX
        else:
            bigrange = absY
        countY = 0
        countX = 0
        for i in range(bigrange):
            for j in range(4):
                if i < absX:
                    GPIO.output(XPins[j], Seq[countX][j] == 1)
                if i < absY:
                    GPIO.output(YPins[j], Seq[countY][j] == 1)
            time.sleep(speed)
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
            GPIO.output(XPins[i], False)
            GPIO.output(YPins[i], False)
    except KeyboardInterrupt:
        for i in range(4):
            GPIO.output(XPins[i], False)
            GPIO.output(YPins[i], False)
        raise


def Move(direction):
    direction = direction.upper()
    if (direction == "A") or (direction == "D"):
        pins = [10, 9, 11, 5]
        ran = 100
    elif (direction == "W") or (direction == "S"):
        pins = [2, 3, 4, 17]
        ran = 40
    else:
        return
    if (direction == "D") or (direction == "W"):
        direc = 1
    elif (direction == "A") or (direction == "S"):
        direc = -1

    counter = 0
    for i in range(ran):
        for i in range(4):
            if Seq[counter][i] != 0:
                GPIO.output(pins[i], True)
            else:
                GPIO.output(pins[i], False)
        time.sleep(0.001)
        counter += direc
        if counter < 0:
            counter = 7
        if counter > 7:
            counter = 0
    for pin in pins:
        GPIO.output(pin, False)

