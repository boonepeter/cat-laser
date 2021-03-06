# Raspberry Pi Laser Driver Setup

The laser driver is Python 3 code that runs on the Raspberry Pi and listens for
laser targeting commands from a MQTT broker (running on the cloud server).

To run this code first make sure you have Python 3 installed on the Pi:

    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-dev python3-numpy git

Next make sure you have the PC9685 library installed by running:

    cd ~
    git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git
    cd Adafruit_Python_PCA9685
    sudo python3 setup.py install

Finally you must install the paho-mqtt client for Python 3 by running:

    sudo pip3 install paho-mqtt


### Note:
The following steps must be completed on the pi before the server works:
Ensure mjpeg-streamer is running and exposing an MJPEG video stream of the Pi camera.

- If your Pi is not directly accessible to the internet (i.e. if you're at home and the Pi is connected to a router) forward port 8080 from your router to the Raspberry Pi. This will allow outside users (like the cloud server) to access the video stream.

- Ensure ssh is running to create a tunnel for port 1883 (MQTT) to this cloud server. On the Pi run the following command (you will need to adjust the -i option to point at the private key for connecting to your cloud server and specify the right username and address for the cloud server):

ssh -nNT -L 1883:localhost:1883 -i /path/to/cloud/server/key.pem user@cloudserver &
- This will run the SSH tunnel in the background and all the Pi to access the cloud server's MQTT server securely without a lot of certificate and SSL hassle.

- Ensure the LaserDriver script is calibrated (using the LaserServer and copying over its calibration.json) and running.

Now you are almost ready to run the laser driver code in this directory.  Before
you run the code make sure to get a calibration.json file from the LaserServer
directory.  Run the original laser server (see part 2) code and go through its
calibration process.  Then copy the calibration.json from the LaserServer directory
into the same directory as this laser driver code.

Next modify the MQTT_SERVER variable at the top of driver.py so that it matches
the hostname or IP address of the host machine running the cloud server VM and
MQTT broker.  This will allow the laser driver to connect to the MQTT broker on
the cloud server and receive targeting commands.

To run the laser driver run the following command from within this directory:

    python3 driver.py

The laser driver should connect to the MQTT broker and wait to receive targeting
messages.  To send a target message you can use the mosquitto_pub command on the
cloud server.  Connect to the cloud server VM and run the following command:

    mosquitto_pub -t "catlaser/target" -m "100,200"

This will tell the laser driver to target screen position 100, 200 with the laser.
You should see the laser move into a position like this!
