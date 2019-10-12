#!/usr/bin/env bash
#activate venv
source ./venv/bin/activate

#start flask app
export FLASK_APP=echo_cardio
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:8000 --reload --preload wsgi:app
