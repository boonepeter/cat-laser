import time
import paho.mqtt.publish as publish

from evdev import InputDevice, categorize, ecodes

CONTROLLER_LOCATION = "/dev/input/event0"
LASER_ON = "ON"
LASER_OFF = "OFF"
MQTT_HOST = 'localhost'

TOPIC_TARGET          = 'catlaser/target'
TOPIC_RELATIVE        = 'catlaser/relative'
TOPIC_PATH            = 'catlaser/path'
TOPIC_LASER           = 'catlaser/laser'

print("Welcome to the cat laser toy!")
print("- D-pad: Move")
print("- B: Laser on/off")
print("- L/R bumper: fast mode")
print("- Start: sleep")
print("- A: keep track of movement")
print("- X: play back movement")

gamepad = InputDevice(CONTROLLER_LOCATION)

move_list = []
is_laser_on = True
up = False
down = False
left = False
right = False
to_break = False
l_trig = False
r_trig = False
keep_track = False
play_moves = False
while True:
    if to_break:
        publish.single(TOPIC_LASER, LASER_OFF, hostname=MQTT_HOST)
        while to_break:
            time.sleep(0.5)
            try:
                events = gamepad.read()
                for event in events:
                    if event.type == ecodes.EV_KEY:
                        if event.code == 297: #START
                            if event.value == 1:
                                to_break = False
                                publish.single(TOPIC_LASER, LASER_ON, hostname=MQTT_HOST)
            except BlockingIOError:
                #do nothing
                pass
    x = 0
    y = 0
    if up:
        y = 30
    elif down:
        y = -30
    if left:
        x = -30
    elif right:
        x = 30
    if (x != 0) or (y != 0):
        if l_trig or r_trig:
            x *= 2
            y *= 2
        publish.single(TOPIC_RELATIVE, f"{x},{y}", hostname=MQTT_HOST)
    if keep_track and (x != 0 or y != 0):
        move_list.append((x, y, True))
    if play_moves:
        for ex, why, on in move_list:
            if on:
                publish.single(TOPIC_LASER, LASER_ON, hostname=MQTT_HOST)
            else:
                publish.single(TOPIC_LASER, LASER_OFF, hostname=MQTT_HOST)
            publish.single(TOPIC_RELATIVE, f"{ex},{why}", hostname=MQTT_HOST)
        play_moves = False

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
                    if event.value == 1:
                        play_moves = True
                elif event.code == 290: # B button
                    if event.value == 1:
                        if is_laser_on:
                            publish.single(TOPIC_LASER, LASER_OFF, hostname=MQTT_HOST)
                            is_laser_on = False
                        else:
                            is_laser_on = True
                            publish.single(TOPIC_LASER, LASER_ON, hostname=MQTT_HOST)
                elif event.code == 289: # A button
                    if event.value == 1:
                        keep_track = True
                    elif event.value == 0:
                        keep_track = False
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
