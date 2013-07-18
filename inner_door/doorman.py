#!/usr/bin/env python
#
# this creates two servers:
# - the primary one on https
# - http redirecting to the primary one

import urllib2

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import datetime
import RPi.GPIO as GPIO

from tornado.options import define, options

secrets = []
for line in file('secrets'):
    secrets.append(line.strip())

import serial
s = serial.Serial(port='/dev/ttyAMA0', baudrate=9600)


def secretIn(path):
    words = path.split('_')
    for word in words:
        word = word.lower()
        if word in secrets:
            return True
    return False #if you got to here then you weren't in secrets

def innerDoorOpen():
    s.write('o')


def innerDoorClose():
    s.write('c')

def unlock_elevator():
    GPIO.output(22, GPIO.LOW)

def unlock_elevator_for_seconds(secs):
    unlock_elevator()

    # re-lock elevator in seconds
    tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(seconds=secs), lock_elevator)



def lock_elevator():
    GPIO.output(22, GPIO.HIGH)

def outerDoorOpen():
    if urllib2.urlopen('http://192.168.1.42/simple',None,2).read().strip() != 'buzzed':
        print "OUTSIDE FAILED"

# use iptables to forward these from privileged ports (80, 443)
define("port", default=7836, help="run on the given port", type=int)
define("sslport", default=7837, help="run SSL on the given port", type=int)

# http redirect server
class RedirectHandler(tornado.web.RequestHandler):
    def get(self, path):
        self.redirect('https://'+self.request.host.split(':')[0], permanent=True)

# https primary server
class PortalHandler(tornado.web.RequestHandler):
    def get(self, path):
        messages=[]
        message_code = self.get_argument('message','')
        if message_code == 'fail':
            messages=['<span style="font-weight:bold;font-size:30px;">WRONG PASSWORD</span><div><img src="/static/newman.gif"/></div>']
        if message_code == 'success':
            messages=['<span style="font-weight:bold;font-size:30px;">SUCCESS!</span>']
        self.render("portal.html",messages=messages)
class ActionHandler(tornado.web.RequestHandler):
    def post(self):
        door = 'inside'
        action = 'open'
        secret = self.get_argument('secret','')
        button = self.get_argument('button','default')
        if button == 'OPEN OUTSIDE DOOR':
            door = 'outside'
        elif button == 'OPEN INSIDE DOOR':
            pass
        elif button == 'CLOSE INSIDE DOOR':
            action = 'close'
        elif button == 'UNLOCK ELEVATOR':
            door = 'elevator'            
        elif button == 'UNLOCK ELEVATOR LONG':
            door = 'elevator_long'
        else:
            self.redirect('/?message=fail', permanent=False)
        if action == 'open' and not secretIn(secret):
            self.redirect('/?message=fail', permanent=False)
            return
        if door == 'inside':
            if action == 'close':
                innerDoorClose()
                self.redirect('/?message=success', permanent=False)
            else:
                innerDoorOpen()
                self.redirect('/?message=success', permanent=False)
        elif door == 'outside':
            outerDoorOpen()
            # unlock elevator for 40 seconds
            unlock_elevator_for_seconds(40)
            self.redirect('/?message=success', permanent=False)
        elif door == 'elevator':
            self.redirect('/?message=success', permanent=False)
            unlock_elevator_for_seconds(20)
        elif door == 'elevator_long':
            self.redirect('/?message=success', permanent=False)
            unlock_elevator_for_seconds(40)
        else:
            self.redirect('/?message=fail', permanent=False)

def main():
    tornado.options.parse_command_line()

    # set the GPIO pin for elevator control as output
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(22, GPIO.OUT)
    lock_elevator()

    # create the http redirect server
    redir_app = tornado.web.Application([(r"/(.*)", RedirectHandler)])
    redir_server = tornado.httpserver.HTTPServer(redir_app)
    redir_server.listen(options.port)


    # create the https primary server
    application = tornado.web.Application([
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path":"./static"}),
        (r"/dooeet", ActionHandler),
        (r"/(.*)", PortalHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        'certfile': 'keys/door.sudoroom.org.together.crt',
        'keyfile': 'keys/door.sudoroom.org.key',
    })
    http_server.listen(options.sslport)

    # begin serving
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
