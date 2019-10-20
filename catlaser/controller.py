import init_laser as laser
import time
from evdev import InputDevice, categorize, ecodes

XPins = [12, 25, 24, 23]
YPins = [4, 17, 27, 22]

Laser_Pin = 16
testlaser = laser.Laser(XPins, YPins, Laser_Pin, 0.001)


#.. / .-.. --- ...- . / -.-- --- ..-
testlaser.PrintMorse("I love you!", 0.01)

print("Welcome to the cat laser toy!")
print("- D-pad: Move")
print("- B: Laser on/off")
print("- L/R bumper: fast mode")
print("- Start: sleep")

gamepad = InputDevice('/dev/input/event0')



up = False
down = False
left = False
right = False
to_break = False
l_trig = False
r_trig = False
while True:
    if to_break:
        testlaser.TurnOff()
        while to_break:
            time.sleep(0.5)
            try:
                events = gamepad.read()
                for event in events:
                    if event.type == ecodes.EV_KEY:
                        if event.code == 297: #START
                            if event.value == 1:
                                to_break = False
                                testlaser.PrintMorse("I love you!", 0.02)
                                testlaser.Laser_On()
            except BlockingIOError:
                #do nothing
                pass
    x = 0
    y = 0
    if up:
        y = 10
    elif down:
        y = -10
    if left:
        x = -10
    elif right:
        x = 10
    if (x != 0) or (y != 0):
        testlaser._MoveRelSteps(x, y)
    if l_trig or r_trig:
        testlaser.speed = 0.0005
    else:
        testlaser.speed = 0.001
    try:
        events = gamepad.read()
        for event in events:
            if event.type == ecodes.EV_KEY:
                if event.code == 296: # SELECT
                    #print("Select")
                    pass
                elif event.code == 297: #START
                    if event.value == 1:
                        to_break = True
                elif event.code == 291: # Y button
                    #print("Y")
                    pass
                elif event.code == 288: # X button
                    #print("X")
                    pass
                elif event.code == 290: # B button
                    if event.value == 1:
                        if testlaser.Is_Laser_On:
                            testlaser.Laser_Off()
                        else:
                            testlaser.Laser_On()                    
                elif event.code == 289: # A button
                    #print("A")
                    pass
                elif event.code == 293: # Right Trigger
                    if event.value == 1:
                        r_trig = True
                    elif event.value == 0:
                        r_trig = False
                elif event.code == 292: # Left trigger
                    if event.value == 1:
                        l_trig = True
                    elif event.value == 0:
                        l_trig = False
            elif event.type == ecodes.EV_ABS:
                if event.code == 0: # X direction
                    if event.value == 0: #Left down
                        left = True
                        right = False
                    if event.value == 127:
                        left = False
                        right = False
                    elif event.value == 255: #Right down
                        right = True
                        left = False
                elif event.code == 1: #Y direction
                    if event.value == 0: #up direction
                        down = True
                        up = False
                    elif event.value == 127:
                        up = False
                        down = False
                    elif event.value == 255: #down direction
                        down = False
                        up = True
    except BlockingIOError:
        #do nothing
        pass