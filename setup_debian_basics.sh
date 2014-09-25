#!/bin/bash

# erstma updaten
echo "sourcen updaten"
aptitude -y update 1>/dev/null
echo "sourcen geupdatet"
echo ""
# add more cool tools
echo "installiere htop iftop mc python3"
aptitude install htop iftop mc python3
#echo "deb http://http.debian.org/debian jessie main non-free contrib" >> /etc/apt/sources.list
#echo "deb http://security.debian.org/ jessie/updates main contrib non-free" >> /etc/apt/sources.list

echo "#######################################################################################" >> /etc/apt/sources.list
echo "# Testing for apache 2.4" >> /etc/apt/sources.list
echo "#" >> /etc/apt/sources.list
echo "" >> /etc/apt/sources.list
echo "deb http://ftp.debian.org/debian sid main non-free contrib" >> /etc/apt/sources.list

echo "sid in sources.list hinzugefügt"
echo "NEW LINE: deb http://http.debian.org/debian sid main non-free contrib"

echo ""
echo "wheezy als default repository gesetzt"
echo "FILE: /etc/apt/apt.conf.d/90binwheezy"
echo "NEW LINE: APT::Default-Release \"wheezy\";"
echo "APT::Default-Release \"wheezy\";" >> /etc/apt/apt.conf.d/90binwheezy

echo ""
echo "MOTD geleert"
echo "" > /etc/motd