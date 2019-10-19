import init_laser as laser
from evdev import InputDevice, categorize, ecodes

XPins = [12, 25, 24, 23]
YPins = [4, 17, 27, 22]

Laser_Pin = 16
testlaser = laser.Laser(XPins, YPins, Laser_Pin, 0.005)


testlaser.Laser_On()
testlaser.Laser_Off()




gamepad = InputDevice('/dev/input/event0')
print(gamepad)

for event in gamepad.read_loop():
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
                testlaser.Move(-10, 0)
            elif event.value == 255: #Right down
                testlaser.Move(10, 0)
        elif event.code == 1: #Y direction
            if event.value == 0: #up direction
                testlaser.Move(0, 10)
            elif event.value == 1: #down direction
                testlaser.Move(-10, 0)
        else:
            print("Unknown direction")