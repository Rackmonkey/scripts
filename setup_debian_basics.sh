#!/bin/bash

# erstma updaten
# backports für certbot
echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list
echo "sourcen updaten"
aptitude -y update 1>/dev/null
echo "sourcen geupdatet"
echo ""

# add more cool tools
echo "installiere htop iftop mc python3 python3-pip"
aptitude install htop iftop mc python3 python3-pip python-certbot-apache

echo "installiere python packages"
pip install configparser

echo ""
echo "MOTD geleert"
echo "" > /etc/motd