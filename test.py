
#coding:utf-8

import sys, os, json
import numpy, re, string
import random
#from model.entity import Entity


def test():
	"""
	create or refresh Json file for LDA data.
	"""
	
	iterNum = 0
	topicsNum = 0
	wordsNum = 0
	for root, dirs, files, in os.walk('./data/'):
		for f in files:
			if str(f).find('lambda') >= 0:
				tmpStr = filter(str.isdigit, f)
				iter = string.atoi(tmpStr, 10)/10	
				if iter > iterNum:
					iterNum = iter
				if topicsNum == 0:
					testlambda = numpy.loadtxt(root+f)
					(topicsNum,wordsNum) = testlambda.shape
			elif str(f).find('gamma') >= 0:
				print ('gamma' + f)
	iterNum = iterNum+1
	matrix = numpy.zeros((wordsNum*iterNum*topicsNum))
	matrix.shape = wordsNum, iterNum, topicsNum
	#matrix =  [[0 for col in range(iterNum)] for row in range(topicsNum)]
	#for i in range (topicsNum):
	#	for j in range (iterNum):
	#		matrix[i][j] = numpy.zeros(wordsNum)	

	print matrix.shape
	for root, dirs, files, in os.walk('./data/'):
		for f in files:
			if str(f).find('lambda') >= 0:
				tmpStr = filter(str.isdigit, f)
				iter = string.atoi(tmpStr, 10)/10
				testlambda = numpy.loadtxt(root+f)
				(topicsNum,wordsNum) = testlambda.shape
				for k in range(0, len(testlambda)):
					lambdak = list(testlambda[k, :])
					lambdak = lambdak / sum(lambdak)
					#print ("k = %d, iter = %d" % (k, iter))
					#print len(testlambda)
					#print topics[k].shape
					for i in range(0, len(lambdak)):
						#print ("i = %d, k = %d, iter = %d" % (i, k, iter))
						if(lambdak[i] >= 0.001):
							matrix[i,iter,k] = lambdak[i]
				
			elif str(f).find('gamma') >= 0:
				print ('gamma' + f)
	
	file_obj = open('./lib/dictnostops.txt')
	vocab = str.split(file_obj.read())
	
	for i in range (topicsNum):
		outMatrix = [] 
		f=open('./static/json/t'+ str(i+1) +'.json','w')
		for j in range (wordsNum):
			outWord = {}
			percent = []
			position = []
			# random color
			colorR = '%02x' %(random.randint(0,255))
			colorG = '%02x' %(random.randint(0,255))
			colorB = '%02x' %(random.randint(0,255))
			
			outWord['word'] = vocab[j]
			outWord['color'] = '#'+ colorR + colorG +colorB
			
			for k in range (iterNum):
				if(matrix[j,k,i] >= 0.001):
				#print matrix[:,k,i]
				#temp = matrix[:,k,i]
				#sortedIndx = [sorted(temp).index(n) + 1 for n in temp]
				#sortedIndx = [sorted(matrix[:,k,i]).index(n) + 1 for n in matrix[:,k,i]]
				#print sortedIndx
				#print ("i = %d, k = %d, j = %d" % (i, k, j))
				#position = [sortedIndx[k]] + [k]
					tmpPer = [matrix[j,k,i]] + [k]	
					tmpPosit = [j] + [k]
					percent.append(tmpPer)
					position.append(tmpPosit)
				#print position
				#print percent
			if(percent):
				outWord['percent'] = percent
				outWord['posit'] = position
				outMatrix.append(outWord)
		
		encodedjson = json.dumps(outMatrix,sort_keys=True)
		print >> f, encodedjson
		f.close
			#print repr(temp)

			#for k in range(0, 10):
			#	topic += vocab[temp[k][1]] + '\t'  
			#	print (vocab[temp[k][1]] + '\t')
			#	print (temp[k][0])
		#print matrix[i]
		
		#numpy.savetxt('.\json\t_%d.json' % i, topics[i])

if __name__ == "__main__":
	test();
