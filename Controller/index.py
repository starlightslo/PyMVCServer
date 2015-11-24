__author__ = 'Tony'

import PyMVCController

class index(PyMVCController.Controller):
    def index(self):
        self.response['headers']['Content-type'] = 'text/html'
        return '<center><h1>Hello PyMVCServer</h1></center>'

    def add(self):
        a = 0
        b = 0
        if len(self.args) == 2:
            a = int(self.args[0])
            b = int(self.args[1])
        return self.models['test_function'].add(a,b)

    def get_pi(self):
        return self.models['test_function'].PI