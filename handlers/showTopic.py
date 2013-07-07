#coding:utf-8

import tornado.web
import sys, os, re, random, math, urllib2, time, cPickle, numpy

from lib import onlineldavb
from lib import wikirandom

class showTopicHandler(tornado.web.RequestHandler):
    def get(self):
	"""
	Displays topics fit by onlineldavb.py. The first column gives the
	(expected) most prominent words in the topics, the second column
	gives their (expected) relative prominence.
	"""
	fileName = './data/lambda-90.dat'

	self.render('showTopic.html',title=fileName)

