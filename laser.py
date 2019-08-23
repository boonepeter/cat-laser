from curtsies import Input, FullscreenWindow
import sys
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

Pins1 = [2, 3, 4, 17]
Pins2 = [10, 9, 11, 5]



for pin in Pins1:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

for pin in Pins2:
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

stepDir = -1
counter = 0

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


for pin in range(4):
    GPIO.output(Pins1[pin], False)
    GPIO.output(Pins2[pin], False)

with FullscreenWindow() as window:
    with Input() as in_gen:
        for e in in_gen:
            Move(e)
