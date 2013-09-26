
#coding:utf-8

import tornado.web
import sys, os, json
import pickle, string, numpy, getopt, sys, random, time, re, pprint

from lib import onlineldavb
from lib import wikirandom

#from model.entity import Entity

class genJsonHandler(tornado.web.RequestHandler):
    """
        create or refresh Json file for LDA data.
    """

    def get(self):

        iteration_num = 0
        topics_num = 0
        words_num = 0
        for root, dirs, files, in os.walk('./data/'):
            for f in files:
                if str(f).find('lambda') >= 0:
                    tmp_str = list(filter(str.isdigit, f))
                    iterations = string.atoi(tmp_str, 10)/10
                    if iterations > iteration_num:
                        iteration_num = iterations
                    if topics_num == 0:
                        test_lambda = numpy.loadtxt(root+f)
                        (topics_num,words_num) = test_lambda.shape
                elif str(f).find('gamma') >= 0:
                    print(('gamma' + f))
        iteration_num += 1
        matrix = numpy.zeros((words_num*iteration_num*topics_num))
        matrix.shape = words_num, iteration_num, topics_num
        #matrix =  [[0 for col in range(iterNum)] for row in range(topicsNum)]
        #for i in range (topicsNum):
        #	for j in range (iterNum):
        #		matrix[i][j] = numpy.zeros(wordsNum)

        print(matrix.shape)
        for root, dirs, files, in os.walk('./data/'):
            for f in files:
                if str(f).find('lambda') >= 0:
                    tmp_str = list(filter(str.isdigit, f))
                    iterations = string.atoi(tmp_str, 10)/10
                    test_lambda = numpy.loadtxt(root+f)
                    (topics_num,words_num) = test_lambda.shape
                    for k in range(0, len(test_lambda)):
                        lambda_k = list(test_lambda[k, :])
                        lambda_k = lambda_k / sum(lambda_k)
                        #print ("k = %d, iter = %d" % (k, iter))
                        #print len(testlambda)
                        #print topics[k].shape
                        for i in range(0, len(lambda_k)):
                            #print ("i = %d, k = %d, iter = %d" % (i, k, iter))
                            matrix[i,iterations,k] = lambda_k[i]

                elif str(f).find('gamma') >= 0:
                    print(('gamma' + f))

        file_obj = open('./lib/dict_no_stops.txt')
        vocab = str.split(file_obj.read())

        for i in range (topics_num):
            out_matrix = []
            f=open('./static/json/t'+ str(i+1) +'.json','w')
            for j in range (words_num):
                out_word = {}
                percent = []
                out_word['word'] = vocab[j]
                for k in range (iteration_num):

                    #print matrix[:,k,i]
                    #temp = matrix[:,k,i]
                    #sortedIndx = [sorted(temp).index(n) + 1 for n in temp]
                    #sortedIndx = [sorted(matrix[:,k,i]).index(n) + 1 for n in matrix[:,k,i]]
                    #print sortedIndx
                    #print ("i = %d, k = %d, j = %d" % (i, k, j))
                    #position = [sortedIndx[k]] + [k]
                    tmp_percentage = [matrix[j,k,i]] + [k]
                    percent.append(tmp_percentage)
                    #print position
                    #print percent
                out_word['percent'] = percent
                out_matrix.append(out_word)

            encoded_json = json.dumps(out_matrix,sort_keys=True)
            print(encoded_json, file=f)
            f.close

        #title = Entity.get('LDA ')
        self.render('index.html', title = 'test')

