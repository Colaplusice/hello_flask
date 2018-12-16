#!/usr/bin/env bash

flask run -h 0.0.0.0 -p 5000
#gunicorn -b  0.0.0.0:5000 --access-logfile - --error-logfile - manage:hello_flask_app
