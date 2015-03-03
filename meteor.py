#!/usr/bin/python2.7
# written by David Bauer, initial start 03.03.2015
#
# Helper for meteor environment
#
# STATUS: jooow
##

version = 0.1

import helper.basic as basics
import sys, os
import argparse
import configparser
import subprocess

parser = argparse.ArgumentParser(description='node.js application helper')
parser.add_argument("-b", "--build", help="build meteor app before running", default=False, action="store_true")
parser.add_argument("-m", "--pm2", help="run with pm2", default=False, action="store_true")
parser.add_argument("-r", "--run", help="run app", default=False, action="store_true")
parser.add_argument("-p", "--port", type=int, help="port for node app", required=True)
parser.add_argument("-e", "--env", help="develop OR production", default="develop")

#parser.add_argument("-o", "--overwrite", help="overwrite existent files", action="store_true", default=False)

def check_port(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((remoteServerIP, port))
	sock.close()
	return result


args = vars(parser.parse_args())
path_script = os.getcwd()
path_env = os.path.dirname(path_script)  ## a bit diiirty!
folder_script = path_script.replace(path_env + "/", "")
folder_dev = "develop"
path_dev = path_env + "/" + folder_dev
folder_prod = "app"
path_prod = path_env + "/" + folder_prod

basics.make_ordner(path_prod)
basics.make_ordner(path_dev)

if not(check_port(args["port"])):
	print "port is not free"
	sys.exit()

if(args["build"] and ["args.env"] != "develop"):
	os.chdir(path_dev)
	basics.command("meteor build --directory " + path_prod)

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
