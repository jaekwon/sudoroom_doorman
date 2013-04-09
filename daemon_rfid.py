#!/usr/bin/env python

import sys
import serial
import subprocess
import time
from os import fork, setsid, umask, dup2, path
from sys import stdin, stdout, stderr
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f","--foreground",action="store_true",dest="foreground")
(options, args) = parser.parse_args()

#GPIO.setwarnings(False)

# daemonize
if not options.foreground:
	if fork(): exit(0)
	umask(0)
	setsid()
	if fork(): exit(0)
	stdout.flush()
	stderr.flush()
	si = file('/dev/null', 'r')
	so = file('/dev/null', 'a+')
	se = file('/dev/null', 'a+', 0)
	dup2(si.fileno(), stdin.fileno())
	dup2(so.fileno(), stdout.fileno())
	dup2(se.fileno(), stderr.fileno())

#our list of codes
codes = []

script_path = path.abspath(path.dirname(__file__))

#open codes file
try:
	f = open(script_path+'/rfid_codes.txt','r')
	for line in f:
		codes.append(line.split("#")[0].strip())
	f.close()
except:
	print("Could Find Code File")
	exit() 

try:
	ser = serial.Serial('/dev/ttyUSB0', 2400, timeout=1)
except Exception:
	print "Serial device not found"

lasttime = 0

while(True):
	string = ser.read(12)
	string = string[2:11]
	# is the input something non-crazy?
	if(len(string) > 4):
		# debounce
		if((int(time.time()) - lasttime) > 6):
			print(string)
			lasttime = time.time()
			try:
				codes.index(string)
				print("  access granted!")
				subprocess.call(script_path+"/opendoor.py")
			except:
				print("  access denied :(")
