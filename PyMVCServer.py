__author__ = 'Tony'

import sys
import os
from BaseHTTPServer import HTTPServer

import PyMVCHandler

class Core:
    DEBUG = False
    CONTROLLERS = {}
    MODELS = {}

    server = None

    def __init__(self):
        controllerPath = os.getcwd() + '/Controller/'
        self.loadController(controllerPath)
        modelPath = os.getcwd() + '/Model/'
        self.loadModel(modelPath)

    def loadModel(self, path):
        from os import listdir
        from os.path import isfile, join
        try:
            for model in listdir(path):
                if isfile(join(path, model)):
                    # Ignore __init__.py
                    if not model.startswith('__init__'):
                        try:
                            model = model[:model.index('.')]
                            sys.path.append(path)
                            customModel = __import__(model)
                            self.MODELS[model] = customModel
                        except:
                            if self.DEBUG:
                                print('Load ' + model + ' model failed.')
        except:
            return False
        return True

    def loadController(self, path):
        from os import listdir
        from os.path import isfile, join
        try:
            for controller in listdir(path):
                if isfile(join(path, controller)):
                    # Ignore __init__.py
                    if not controller.startswith('__init__'):
                        try:
                            controller = controller[:controller.index('.')]
                            sys.path.append(path)
                            customController = __import__(controller)
                            self.CONTROLLERS[controller] = customController
                        except:
                            if self.DEBUG:
                                print('Load ' + controller + ' controller failed.')
        except:
            return False
        return True

    def start(self, port):
        def handler(*args):
            PyMVCHandler.Handler(self.CONTROLLERS, self.MODELS, *args)
        self.server = HTTPServer(('', port), handler)
        self.server.serve_forever()

    def stop(self):
        if(not self.server is None):
            self.server.socket.close()
