#coding:utf-8

import tornado.web

from model.entity import Entity
	
class drawGraphHandler(tornado.web.RequestHandler):
    def get(self):
		topicNum = self.get_argument('t',1)
		title = 'LDA test'
		self.render('graph.html', title = title, topicNum = topicNum)


