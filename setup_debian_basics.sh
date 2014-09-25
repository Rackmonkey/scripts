#!/bin/bash

# erstma updaten
aptitude -y update 1>/dev/null
# add more cool tools
aptitude install htop iftop mc python3

#echo "deb http://http.debian.org/debian jessie main non-free contrib" >> /etc/apt/sources.list
#echo "deb http://security.debian.org/ jessie/updates main contrib non-free" >> /etc/apt/sources.list
echo "deb http://http.debian.org/debian sid main non-free contrib" >> /etc/apt/sources.list

echo "APT::Default-Release \"wheezy\";" >> /etc/apt/apt.conf.d/90binwheezy