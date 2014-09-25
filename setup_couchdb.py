#!/usr/bin/python3.2
# written by David Bauer, initial start 22.09.2014
# 
#
##

import helper.basic as basics
import sys, os
import argparse
import configparser

parser = argparse.ArgumentParser(description='Anlegen einer neuen Domain')
#parser.add_argument("-h", help="print this help")
parser.add_argument("-b", "--bind", help="Bind to IP. Default 127.0.0.1", default="127.0.0.1")
parser.add_argument("-p", "--port", help="Port, Default: 5984", default="5984")
parser.add_argument("-s", "--secret", help="Port, Default: 5984")
#parser.add_argument("-o", "--overwrite", help="overwrite existent files", action="store_true", default=False)
args = vars(parser.parse_args())

domain = args["domain"]
homeRoot = args["home"]

conf = configparser.ConfigParser()
conf.read("/etc/couchdb/local.ini")

conf.set("httpd", 'port', args["port"])
conf.set("httpd", 'bind_address', args["bind"])
conf.set("couch_httpd_auth", 'secret', args["secret"])

conf.write("/etc/couchdb/local.ini")
