#!/usr/bin/env python

import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 2400, timeout=1)

lasttime = 0

codes = [
  "4003510BB",
  "4003509CC",
  "700B94870",
  "10031D0E4"  
]

while(True):
	string = ser.read(12)
	string = string[2:11]
	# is the input something non-crazy?
	if(len(string) > 4):
		# debounce
		if((int(time.time()) - lasttime) > 3):
			print(string)
			lasttime = time.time()
			try:
				codes.index(string)
				print("  access granted!")
			except:
				print("  access denied :(")
