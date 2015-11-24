__author__ = 'Tony'

from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    DEBUG = False
    CONTROLLERS = None
    MODELS = None

    def __init__(self, controllers, models, *args):
        self.CONTROLLERS = controllers
        self.MODELS = models
        BaseHTTPRequestHandler.__init__(self, *args)

    def routing(self):
        controller = 'index'
        action = 'index'
        args = []
        params = self.path.split('/')
        if len(params) > 2:
            controller = params[1]
            if len(params[2]) > 0:
                action = params[2]
            args = params[3:]
        else:
            if len(params[1]) > 0:
                action = params[1]
        return controller, action, args

    def parse(self, method):
        headers = {}
        try:
            if (self.path.endswith('.html')) or (self.path.endswith('.htm')):
                f = open(curdir + sep + self.path)
                data = f.read()
                f.close()
                headers['Content-type'] = 'text/html'
                self.respond(200, headers, data)
            elif (self.path.endswith('.ico')):
                f = open(curdir + sep + self.path)
                data = f.read()
                f.close()
                headers['Content-type'] = 'image/x-icon'
                self.respond(200, headers, data)
            else:
                controller, action, args = self.routing()
                if self.DEBUG:
                    print(controller + ' - ' + action)
                try:
                    myControlelr = getattr(self.CONTROLLERS[controller], controller)
                except:
                    self.send_error(500, 'Can Not Found Controller: %s' % controller)
                    return
                try:
                    action = getattr(myControlelr(), action)
                except:
                    self.send_error(500, 'Can Not Found Controller: %s' % controller)
                    return
                contentLength = self.headers.getheader('content-length')
                body = None
                if contentLength:
                    length = int(contentLength)
                    body = self.rfile.read(length)

                # Set information
                headers['Content-type'] = 'text/plain'
                myControlelr.headers = self.headers
                myControlelr.models = self.MODELS
                myControlelr.method = method
                myControlelr.path = self.path
                myControlelr.controller = controller
                myControlelr.action = action
                myControlelr.args = args
                myControlelr.body = body
                data = action()
                addHeaders = myControlelr.response['headers']
                for key in addHeaders:
                    headers[key] = addHeaders[key]

                # Respond to the client
                self.respond(200, headers, data)
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
        return

    def do_GET(self):
        return self.parse('GET')

    def do_POST(self):
        return self.parse('POST')

    def respond(self, code, headers, data):
        self.send_response(code)
        for key in headers:
            self.send_header(key, headers[key])
        self.end_headers()
        self.wfile.write(data)