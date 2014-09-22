#!/usr/bin/python3.2
#
# written by David Bauer, initial start 17.09.2014
# 

import helper.basic as basicHelper
import sys

# erstma updaten
command("aptitude -y update 1>/dev/null")
# add more cool tools
command("aptitude install apache2-mpm-worker/sid") 
command("aptitude install apache2-utils/sid php5-fpm/sid libapache2-mod-fastcgi")
command("a2enmod actions")
command("service apache2 restart")