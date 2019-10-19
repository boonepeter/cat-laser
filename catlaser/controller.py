import init_laser as laser
from evdev import InputDevice, categorize, ecodes

XPins = [12, 25, 24, 23]
YPins = [4, 17, 27, 22]

Laser_Pin = 16
testlaser = laser.Laser(XPins, YPins, Laser_Pin, 0.01)


testlaser.Laser_On()
testlaser.Laser_Off()

gamepad = InputDevice('/dev/input/event0')
print(gamepad)


up = False
down = False
left = False
right = False
while True:
    if up:
        testlaser._MoveRelSteps(0, 5)
    elif down:
        testlaser._MoveRelSteps(0, -5)
    if left:
        testlaser._MoveRelSteps(-5, 0)
    elif right:
        testlaser._MoveRelSteps(5, 0)

    try:
        events = gamepad.read()
        for event in events:
            if event.type == ecodes.EV_KEY:
                if event.code == 296: # SELECT
                    if event.value == 1:
                        if testlaser.Is_Laser_On:
                            testlaser.Laser_Off()
                        else:
                            testlaser.Laser_On()
                elif event.code == 297: #START
                    print("start")
                elif event.code == 291: # Y button
                    print("Y")
                elif event.code == 288: # X button
                    print("X")
                elif event.code == 290: # B button
                    print("B")
                elif event.code == 289: # A button
                    print("A")
                elif event.code == 293: # Right Trigger
                    print("R Trig")
                elif event.code == 292: # Left trigger
                    print("L Trig")
                else:
                    print("unknown button")
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
                else:
                    print("Unknown direction")
    except BlockingIOError:
        #do nothing
        pass