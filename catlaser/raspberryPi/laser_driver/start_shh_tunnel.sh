#!/bin/bash

ssh -nNT -L 1883:localhost:1883 -i /home/pi/secrets/LightsailDefaultKey-us-east-1.pem ubuntu@50.16.5.232 &
