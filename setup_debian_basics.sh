#!/bin/bash

# erstma updaten
echo "sourcen updaten"
aptitude -y update 1>/dev/null
echo "sourcen geupdatet"
echo ""
# add more cool tools
echo "installiere htop iftop mc python3"
aptitude install htop iftop mc python3

echo ""
echo "MOTD geleert"
echo "" > /etc/motd