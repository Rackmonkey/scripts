#!/usr/bin/python2.7
# written by David Bauer, initial start 03.03.2015
#
# Helper for meteor environment
#
# STATUS: untested
# TODO: more verbosity and pm2 support
##

version = 0.1

from termcolor import colored
import socket
import helper.basic as basics
import sys, os
import argparse
import configparser
import subprocess

config = configparser.ConfigParser()

meteor_port = 0;

parser = argparse.ArgumentParser(description='node.js application helper')
parser.add_argument("-b", "--build", help="build meteor app before running", default=False, action="store_true")
parser.add_argument("--pm2", help="run with pm2", default=False, action="store_true")
parser.add_argument("-r", "--run", help="run app", default=False, action="store_true")
parser.add_argument("-i", "--init", help="init the environment", default=False, action="store_true")
#parser.add_argument("-p", "--port", type=int, help="port for meteor", required=True)
parser.add_argument("-e", "--env", help="develop OR production", default="develop")

#parser.add_argument("-o", "--overwrite", help="overwrite existent files", action="store_true", default=False)

def verbose_command(cmd):
	print  colored("command:", 'cyan'), colored(cmd, 'magenta')
	basics.command(cmd)

def verbose_chdir(cmd):
	print  colored("chdir:", 'cyan'), colored(cmd, 'magenta')
	os.chdir(path_dev)


def check_port(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex(("127.0.0.1", port))
	sock.close()
	return result

def check_file(path,file):
	if not (os.path.isfile(path + file)):
		return 0
	else:
		return 1

def init():
	basics.make_ordner(path_prod)
	basics.make_ordner(path_dev)
	basics.make_ordner(path_dev)
	config.add_section('ENV')

	print "init environment"

	# ask for the basic config
	root_url 			= raw_input("url (www.example.tld): ")
	mongo_collection 	= raw_input("mongo collection (meteor): ")
	mongo_user 			= raw_input("mongo user (-): ")
	mongo_pass 			= raw_input("mongo pass (-): ")
	mongo_ip 			= raw_input("mongo ip (127.0.0.1.): ")
	mongo_port 			= raw_input("mongo port (27017): ")
	meteor_port 		= raw_input("meteor port (8000): ")

	# set defaults if the input ist empty
	root_url 			= "http://" + root_url	if (len(root_url 		)>0) else 'http://example.tld'
	mongo_collection 	= mongo_collection		if (len(mongo_collection)>0) else 'meteor' 
	mongo_ip 			= mongo_ip 				if (len(mongo_ip  		)>0) else '127.0.0.1'
	mongo_port 			= mongo_port 			if (len(mongo_port 		)>0) else '27017'	
	meteor_port 		= meteor_port 			if (len(meteor_port 	)>0) else '8000'	

	if(mongo_user == '' or mongo_pass == ''):
		mongo_pp = ''
	else:
		mongo_pp = mongo_user + ':' + mongo_pass + '@'

	# set config collection
	config.set('ENV','ROOT_URL',root_url)
	config.set('ENV','MONGO_URL','mongodb://' + mongo_pp + mongo_ip + ':' + mongo_port + '/' + mongo_collection)
	config.set('ENV','PORT',meteor_port)
	#config.set('ENV','HTTP_FORWARDED_COUNT','1')

	# save config
	configfile = open(path_config + "/meteor.conf",'w')
	config.write(configfile)
	configfile.close()

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
	init()


if(args["build"] or args["run"]):
	# config present? if not we stop.
	if not check_file(path_config + "/","meteor.conf"):
		print colored("config is not present. please run with -i (--init)", "red")
		sys.exit()
	
	# read the config
	print  colored("read:", 'cyan'), colored("config (" + path_config + "/meteor.conf)", 'magenta')
	config.read(path_config + "/meteor.conf")
	meteor_port 	= config['ENV']['PORT']
	root_url 		= config['ENV']['ROOT_URL']
	mongo_url 		= config['ENV']['MONGO_URL']
	
	if(args["build"] and ["args.env"] != "develop"):
		verbose_chdir(path_dev)
		verbose_command("meteor build --directory " + path_prod)
	
	
	if not(check_port(int(meteor_port))):
		print colored("port is not free", "red")
		sys.exit()
	
	if(args["run"]):
		print  colored("set:", 'cyan'), colored("environment variables", 'magenta')
		os.environ['PORT'] = meteor_port
		os.environ['ROOT_URL'] = root_url
		os.environ['MONGO_URL'] = mongo_url
	
		if(args["env"] == "develop"):
			verbose_chdir(path_dev)
			verbose_command("meteor --port " + meteor_port)
		
		if(args["env"] == "production"):
			verbose_chdir(path_prod + "/bundle/programs/server")
			verbose_command("npm install")
			verbose_chdir(path_prod)
			verbose_command("node bundle/main.js")


