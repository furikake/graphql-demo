#!/bin/bash
set -e

APP_PATH=/restapi

pip3 install -r "$APP_PATH"/requirements.txt
export FLASK_APP="$APP_PATH"/main.py

# check if DB exists first
if [[ ! -e "$APP_PATH"/db/demo.db ]]; then
	echo "Database not found. Creating."
	flask initdb
fi

# start app
/sbin/su-exec nobody gunicorn --workers=2 -b 0.0.0.0:8000 --log-file=- --chdir=$APP_PATH main:app