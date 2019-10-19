from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice('/dev/input/event0')
print(gamepad)

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        if event.code == 296:
            print("select")
        elif event.code == 297:
            print("start")
        elif event.code == 291:
            print("Y")
        elif event.code == 288:
            print("X")
        elif event.code == 290:
            print("B")
        elif event.code == 289:
            print("A")
        elif event.code == 293:
            print("R Trig")
        elif event.code == 292:
            print("L Trig")
        else:
            print("unknown")
    elif event.type == ecodes.EV_ABS:
        if event.code == 0:
            print("X")
        elif event.code == 1:
            print("Y")
        else:
            print("Unknown")