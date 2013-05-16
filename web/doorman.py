#!/usr/bin/env python
#
# this creates two servers:
# - the primary one on https
# - http redirecting to the primary one

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

def closeIn(path):
    words = path.split('_')
    for word in words:
        word = word.lower()
        if word == 'close':
            return True
    return False

def innerDoorOpen():
    s.write('o')

def innderDoorClose():
    s.write('c')

# use iptables to forward these from privileged ports (80, 443)
define("port", default=7836, help="run on the given port", type=int)
define("sslport", default=7837, help="run SSL on the given port", type=int)

# http redirect server
class RedirectHandler(tornado.web.RequestHandler):
    def get(self, path):
        self.redirect('https://'+self.request.host.split(':')[0], permanent=True)

# https primary server
class MainHandler(tornado.web.RequestHandler):
    def get(self, path):
            if secretIn(path):
                if closeIn(path):
                    innerDoorClose()
                    self.write(goodbyeMessage)
                else:
                    innerDoorOpen()
                    self.write(welcomeMessage)
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
        (r"/(.*)", MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        'certfile': 'keys/doorman.pem',
        'keyfile': 'keys/doorman.key',
        'ca_certs': 'keys/doorman.pem',
    })
    http_server.listen(options.sslport)


    # begin serving
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
