#!/usr/bin/python3.2
#
# written by David Bauer, initial start 17.09.2014
# 
import helper.basic as basics
import sys

# erstma updaten
print("sourcen updaten")
basics.command("aptitude -y update 1>/dev/null")
print("sourcen geupdatet")

# add more cool tools
basics.command("aptitude install apache2-mpm-worker")
basics.command("aptitude install apache2-utils libapache2-mod-fastcgi")
basics.command("aptitude install php5-fpm")
basics.command("a2enmod actions")
basics.command("service apache2 restart")

#basics.command('echo "apache2-mpm-worker 2.4 (sid), php5-fpm 5.6 (sid) and fastcgi setup" >> /etc/motd')
#basics.command('echo "apache2-mpm-worker, php5-fpm and fastcgi setup" >> /etc/motd')
#basics.command('echo "by david bauer aka debauer - me@debauer.net" >> /etc/motd')
#basics.command('echo "" >> /etc/motd')
#basics.command('echo "USAGE:" >> /etc/motd')
#basics.command('echo "- do not install change anything relatet to this packages!" >> /etc/motd')
#basics.command('echo "- use setup_domain.py script to add new vHosts. location: /root/scripts" >> /etc/motd')