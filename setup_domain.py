#!/usr/bin/python3.4
# written by David Bauer, initial start 11.09.2014
# Inspiriert von https://github.com/bastelfreak/scripts/blob/master/setup_domain.sh
# 
# Apache < 2.4 ist highly broken!
# Apache = 2.4 lueppt sehr gut
# status: Allet geht!
##

import helper.basic as basics
#import glob
import sys, os
import argparse
import configparser
import subprocess
from termcolor import colored

version = 1.0

# argumente auswerten

parser = argparse.ArgumentParser(description='Anlegen einer neuen Domain')
#parser.add_argument("-h", help="print this help")
parser.add_argument("-n", "--home", help="home root path. default: \"/home\"", default="/home")
parser.add_argument("--nossl", help="no ssl certificate for me", action='store_true')
parser.add_argument("-d", "--domain", help="domain name", required=True)
parser.add_argument("-f","--force", help="dont ask, just fucking do it!", action='store_true')
parser.add_argument("-t","--test", help="just test the command output", action='store_true')
parser.add_argument("-v","--verbose", help="verbose", action='store_true')
#parser.add_argument("-o", "--overwrite", help="overwrite existent files", action="store_true", default=False)
args = vars(parser.parse_args())

domain = args["domain"]
homeRoot = args["home"]
nossl = True if args["ssl"] else False
force = True if args["force"] else False
test = True if args["test"] else False
verbose = True if args["verbose"] else False

if verbose:
	basics.set_print_command(True)

#overwrite = args["overwrite"]

print  colored("setup domain script", 'red')
print  colored("homeroot:", 'cyan'), colored(homeRoot, 'magenta')
print  colored("domain:", 'cyan'), colored(domain, 'magenta')
if nossl:
	print  colored("SSL:", 'cyan'), colored("no", 'magenta')
else:
	print  colored("SSL:", 'cyan'), colored("yes", 'magenta')

yesNo = basics.query_yes_no("Do you want to create this vHost?")
if force: 
	yesNo = "yes"

# ======================================================================================================================
# ======================================================================================================================
#	Funktionen
# ======================================================================================================================

def add_domain_to_dns():
	global domain
	return true

def create_www_user():
	global domain, homeRoot
	if(basics.command("grep --quiet \"" + domain + "\" /etc/passwd")):
		basics.command("adduser --force-badname --disabled-password --gecos \"\" --home \""+ homeRoot + "/" + domain +"\" --shell /bin/bash \"" + domain + "\"")
		#basics.command("usermod --append --groups  www-data")
		basics.command("usermod --append --groups www-data \""+ domain +"\"")

def create_www_home():
	global domain, homeRoot
	print  colored("create www home", 'red')
	path = homeRoot + "/" + domain
	basics.make_ordner(path + "/htdocs")
	basics.make_ordner(path + "/tmp")
	basics.make_ordner(path + "/config")
	basics.make_ordner(path + "/logs")
	basics.command("chown --recursive \""+domain+":"+domain+"\" \""+homeRoot+"/"+domain+"\"")
	basics.command("chmod 755 --recursive \""+homeRoot+"/"+domain+"\"")

def get_fpm_port():
	# the default port from the standard php-fpm config is 9000
	max_port = 9001 #init for first vhost
	port = 0
	conf = configparser.ConfigParser()
	print  colored("Searching for highest FPM Port", 'red')

	for root, dirs, files in os.walk("/etc/php5/fpm/pool.d/"):
	    for file in files:
	    	if not (file == "www.conf"):
		        if file.endswith('.conf'):
		            conf.read("/etc/php5/fpm/pool.d/" + file)
		            section = conf.sections()
		            ipPort = conf.get(section[0], 'listen')
		            port = ipPort.split(":")
		            if(max_port < int(port[1])):
		            	max_port = int(port[1])

	print  colored("Found highest Port: ", 'cyan'), colored(max_port, 'magenta')
	print  colored("Port for new vHost: ", 'cyan'), colored(max_port+1 , 'magenta')
	return max_port + 1

def add_apache_vhost():
	global domain, homeRoot, nossl, fpmPort
	print  colored("add apache vhost", 'red')
	if not(basics.check_file("/etc/apache2/sites-available/",domain + ".conf")):
		if nossl:
			templateFile = open("templates/apache_conf.txt", "r")
		else:
			templateFile = open("templates/apache_conf_ssl.txt", "r")
		template = templateFile.read();
		templateFile.close();
		template = template.replace("[root_path]",homeRoot);
		template = template.replace("[domain]",domain);
		template = template.replace("[port]",str(fpmPort));
		configFile = open("/etc/apache2/sites-available/" + domain + ".conf", "w")
		configFile.write(template)
		configFile.close();

def add_phpfpm_conf():
	global domain, homeRoot, fpmPort
	print  colored("add php fpm conf", 'red')
	if not(basics.check_file("/etc/php5/fpm/pool.d/",domain + ".conf")):
		templateFile = open("templates/php-fpm_conf.txt", "r")
		template = templateFile.read();
		templateFile.close();
		template = template.replace("[root_path]",homeRoot);
		template = template.replace("[domain]",domain);
		template = template.replace("[port]",str(fpmPort));
		configFile = open("/etc/php5/fpm/pool.d/" + domain + ".conf", "w")
		configFile.write(template)
		configFile.close();
	basics.command("service php5-fpm force-reload")

def lets_encrypt():
	global domain, homeRoot
	basics.command("certbot --apache certonly --webroot -w " + homeRoot + " -d " + domain )

def enable_apache_site():
	global domain
	basics.command("/usr/sbin/a2ensite " + domain)
	basics.command("service apache2 reload")

def restart_services():
	basics.command("service apache2 reload")
	basics.command("service php5-fpm force-reload")

# ======================================================================================================================
# ======================================================================================================================
#	shots are fired!!!!
# ======================================================================================================================

if yesNo == "yes":
	fpmPort = get_fpm_port()
	create_www_user()
	create_www_home()
	if not nossl:
		lets_encrypt()
	add_apache_vhost()
	add_phpfpm_conf()
	enable_apache_site()
	print  colored("created the vhost " + domain, 'red')
else:
	print  colored("not created the vhost " + domain, 'red')

# ======================================================================================================================
# ======================================================================================================================
#	the End
# ======================================================================================================================