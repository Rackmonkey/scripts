#!/usr/bin/python2.7
# written by David Bauer, initial start 03.03.2015
#
# Helper for meteor environment
#
# STATUS: untested
# TODO: pm2 support and parallel dev+prod environment
##

version = 0.1
meteor_port = 0;


from termcolor import colored
import socket
import helper.basic as basics
import sys, os
import argparse
import configparser
import subprocess
import demjson

config = configparser.ConfigParser()
parser = argparse.ArgumentParser(description='meteor application helper')
parser.add_argument("-b", "--build", help="build meteor app (pre running)", default=False, action="store_true")
#parser.add_argument("--pm2", help="run with pm2", default=False, action="store_true")
#parser.add_argument("-s","--set", help="var=value", default=False, action="store_true")
parser.add_argument("-r", "--run", help="run app", default=False, action="store_true")
parser.add_argument("-i", "--init", help="init the environment", default=False, action="store_true")
parser.add_argument("-e", "--env", help="develop OR production OR pm2")
parser.add_argument("--backup", help="backup Mongo DB to file (pre running)")
parser.add_argument("--restore", help="restore Mongo DB from file (pre running)")
parser.add_argument("--list", help="list Mongo DB backups")

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

def check_config():
	if not check_file(path_config + "/","meteor.conf"):
		print colored("config is not present. please run with -i (--init)", "red")
		sys.exit()

def init():
	basics.make_ordner(path_prod)
	basics.make_ordner(path_dev)
	basics.make_ordner(path_config)
	basics.make_ordner(path_backup)

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
	config.set('DEV','MONGO_USER',"")
	config.set('DEV','MONGO_PASS',"")
	config.set('DEV','MONGO_IP',"127.0.0.1")
	config.set('DEV','MONGO_PORT',"3001")
	config.set('DEV','MONGO_COLLECTION',"meteor")
	config.set('DEV','PORT',"3000")
	#config.set('ENV','HTTP_FORWARDED_COUNT','1')

	config.add_section('PROD')
	config.set('PROD','ROOT_URL',root_url)
	config.set('PROD','MONGO_URL','mongodb://' + mongo_pp + mongo_ip + ':' + mongo_port + '/' + mongo_collection)
	config.set('PROD','MONGO_USER',mongo_user)
	config.set('PROD','MONGO_PASS',mongo_pass)
	config.set('PROD','MONGO_IP',mongo_ip)
	config.set('PROD','MONGO_PORT',mongo_port)
	config.set('PROD','MONGO_COLLECTION',mongo_collection)
	config.set('PROD','PORT',meteor_port)
	#config.set('ENV','HTTP_FORWARDED_COUNT','1')

	config.add_section('SETTING')
	config.set('SETTING','environment',"develop")

	config.add_section('STATUS')
	config.set('STATUS','last_build',"")

	# save config
	configfile = open(path_config + "/meteor.conf",'w')
	config.write(configfile)
	configfile.close()
	json_data = '{ "name": "' + pm2_name + '", \
		"script": "../app/bundle/main.js", \
		"log_date_format": "YYYY-MM-DD", \
    	"exec_mode": "fork_mode", \
    	"env": { \
    	    "PORT": ' + config['PROD']['PORT'] + ', \
    	    "MONGO_URL": "' + config['PROD']['MONGO_URL'] + '", \
    	    "ROOT_URL": "' + config['PROD']['ROOT_URL'] + '", \
    	    "log_file": "pm2.log", \
    	    "merge_logs": true \
      	}\
	}'

	json_file = open(path_config + "/pm2.json",'w')
	json_file.write(json_data)
	json_file.close()



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
folder_backup = "backup"
path_backup = path_env + "/" + folder_backup

try:
	if(args["init"]):
		init()


	if(args["build"] or args["run"] or args["backup"]):

		# config present? if not we stop.
		check_config()
		
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
			env_conf = "DEV"
		else:
			env_conf = "PROD"

		if(args["backup"]):
			check_config()
			command =  "mongodump -h " + config[env_conf]['MONGO_IP']
			command += " --port " + config[env_conf]['MONGO_PORT']
			command += " -d " + config[env_conf]['MONGO_COLLECTION']
			if not (config[env_conf]['MONGO_USER'] == "" or config[env_conf]['MONGO_PASS'] == ""):
				command += " -u " + config[env_conf]['MONGO_USER']
				command += " -p " + config[env_conf]['MONGO_PASS']
			command += " -v "
			command += ' -o "' + path_backup + '/' + args["backup"] + '"'
			verbose_command(command)

		if(args["restore"]):
			check_config()
	
		if(env == "develop"):
			meteor_port 	= config['DEV']['PORT']
			root_url 		= config['DEV']['ROOT_URL']
			mongo_url 		= config['DEV']['MONGO_URL']
		else:
			meteor_port 	= config['PROD']['PORT']
			root_url 		= config['PROD']['ROOT_URL']
			mongo_url 		= config['PROD']['MONGO_URL']

	
		
		if(args["build"] and ["args.env"] != "develop"):
				verbose_chdir(path_dev)
				verbose_command("meteor build --directory " + path_prod)
		
		if(args["run"]):
			print  colored("set:", 'cyan'), colored("environment variables", 'magenta')
			if not(check_port(int(meteor_port))):
				print colored("port is not free: " + meteor_port, "red")
				sys.exit()

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
				if not check_file(path_config + "/","pm2.json"):
					print colored("pm2.json is not present. please run with -i (--init)", "red")
					sys.exit()
				verbose_command("pm2 start ../config/pm2.json")


except (SystemExit):
	print colored("SystemExit: stop script", "red")
	sys.exit()
except (KeyboardInterrupt):
	print colored("KeyboardInterrupt: stop script", "red")
	sys.exit()