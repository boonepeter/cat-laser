#!/bin/bash
# Start the flask server

sudo FLASK_APP=server.py flask run --host 0.0.0.0 --port 80
