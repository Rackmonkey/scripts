#!/usr/bin/python3.4
# written by David Bauer, initial start 04.12.2016
# status: Allet geht!
##

import helper.basic as basics
#import glob
import sys, os
import argparse
import configparser
import subprocess
import time

version = 1.0

# ======================================================================================================================
# ======================================================================================================================
#	Funktionen
# ======================================================================================================================


def move_folder(domain, homeRoot):
	basics.make_ordner("/home/removed")
	basics.command("mv \""+homeRoot+"/"+domain+"\" \""+homeRoot+"/removed/"+domain+"_"+time.time() +"\"")

def deactivate_vhost(domain):
	basics.command("/usr/sbin/a2dissite " + domain)

def remove_configs(domain):
	if (basics.check_file("/etc/php5/fpm/pool.d/",domain + ".conf")):
		basics.command("rm " + "/etc/php5/fpm/pool.d/" + domain + ".conf")
	if (basics.check_file("/etc/apache2/sites-available/",domain + fileSuffix)):
		basics.command("/etc/apache2/sites-available/" + domain + fileSuffix)

def restart_services():
	basics.command("service apache2 reload")
	basics.command("service php5-fpm force-reload")

def delete_user(domain):
	basics.command("userdel -r -f " + domain)

def check_if_vhost(domain):
	if (basics.check_file("/etc/php5/fpm/pool.d/",domain + ".conf")) AND (basics.check_file("/etc/apache2/sites-available/",domain + fileSuffix)):
		return True
	else
		return False

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

if check_if_vhost():
	deactivate_vhost(domain)
	remove_configs(domain)
	move_folder(domain, homeRoot)
	delete_user(domain) # delete user with home dir
	restart_services()
else
	print("value is no valid vhost")