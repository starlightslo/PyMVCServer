__author__ = 'Tony'

class Controller(object):
    # Request
    method = None
    path = None
    headers = {}
    controller = None
    action = None
    args = []
    body = None

    # Response
    response = {
        'headers': {}
    }