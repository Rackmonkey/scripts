#
# written by David Bauer, initial start 11.09.2014
# some usefull funktions to convert Bash Scripts to Python
##

import os,subprocess,sys
from subprocess import Popen, PIPE, call
from os import path

# ======================================================================================================================
# ======================================================================================================================
#	Funktionen
# ======================================================================================================================

def command(cmd):
	process = subprocess.Popen(cmd, shell=True)
	process.wait()
	errorcode = process.returncode
	#process.kill()
	return errorcode

# File vorhanden wenn nicht beenden
def check_file(path,file):
	if not (os.path.isfile(path + file)):
		return 0
	else:
		return 1

# Programm beenden
def beenden():
	sys.exit()

# Ordner vorhanden wenn nicht erstellen
def check_ordner(path):
	if not (os.access(path, os.F_OK)):
		print("0: " + path)
		return 0
	else:
		print("1: " + path)
		return 1

# Ordner erstellen
# Python scheint asyncron zu arbeiten was Betriebsystem/Filesystem zugriff angeht.
# os.access(path, os.F_OK) meldet vereinzelt gelöschte Ordner als vorhanden.
# Könnte auch nur mitm Netzwerk Share zutun haben.
def make_ordner(path):
	try:
		os.mkdir(path)
	except OSError:
		pass
	
# ======================================================================================================================
# ======================================================================================================================
#                                                   SNIPPETS
# ======================================================================================================================
#
#
# urllib.request.urlopen(apiURL + "/create?hostname=asd")
#
# process = subprocess.Popen("", shell=True)
# process.wait()
# errorcode = process.returncode
# process.kill()
#
#
#