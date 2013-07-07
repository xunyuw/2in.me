#coding:utf-8

import tornado.ioloop
import sys


from model import entity
from handlers import index
from application import application
from lib import onlineldavb

PORT = '8888'

if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    application.listen(PORT)
    print 'Development server is running at http://127.0.0.1:%s/' % PORT
    print 'Quit the server with CONTROL-C'
    tornado.ioloop.IOLoop.instance().start()
