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

from tornado.options import define, options

#CONSTANTS
welcomeMessage = "liberation"
goodbyeMessage = "sleep is good"
denyTemplate = 'deny.html'
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
            self.render("portal.html")
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
        else:
            self.render(denyTemplate)
        if action == 'open' and not secretIn(secret):
            self.render(denyTemplate)
            return
        if door == 'inside':
            if action == 'close':
                innerDoorClose()
                self.write(goodbyeMessage)
            else:
                innerDoorOpen()
                self.write(welcomeMessage)
        elif door == 'outside':
            outerDoorOpen()
        else:
            self.render(denyTemplate)

def main():
    tornado.options.parse_command_line()


    # create the http redirect server
    redir_app = tornado.web.Application([(r"/(.*)", RedirectHandler)])
    redir_server = tornado.httpserver.HTTPServer(redir_app)
    redir_server.listen(options.port)


    # create the https primary server
    application = tornado.web.Application([
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path":"./images"}),
        (r"/dooeet", ActionHandler),
        (r"/(.*)", PortalHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        'certfile': 'keys/door.sudoroom.org.crt',
        'keyfile': 'keys/door.sudoroom.org.key',
    })
    http_server.listen(options.sslport)

    # begin serving
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
