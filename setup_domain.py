#!/usr/bin/python3.2
# written by David Bauer, initial start 11.09.2014
# Inspiriert von https://github.com/bastelfreak/scripts/blob/master/setup_domain.sh
# 
#
# apache >= 2.4 !!
# status: Allet geht!
##

import helper.basic as basics
#import glob
import sys, os
import argparse
import configparser

version = 1.0

# ======================================================================================================================
# ======================================================================================================================
#	Funktionen
# ======================================================================================================================


def add_domain_to_dns(domain):
	return true

def create_www_user(domain, homeRoot):
	if(basics.command("grep --quiet \"" + domain + "\" /etc/passwd")):
		basics.command("adduser --force-badname --disabled-password --gecos \"\" --home \""+ homeRoot + "/" + domain +"\" --shell /bin/bash \"" + domain + "\"")
		#basics.command("usermod --append --groups  www-data")
		basics.command("usermod --append --groups www-data \""+ domain +"\"")

def create_www_home(domain, homeRoot):
	path = homeRoot + "/" + domain
	basics.make_ordner(path + "/htdocs")
	basics.make_ordner(path + "/tmp")
	basics.make_ordner(path + "/config")
	basics.make_ordner(path + "/logs")
	basics.command("chown --recursive \""+domain+":"+domain+"\" \""+homeRoot+"/"+domain+"\"")
	basics.command("chmod 755 --recursive \""+homeRoot+"/"+domain+"\"")

def get_highest_fpm_port():
	# the default port from the standard php-fpm config is 9000
	max_port = 9001
	port = 0
	conf = configparser.ConfigParser()

	for root, dirs, files in os.walk("/etc/php5/fpm/pool.d/"):
	    for file in files:
	        if file.endswith('.conf'):
	            conf.read("/etc/php5/fpm/pool.d/" + file)
	            section = conf.sections()
	            ipPort = conf.get(section[0], 'listen')
	            port = ipPort.split(":")
	            if(max_port < int(port[1])):
	            	max_port = int(port[1])
	return max_port

def add_apache_vhost(domain,homeRoot,fpmPort):
	# wir haben nach dem höchsten gesucht und brauchen nun +1
	fpmPort += 1
	if not(basics.check_file("/etc/apache2/sites-available/",domain + ".conf")):
		templateFile = open("templates/apache_conf.txt", "r")
		template = templateFile.read();
		templateFile.close();
		template = template.replace("[root_path]",homeRoot);
		template = template.replace("[domain]",domain);
		template = template.replace("[port]",str(fpmPort));
		configFile = open("/etc/apache2/sites-available/" + domain + ".conf", "w")
		configFile.write(template)
		configFile.close();

def add_phpfpm_conf(domain,homeRoot,fpmPort):
	# wir haben nach dem höchsten gesucht und brauchen nun +1
	fpmPort += 1
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

def replace_attribute(attr,value,file):
	# sucht nach Zeile mit prefix (attr) und setzt das Value neu.
	# attr:value
	# attr=value
	# attr value
	file = open("templates/php-fpm_conf.txt")
	fileStr = file.read();
	template.replace("[root_path]",homeRoot);
	return true

def enable_apache_site(domain):
	basics.command("/usr/sbin/a2ensite " + domain)
	basics.command("service apache2 reload")

def restart_services():
	basics.command("service apache2 reload")
	basics.command("service php5-fpm force-reload")

# argumente auswerten

parser = argparse.ArgumentParser(description='Anlegen einer neuen Domain')
#parser.add_argument("-h", help="print this help")
parser.add_argument("-n", "--home", help="home root path. default: \"/home\"", default="/home")
parser.add_argument("-d", "--domain", help="domain name", required=True)
#parser.add_argument("-o", "--overwrite", help="overwrite existent files", action="store_true", default=False)
args = vars(parser.parse_args())

domain = args["domain"]
homeRoot = args["home"]
#verwrite = args["overwrite"]

create_www_user(domain, homeRoot)
create_www_home(domain, homeRoot)
fpmPort = get_highest_fpm_port()
add_apache_vhost(domain,homeRoot,fpmPort)
add_phpfpm_conf(domain,homeRoot,fpmPort)
enable_apache_site(domain)