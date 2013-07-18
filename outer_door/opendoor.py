#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set GPIO 0 (the door control pin) as output 
GPIO.setup(11, GPIO.OUT)

print("Unlocking door for five seconds")
GPIO.output(11, GPIO.HIGH)
time.sleep(5)
GPIO.output(11, GPIO.LOW)
print("Door re-locked door")

