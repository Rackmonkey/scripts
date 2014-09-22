#!/bin/bash

# WORK IN PROGRESS

# Install and start the Node-Host-Api

aptitude update
aptitude install git

chmod +x setup_nodejs.sh
./setup_nodejs.sh

git clone git@domain.tld:node-host-api /home/node/node-host-api
mkdir /home/node/node-host-api_logs
forever start -l /home/node/node-host-api_logs/forever.log \
			  -o /home/node/node-host-api_logs/out.log \
			  -e /home/node/node-host-api_logs/err.log \
			  /home/node/node-host-api/app.js 

# 