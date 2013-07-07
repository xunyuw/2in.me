#coding:utf-8

from handlers.index import MainHandler
from handlers.LDA import LDAHandler
from handlers.showTopic import showTopicHandler
from handlers.genJson import genJsonHandler
from handlers.drawGraph import drawGraphHandler


urls = [
    (r'/', MainHandler),
    (r'/lda', LDAHandler),
    (r'/topic', showTopicHandler),
    (r'/refresh', genJsonHandler),
    (r'/graph', drawGraphHandler),
]


