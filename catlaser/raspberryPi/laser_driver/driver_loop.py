# Raspberry Pi Cat Laser Driver
# This code controls the laser pointer servos to target the laser at different
# locations.  Make sure to modify the MQTT_SERVER variable below so that it points
# to the name or IP address of the host computer for the cloud server VM (i.e. the
# machine running the Vagrant virtual machine that has the MQTT broker).
# Author: Tony DiCola
import sys

import model
import servos

import paho.mqtt.client as mqtt
import parse
import RPi.GPIO as GPIO

from evdev import InputDevice, categorize, ecodes

# Configuration:
SERVO_I2C_ADDRESS     = 0x40   # I2C address of the PCA9685-based servo controller
SERVO_XAXIS_CHANNEL   = 1      # Channel for the x axis rotation which controls laser up/down
SERVO_YAXIS_CHANNEL   = 0      # Channel for the y axis rotation which controls laser left/right
LASER_CHANNEL         = 5
SERVO_PWM_FREQ        = 50     # PWM frequency for the servos in HZ (should be 50)
SERVO_MIN             = 150    # Minimum rotation value for the servo, should be -90 degrees of rotation.
SERVO_MAX             = 600    # Maximum rotation value for the servo, should be 90 degrees of rotation.
SERVO_CENTER          = 200    # Center value for the servo, should be 0 degrees of rotation.
MQTT_SERVER           = 'localhost'  # MQTT server to connect to for receiving commands.
MQTT_PORT             = 1883         # Port for the MQTT server.
LASER_GPIO            = 23     # GPIO pin connected to a transistor that controls the laser on/off.
# MQTT topics used for controlling the laser.
TOPIC_TARGET          = 'catlaser/target'
TOPIC_RELATIVE        = 'catlaser/relative'
TOPIC_PATH            = 'catlaser/path'
TOPIC_LASER           = 'catlaser/laser'

CONTROLLER_LOCATION = "/dev/input/event0"

# Create servo and laser movement model.
servos = servos.Servos(SERVO_I2C_ADDRESS, SERVO_XAXIS_CHANNEL, SERVO_YAXIS_CHANNEL, LASER_CHANNEL, SERVO_PWM_FREQ)
model = model.LaserModel(servos, SERVO_MIN, SERVO_MAX, SERVO_CENTER, LASER_GPIO)
gamepad = InputDevice(CONTROLLER_LOCATION)

# MQTT callbacks:
def on_connect(client, userdata, flags, rc):
    # Called when connected to the MQTT server.
    print('Connected to MQTT server!')
    # Subscribe to the laser targeting topic.
    client.subscribe(TOPIC_TARGET)
    client.subscribe(TOPIC_PATH)
    client.subscribe(TOPIC_RELATIVE)
    client.subscribe(TOPIC_LASER)

def on_message(client, userdata, msg):
    # Called when a MQTT message is received.
    print('{0}: {1}'.format(msg.topic, str(msg.payload)))
    # Handle a target request.
    if msg.topic == TOPIC_TARGET:
        # Try to parse out two numbers from the payload.  These are the
        # screen x and screen y coordinates for the target command.
        result = parse.parse('{:d},{:d}', msg.payload.decode('ascii'))
        if result is not None:
            # Got a valid pair of numbers, use the laser model to target that
            # position.
            model.target(result[0], result[1])
    elif msg.topic == TOPIC_RELATIVE:
        # Try to parse out two numbers from the payload.  These are the
        # relative coordinates for the relative target command.
        result = parse.parse('{:d},{:d}', msg.payload.decode('ascii'))
        if result is not None:
            # Got a valid pair of numbers, use the laser model to target that
            # position.
            model.target_relative(result[0], result[1])
    elif msg.topic == TOPIC_PATH:
        lines = msg.payload.decode("ascii")
        lines = lines.split(";")
        path_list = []
        for line in lines:
            result = parts.parse("{:d},{:d}", line)
            if result is not None:
                path_list.append((result[0], result[1]))
        model.target_path(path_list)
    elif msg.topic == TOPIC_LASER:
        mess = msg.payload.decode('ascii')
        if mess == "ON":
            model.Laser_On()
        elif mess == "OFF":
            model.Laser_Off()
        else:
            model.Toggle_Laser()
            


def on_disconnect(client, userdata, rc):
    # Called when disconnected by the MQTT server.  For now just prints out the
    # result code/reason for disconnecting and quits.
    print('Disconnected with rc: {0}'.format(rc))
    sys.exit(1)


# Turn the laser on by setting its control GPIO high.
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_GPIO, GPIO.OUT)
GPIO.output(LASER_GPIO, GPIO.HIGH)

# Setup MQTT client and connect to server.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Run a loop in the foreground that waits for MQTT events/messages and processes
# them appropriately with the callbacks above.  The loop_forever call will never
# return!
print('Press Ctrl-C to quit...')
client.loop_start()

print("Welcome to the cat laser toy!")
print("- D-pad: Move")
print("- B: Laser on/off")
print("- L/R bumper: fast mode")
print("- Start: sleep")
print("- A: keep track of movement")
print("- X: play back movement")

move_list = []
is_laser_on = True
up = False
down = False
left = False
right = False
to_break = False
l_trig = False
r_trig = False
change_laser_on = False
keep_track = False
play_moves = False
while True:
    if to_break:
        while to_break:
            time.sleep(0.5)
            try:
                events = gamepad.read()
                for event in events:
                    if event.type == ecodes.EV_KEY:
                        if event.code == 297: #START
                            if event.value == 1:
                                to_break = False
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
        model.target_relative(x, y)
    if keep_track and (x != 0 or y != 0):
        move_list.append((x, y, True))
    if play_moves:
        for ex, why, on in move_list:
            if on:
                model.Laser_On()
            else:
                model.Laser_Off()
            model.target_relative(ex, why)
        play_moves = False
    if change_laser_on:
        if is_laser_on:
            model.Laser_On()
        else:
            model.Laser_Off()
        change_laser_on = False
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
                            is_laser_on = False
                            change_laser_on = True
                        else:
                            is_laser_on = True
                            change_laser_on = True
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
