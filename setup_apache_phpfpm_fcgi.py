#!/usr/bin/python3.2
#
# written by David Bauer, initial start 17.09.2014
# 

import helper.basic as basicHelper
import sys

# erstma updaten
basicHelper.command("aptitude -y update 1>/dev/null")
# add more cool tools
basicHelper.command("aptitude install apache2-mpm-worker/sid")
basicHelper.command("aptitude install apache2-utils/sid php5-fpm/sid libapache2-mod-fastcgi")
basicHelper.command("a2enmod actions")
basicHelper.command("service apache2 restart")
