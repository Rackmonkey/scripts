#!/usr/bin/python2.7
# written by David Bauer, initial start 03.03.2015
#
# Helper for meteor environment
#
# STATUS: untested
# TODO: pm2 support and parallel dev+prod environment
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

parser = argparse.ArgumentParser(description='meteor application helper')
parser.add_argument("-b", "--build", help="build meteor app before running", default=False, action="store_true")
#parser.add_argument("--pm2", help="run with pm2", default=False, action="store_true")
#parser.add_argument("-s","--set", help="var=value", default=False, action="store_true")
parser.add_argument("-r", "--run", help="run app", default=False, action="store_true")
parser.add_argument("-i", "--init", help="init the environment", default=False, action="store_true")
parser.add_argument("-e", "--env", help="develop OR production OR pm2")

def verbose_command(cmd):
	print  colored("command:", 'cyan'), colored(cmd, 'magenta')
	basics.command(cmd)

def verbose_chdir(cmd):
	print colored("chdir:", 'cyan'), colored(cmd, 'magenta')
	os.chdir(cmd)
	#print colored("path:", 'cyan'), colored(os.getcwd(), 'magenta')

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
	basics.make_ordner(path_config)

	print "init environment"

	# ask for the basic config
	url 				= raw_input("url (www.example.tld): ")
	mongo_collection 	= raw_input("mongo collection (meteor): ")
	mongo_user 			= raw_input("mongo user (-): ")
	mongo_pass 			= raw_input("mongo pass (-): ")
	mongo_ip 			= raw_input("mongo ip (127.0.0.1): ")
	mongo_port 			= raw_input("mongo port (27017): ")
	meteor_port 		= raw_input("meteor port (8000): ")

	# set defaults if the input ist empty
	root_url 			= "http://" + url		if (len(url 		)>0) else 'http://example.tld'
	pm2_name 			= url					if (len(url 		)>0) else 'unnamed'
	mongo_collection 	= mongo_collection		if (len(mongo_collection)>0) else 'meteor' 
	mongo_ip 			= mongo_ip 				if (len(mongo_ip  		)>0) else '127.0.0.1'
	mongo_port 			= mongo_port 			if (len(mongo_port 		)>0) else '27017'	
	meteor_port 		= meteor_port 			if (len(meteor_port 	)>0) else '8000'	

	if(mongo_user == '' or mongo_pass == ''):
		mongo_pp = ''
	else:
		mongo_pp = mongo_user + ':' + mongo_pass + '@'

	# set config collection
	config.add_section('DEV')
	config.set('DEV','ROOT_URL',"")
	config.set('DEV','MONGO_URL',"")
	config.set('DEV','PORT',"3000")
	#config.set('ENV','HTTP_FORWARDED_COUNT','1')

	config.add_section('PROD')
	config.set('PROD','ROOT_URL',root_url)
	config.set('PROD','MONGO_URL','mongodb://' + mongo_pp + mongo_ip + ':' + mongo_port + '/' + mongo_collection)
	config.set('PROD','PORT',meteor_port)
	#config.set('ENV','HTTP_FORWARDED_COUNT','1')

	config.add_section('SETTING')
	config.set('SETTING','environment',"develop")

	config.add_section('STATUS')
	config.set('STATUS','last_build',"")

	config.add_section('PM2')
	config.set('PM2','name',pm2_name)
	config.set('PM2','mode',"fork_mode")
	config.set('PM2','log_date_format',"YYYY-MM-DD")
	config.set('PM2','log_file',"pm2.log")
	config.set('PM2','merge_logs',"1")

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

	if(args["env"] == "develop" or args["env"] == "d"):
		print  colored("set:", 'cyan'), colored("environment to develop", 'magenta')
		config['SETTING']['environment'] = "develop"
	if(args["env"] == "production" or args["env"] == "p"):
		print  colored("set:", 'cyan'), colored("environment to production", 'magenta')
		config['SETTING']['environment'] = "production"
	if(args["env"] == "pm2"):
		print  colored("set:", 'cyan'), colored("environment to pm2", 'magenta')
		config['SETTING']['environment'] = "pm2"
	configfile = open(path_config + "/meteor.conf",'w')
	config.write(configfile)
	configfile.close()
	env = config['SETTING']['environment']



	if(env == "develop"):
		meteor_port 	= config['DEV']['PORT']
		root_url 		= config['DEV']['ROOT_URL']
		mongo_url 		= config['DEV']['MONGO_URL']
	elif(env == "production"):
		meteor_port 	= config['PROD']['PORT']
		root_url 		= config['PROD']['ROOT_URL']
		mongo_url 		= config['PROD']['MONGO_URL']

	
	if(args["build"] and ["args.env"] != "develop"):
		try:
			verbose_chdir(path_dev)
			verbose_command("meteor build --directory " + path_prod)
		except (KeyboardInterrupt, SystemExit):
			print colored("KeyboardInterrupt: stop script", "red")
			sys.exit()
	
	if not(check_port(int(meteor_port))):
		print colored("port is not free", "red")
		sys.exit()
	
	if(args["run"]):
		print  colored("set:", 'cyan'), colored("environment variables", 'magenta')
	
		try:
			if(env == "develop"):
				os.environ['PORT'] = meteor_port
				#os.environ['ROOT_URL'] = root_url
				#os.environ['MONGO_URL'] = mongo_url
				print  colored("env:", 'cyan'), colored("development", 'magenta')
				verbose_chdir(path_dev)
				verbose_command("meteor --port " + meteor_port)
			
			if(env == "production"):
				os.environ['PORT'] = meteor_port
				os.environ['ROOT_URL'] = root_url
				os.environ['MONGO_URL'] = mongo_url
				print  colored("env:", 'cyan'), colored("production", 'magenta')
				verbose_chdir(path_prod + "/bundle/programs/server")
				verbose_command("npm install")
				verbose_chdir(path_prod + "/bundle")
				verbose_command("node main.js")

			if(env == "pm2"):
				print  colored("env:", 'cyan'), colored("pm2", 'magenta')

		except (KeyboardInterrupt, SystemExit):
			print colored("KeyboardInterrupt: stop script", "red")
			sys.exit()