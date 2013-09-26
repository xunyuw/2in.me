
#coding:utf-8

import sys, os, json
import numpy, re, string
import random
#from model.entity import Entity


def test():
	"""
	create or refresh Json file for LDA data.
	"""
	
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
	#matrix =  [[0 for col in range(iteration_num)] for row in range(topicsNum)]
	#for i in range (topicsNum):
	#	for j in range (iteration_num):
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
					lamb_dak = list(test_lambda[k, :])
					lamb_dak = lamb_dak / sum(lamb_dak)
					#print ("k = %d, iterations = %d" % (k, iterations))
					#print len(test_lambda)
					#print topics[k].shape
					for i in range(0, len(lamb_dak)):
						#print ("i = %d, k = %d, iterations = %d" % (i, k, iterations))
						if lamb_dak[i] >= 0.001:
							matrix[i,iterations,k] = lamb_dak[i]
				
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
			position = []
			# random color
			color_r = '%02x' %(random.randint(0,255))
			color_g = '%02x' %(random.randint(0,255))
			color_b = '%02x' %(random.randint(0,255))
			
			out_word['word'] = vocab[j]
			out_word['color'] = '#'+ color_r + color_g +color_b
			
			for k in range (iteration_num):
				if matrix[j,k,i] >= 0.00:
				#print matrix[:,k,i]
				#temp = matrix[:,k,i]
				#sortedIndex = [sorted(temp).index(n) + 1 for n in temp]
				#sortedIndex = [sorted(matrix[:,k,i]).index(n) + 1 for n in matrix[:,k,i]]
				#print sortedIndex
				#print ("i = %d, k = %d, j = %d" % (i, k, j))
				#position = [sortedInedx[k]] + [k]
					tmp_percentage = [matrix[j,k,i]] + [k]
					tmp_posit = [j] + [k]
					percent.append(tmp_percentage)
					position.append(tmp_posit)
				#print position
				#print percent
			if(percent):
				out_word['percent'] = percent
				out_word['posit'] = position
				out_matrix.append(out_word)
		
		encoded_json = json.dumps(out_matrix,sort_keys=True)
		print(encoded_json, file=f)
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
