__author__ = 'Tony'

import PyMVCServer

PORT = 8080

def main():
    server = PyMVCServer.Core()
    try:
        server.start(PORT)
    except (KeyboardInterrupt, SystemExit) as e:
        server.stop()

if __name__ == '__main__':
    main()
