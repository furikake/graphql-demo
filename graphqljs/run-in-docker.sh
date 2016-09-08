#!/bin/bash
set -e

cd $APP_DIR

# start app
/sbin/su-exec root npm run start-babel-node