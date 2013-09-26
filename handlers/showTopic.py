#coding:utf-8

import tornado.web
import sys, os, re, random, math, urllib.request, urllib.error, urllib.parse, time, pickle, numpy

from lib import onlineldavb
from lib import wikirandom

class showTopicHandler(tornado.web.RequestHandler):
	"""
	Displays topics fit by onlineldavb.py. The first column gives the
	(expected) most prominent words in the topics, the second column
	gives their (expected) relative prominence.
	"""

	def get(self):

		file_name = './data/lambda-90.dat'
		self.render('showTopic.html',title=file_name)

