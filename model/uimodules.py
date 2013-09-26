#coding:utf-8

import tornado.web
import sys, os, re, random, math, urllib.request, urllib.error, urllib.parse, time, pickle, numpy, string

from lib import onlineldavb
from lib import wikirandom

class Topic(tornado.web.UIModule):
	"""
	Displays topics fit by onlineldavb.py. The first column gives the
	(expected) most prominent words in the topics, the second column
	gives their (expected) relative prominence.
	"""

	def render(self, fileName):

		file_obj = open('./static/dictnostops.txt')
		vocab = str.split(file_obj.read())
		test_lambda= numpy.loadtxt(fileName)
		topics = []

		for k in range(0, len(test_lambda)):
			topic = '';
			lambda_k = list(test_lambda[k, :])
			lambda_k = lambda_k / sum(lambda_k)
			temp = list(zip(lambda_k, list(range(0, len(lambda_k)))))

			temp = sorted(temp, key = lambda x: x[0], reverse=True)
			#print 'topic %d:' % (k)
			# feel free to change the "53" here to whatever fits your screen nicely.
			for i in range(0, 10):
				topic += vocab[temp[i][1]] + '\t'
			#print '%20s  \t---\t  %.4f' % (vocab[temp[i][1]], temp[i][0])
			#print
			topics.append(topic)

		return self.render_string('topicTemp.html',title=fileName , topics = topics)


class Graph(tornado.web.UIModule):
	"""
	Displays topics fit by onlineldavb.py. The first column gives the
	(expected) most prominent words in the topics, the second column
	gives their (expected) relative prominence.
	"""

	def render(self, topicNum):

		#file_obj = open('./lib/dictnostops.txt')
		#vocab = str.split(file_obj.read())
		#testlambda= numpy.loadtxt('./data/lambda-20.dat')
		#topics = []
		date = 'Jun 17, 2013'
		topic_file= '\'./static/json/t'+str(topicNum)+'.json\''
		iteration_num = 0
		for root, dirs, files, in os.walk('./data/'):
			for f in files:
				if str(f).find('lambda') >= 0:
					tmp_str = list(filter(str.isdigit, f))
					iter = string.atoi(tmp_str, 10)/10
					if iter > iteration_num:
						iteration_num = iter

		iteration_num += 1
		# for k in range(0, len(testlambda)):
			# topic = '';
			# lambdak = list(testlambda[k, :])
			# lambdak = lambdak / sum(lambdak)
			# temp = zip(lambdak, range(0, len(lambdak)))

			# temp = sorted(temp, key = lambda x: x[0], reverse=True)
			#print 'topic %d:' % (k)
			#feel free to change the "53" here to whatever fits your screen nicely.
			# for i in range(0, 10):
				# topic += vocab[temp[i][1]] + '\t'
			#print '%20s  \t---\t  %.4f' % (vocab[temp[i][1]], temp[i][0])
			#print
			# topics.append(topic)

		return self.render_string('GraphTemp.html', date = date, filename = topic_file, topics = str(topicNum), MaxIter = iteration_num)
