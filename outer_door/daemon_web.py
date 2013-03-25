#!/usr/bin/env python

import sys
import time
import RPi.GPIO as GPIO
import SimpleHTTPServer, SocketServer
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

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# set GPIO 0 (the door control pin) as output 
GPIO.setup(11, GPIO.OUT)

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
#	if self.path == "/library/test/success.html":
#		self.send_response(200)
#		return
	if self.path == "/secret_password":
		self.send_response(200)
        	self.send_header('Content-type', 'text/html')
	        self.end_headers()
        	self.wfile.write("<html><head><title>sudo door</title></head>")
		self.wfile.write("<body>")             
	        self.wfile.write("<h1>WELCOME TO THE SUDOS!!1</h1>")
        	self.wfile.write("</body></html>")
		# open the door for 5 seconds
		print("Unlocking door for five seconds")
		GPIO.output(11, GPIO.HIGH)
		time.sleep(5)
		GPIO.output(11, GPIO.LOW)
		print("Door re-locked door")
		return
	else:
#        if self.path == "mypage.html":
		self.send_response(200)
        	self.send_header('Content-type', 'text/html')
	        self.end_headers()
        	self.wfile.write("<html><head><title>sudo door</title>")
        	self.wfile.write("<script type='text/javascript'>")
        	self.wfile.write("  function go() {")
        	self.wfile.write("    document.location = '/'+document.getElementById('wasspord').value;")
        	self.wfile.write("    return false;")
        	self.wfile.write("  }")
		self.wfile.write("</script></head>")
		self.wfile.write("<body>")             
	        self.wfile.write("<h1>sudo room</h1>")	        
	        self.wfile.write("<h2>speak friend and enter</h2>")	        
	        self.wfile.write("<form onsubmit='go(); return false'")
	        self.wfile.write("<p><input id='wasspord' type='text'/>")
	        self.wfile.write("<input type='button' onclick='go()' value='access' /></p>")
        	self.wfile.write("</body></html>")
	        return
#            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

handler = MyHandler
server = SocketServer.TCPServer(("192.168.168.1",80), handler)
server.serve_forever()
