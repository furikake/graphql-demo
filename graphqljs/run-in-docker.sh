#!/bin/bash
set -e

APP_DIR=/app/

# install npm dependencies
cd $APP_DIR && npm install

# start app
/sbin/su-exec root npm run start-babel-node