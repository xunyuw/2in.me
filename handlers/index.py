#coding:utf-8

import tornado.web

from model.entity import Entity
	
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        title = 'LDA test'
        self.render('index.html', title = title)


