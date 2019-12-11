#!/bin/bash
# Start the flask server

sudo FLASK_APP=server.py nohup flask run --host 0.0.0.0 --port 80 > log.txt &
