#!/usr/bin/env python

import sys
import serial
import subprocess
import time
from os import fork, setsid, umask, dup2
from sys import stdin, stdout, stderr

#GPIO.setwarnings(False)

# daemonize
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


ser = serial.Serial('/dev/ttyUSB0', 2400, timeout=1)

lasttime = 0

codes = [
  "4003510BB",
  "4003509CC",
  "700B94870",
  "10031D0E4",
  "4003522F4",
  "40034BA5E"
]

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
				subprocess.call("/root/sudoor/opendoor.py")
			except:
				print("  access denied :(")
