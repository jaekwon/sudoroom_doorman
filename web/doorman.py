#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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

def doorOpen():
    s.write('o')

def doorClose():
    s.write('c')

# use iptables to forward these from privileged ports (80, 443)
define("port", default=7836, help="run on the given port", type=int)
define("sslport", default=7837, help="run SSL on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self, path):
            if secretIn(path):
                if closeIn(path):
                    doorClose()
                    self.write(goodbyeMessage)
                else:
                    doorOpen()
                    self.write(welcomeMessage)
            else:
                self.render(denyTemplate)

class RedirectHandler(tornado.web.RequestHandler):
    def get(self, path):
        self.redirect('https://'+self.request.host.split(':')[0], permanent=True)

def main():
    tornado.options.parse_command_line()
    redir_app = tornado.web.Application([(r"/(.*)", RedirectHandler)])
    redir_server = tornado.httpserver.HTTPServer(redir_app)
    redir_server.listen(options.port)
    application = tornado.web.Application([
        (r"/images/(.*)", tornado.web.StaticFileHandler, {"path":"./images"}),
        (r"/(.*)", MainHandler),

    ])
    # generate these with openssl
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={
        'certfile': 'keys/doorman.pem',
        'keyfile': 'keys/doorman.key',
        'ca_certs': 'keys/doorman.pem',
    })
    http_server.listen(options.sslport)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

# msp4302553
