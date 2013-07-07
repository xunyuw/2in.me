
#coding:utf-8

import tornado.web
import sys
import cPickle, string, numpy, getopt, sys, random, time, re, pprint

from lib import onlineldavb
from lib import wikirandom

#from model.entity import Entity

class LDAHandler(tornado.web.RequestHandler):
    def get(self,iters):
	"""
    	Downloads and analyzes a bunch of random Wikipedia articles using
    	online VB for LDA.
    	"""

 	# The number of documents to analyze each iteration
    	batchsize = 64
   	# The total number of documents in Wikipedia
    	D = 3.3e6
    	# The number of topics
    	K = 100


    	# How many documents to look at
    	if (len(iters) < 2):
        	documentstoanalyze = int(D/batchsize)
    	else:
        	documentstoanalyze = int(iters)

    	# Our vocabulary
    	vocab = file('./lib/dictnostops.txt').readlines()
    	W = len(vocab)


    	# Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
	olda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
    	# Run until we've seen D documents. (Feel free to interrupt *much*
    	# sooner than this.)
    	for iteration in range(0, documentstoanalyze):
        	# Download some articles
        	(docset, articlenames) = \
            	wikirandom.get_random_wikipedia_articles(batchsize)
        	# Give them to online LDA
        	(gamma, bound) = olda.update_lambda(docset)
        	# Compute an estimate of held-out perplexity
        	(wordids, wordcts) = onlineldavb.parse_doc_list(docset, olda._vocab)
        	perwordbound = bound * len(docset) / (D * sum(map(sum, wordcts)))
        	print '%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
            	(iteration, olda._rhot, numpy.exp(-perwordbound))

        # Save lambda, the parameters to the variational distributions
        # over topics, and gamma, the parameters to the variational
        # distributions over topic weights for the articles analyzed in
        # the last iteration.
        	if (iteration % 10 == 0):
            		numpy.savetxt('lambda-%d.dat' % iteration, olda._lambda)
            		numpy.savetxt('gamma-%d.dat' % iteration, gamma)


#        title = Entity.get('LDA ')
        self.render('lda.html', title = title)



