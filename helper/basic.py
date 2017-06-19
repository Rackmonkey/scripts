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

print_command=False
test=False

def set_print_command(val):
	global print_command
	print_command = val

def command(cmd):
	global print_command, test
	if print_command:
		print  colored("command:", 'cyan'), colored(cmd, 'magenta')
	if not test:
		process = subprocess.Popen(cmd, shell=True)
		process.wait()
		errorcode = process.returncode
		#process.kill()
		return errorcode
	return "test"

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
# os.access(path, os.F_OK) meldet vereinzelt geloeschte Ordner als vorhanden.
# Koennte auch nur mitm Netzwerk Share zutun haben.
def make_ordner(path):
	global test
	if not test:
		try:
			os.mkdir(path)
		except OSError:
			pass
	print  colored("mkdir:", 'cyan'), colored(path, 'magenta')

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")
	
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
