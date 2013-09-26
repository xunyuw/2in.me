
#coding:utf-8

import tornado.web
import pickle, string, numpy, getopt, sys, random, time, re, pprint

from lib import onlineldavb
from lib import wikirandom

#from model.entity import Entity

class LDAHandler(tornado.web.RequestHandler):
    def get(self,iterations):
        """
        Downloads and analyzes a bunch of random Wikipedia articles using
        online VB for LDA.
        """

    # The number of documents to analyze each iteration
        batch_size = 64
    # The total number of documents in Wikipedia
        D = 3.3e6
        # The number of topics
        K = 100


        # How many documents to look at
        if len(iterations)<2:
            documents_to_analyze = int(D/batch_size)
        else:
            documents_to_analyze = int(iterations)

        # Our vocabulary
        vocab = file('./lib/dict_no_stops.txt').readlines()
        W = len(vocab)


        # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
        o_lda = onlineldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
        # Run until we've seen D documents. (Feel free to interrupt *much*
        # sooner than this.)
        for iteration in range(0, documents_to_analyze):
            # Download some articles
            (doc_set, article_names) = \
                wikirandom.get_random_wikipedia_articles(batch_size)
            # Give them to online LDA
            (gamma, bound) = o_lda.update_lambda(doc_set)
            # Compute an estimate of held-out perplexity
            (word_ids, word_cts) = onlineldavb.parse_doc_list(doc_set, o_lda._vocab)
            per_word_bound = bound * len(doc_set) / (D * sum(map(sum, word_cts)))
            print('%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
                (iteration, o_lda._rhot, numpy.exp(-per_word_bound)))

        # Save lambda, the parameters to the variational distributions
        # over topics, and gamma, the parameters to the variational
        # distributions over topic weights for the articles analyzed in
        # the last iteration.
            if iteration % 10 == 0:
                    numpy.savetxt('lambda-%d.dat' % iteration, o_lda._lambda)
                    numpy.savetxt('gamma-%d.dat' % iteration, gamma)


#        title = Entity.get('LDA ')
        self.render('lda.html', title = 'None')



