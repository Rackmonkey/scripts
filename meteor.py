#!/usr/bin/python2.7
# written by David Bauer, initial start 03.03.2015
#
# Helper for meteor environment
#
# STATUS: untested
##

version = 0.1

import socket
import helper.basic as basics
import sys, os
import argparse
import configparser
import subprocess

config = configparser.ConfigParser()

parser = argparse.ArgumentParser(description='node.js application helper')
parser.add_argument("-b", "--build", help="build meteor app before running", default=False, action="store_true")
parser.add_argument("--pm2", help="run with pm2", default=False, action="store_true")
parser.add_argument("-r", "--run", help="run app", default=False, action="store_true")
parser.add_argument("-i", "--init", help="run app", default=False, action="store_true")
parser.add_argument("-p", "--port", type=int, help="port for node app", required=True)
parser.add_argument("-e", "--env", help="develop OR production", default="develop")

#parser.add_argument("-o", "--overwrite", help="overwrite existent files", action="store_true", default=False)

def check_port(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((remoteServerIP, port))
	sock.close()
	return result

def check_file(path,file):
	if not (os.path.isfile(path + file)):
		return 0
	else:
		return 1

args = vars(parser.parse_args())
path_script = os.getcwd()
path_env = os.path.dirname(path_script)  ## a bit diiirty!
folder_script = path_script.replace(path_env + "/", "")
folder_dev = "develop"
path_dev = path_env + "/" + folder_dev
folder_prod = "app"
path_prod = path_env + "/" + folder_prod
folder_config = "config"
path_config = path_env + "/" + folder_config

if(args["init"]):
	basics.make_ordner(path_prod)
	basics.make_ordner(path_dev)
	basics.make_ordner(path_dev)
	config.add_section('ENV')

	root_url 			= raw_input("ROOT_URL: ")
	mongo_user 			= raw_input("ROOT_URL: ")
	mongo_pass 			= raw_input("ROOT_URL: ")
	mongo_ip 			= raw_input("ROOT_URL: ")
	mongo_port 			= raw_input("ROOT_URL: ")
	mongo_collection 	= raw_input("ROOT_URL: ")

	config.set('ENV','ROOT_URL',root_url)
	config.set('ENV','MONGO_URL','mongodb://' + mongo_user + ':' + mongo_pass + '@' + mongo_ip + ':' + mongo_port + '/' + mongo_collection)
	config.set('ENV','PORT',args["port"])
	#config.set('ENV','HTTP_FORWARDED_COUNT','1')
	
	configfile = open(path_config + "/config.ini",'w')
	status.write(configfile)
	configfile.close()

if not check_file(path_config + "/","meteor.conf"):
	print "config is not present. please run with -i (--init)"
	sys.exit()

config.read(path_config + "/meteor.conf")

else:
	if not(check_port(args["port"])):
		print "port is not free"
		sys.exit()
	
	if(args["build"] and ["args.env"] != "develop"):
		os.chdir(path_dev)
		basics.command("meteor build --directory " + path_prod)
	
	if(args["run"]):
		if(args["env"] == "develop"):
			os.chdir(path_dev)
			basics.command("./set_env.sh")
			basics.command("meteor --port " + args["port"])
		
		if(args["env"] == "production"):
			os.chdir(path_prod + "/bundle/programs/server")
			basics.command("npm install")
			os.chdir(path_prod)
			basics.command("./set_env.sh")
			basics.command("node bundle/main.js")

