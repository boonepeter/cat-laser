from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice('/dev/input/event0')
print(gamepad)

<<<<<<< HEAD
for event in gamepad.read_loop()
    print(event)
=======
for event in gamepad.read_loop():
>>>>>>> d91c61e2b26787f117d040adcb70833f3cb23c7a
    print(categorize(event))
