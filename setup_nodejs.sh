#!/bin/bash
#
# written by David Bauer, initial start 17.09.2014
# 
# Status: Sollte funzen

aptitude -y update 1>/dev/null
aptitude install nodejs sudo #nodejs-legacy

npm install sails -g # sails wird global installiert
npm install forever -g 

adduser --force-badname --disabled-password --gecos "" --home /home/node --shell /bin/bash node