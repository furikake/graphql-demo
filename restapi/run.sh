#!/bin/bash
set -e

VENV_NAME=flaskvenv

# check if virtualenv exists
if [[ ! -d ./"$VENV_NAME" ]]; then
	echo "Virtualenv not found. Initializing."
	python3 -m virtualenv ./"$VENV_NAME"
fi

source "$VENV_NAME"/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=./main.py

# check if DB exists first
if [[ ! -e ./db/demo.db ]]; then
	echo "Database not found. Creating."
	flask initdb
fi

# start app
gunicorn main:app --workers=2 -b 0.0.0.0:8000 --log-file=-
