#coding: utf8
"""
###############################################################################################

1. If you want to query one keyword, then you can input the word you want to know.            #

eg: boy                                                                                       #

2. If you want to query two keywords, then there are two different operations you can choose. #

Operator AND:  boy girl                                                                       #

Operator OR:  boy | girl                                                                      #

Operator Minus:  boy - girl                                                                   #

###############################################################################################

"""
print __doc__

import re
import sys
import pickle
import math
import string
import Spimi
import numpy as np

reversedic = {}

def getrevdic():
	global reversedic
	picklefile = './finalpickle.pic'
	pickleread = open(picklefile,'rb')
	reversedic = pickle.load(pickleread)

def leDistance(input_x, input_y):
	xlen = len(input_x) + 1  
	ylen = len(input_y) + 1

	dp = np.zeros(shape=(xlen, ylen), dtype=int)
	for i in range(0, xlen):
		dp[i][0] = i
	for j in range(0, ylen):
		dp[0][j] = j

	for i in range(1, xlen):
		for j in range(1, ylen):
			if input_x[i - 1] == input_y[j - 1]:
				dp[i][j] = dp[i - 1][j - 1]
			else:
				dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
	return dp[xlen - 1][ylen - 1]

def judge2query(quer1,quer2):
	list1 = [] 
	list2 = []
	answer = 2

	if reversedic.has_key(quer1):
		list1 = reversedic[quer1]
	else:
		answer -= 1
	if reversedic.has_key(quer2):
		list2 = reversedic[quer2]
	else:
		answer -= 1
	return answer,list1,list2

def merge2list(list1,list2):
	answer = []
	for a in list1:
		if a in list2:
			answer.append(a)
	return answer

def or2list(list1,list2):
	
	answer2 = list1[:]
	answer2.extend(list2)
	# print answer2
	answer = set(answer2)
	return list(answer)	

def minus2list(list1,list2):
	answer = []
	for a in list1:
		if a not in list2:
			answer.append(a)
	return answer

def onequery(quer1):
	if reversedic.has_key(quer1):
		return reversedic[quer1]
	else:
		return []

def twoquery(quer1,quer2,operator3):
	answer,list1,list2 = judge2query(quer1,quer2)
	if answer == 0:
		return []
	if answer == 1:
		if len(list1) == 0:
			return list2
		else:
			return list1

	if operator3 == ' ':
		list3 = merge2list(list1,list2)
		return list3
	if operator3 == '|':
		list3 = or2list(list1,list2)
		return list3
	if operator3 == '-':
		list3 = minus2list(list1,list2)
		return list3

if __name__ == '__main__':
	getrevdic()

	while 1:
		string = raw_input("Input your query:\n")
		string = string.lower()
		splist = string.split(" ")
		anslist = []
		candatate = []
		if len(splist) == 1:
			print 1
			# print splist[0]
			anslist = onequery(splist[0])
			#print "^^^^^^^^^some possible options^^^^^^^^^^"
			for keyss in reversedic.keys():
				if leDistance(keyss,splist[0])==1:
					candatate.append(keyss)
					
		elif len(splist) == 2:
			print 2
			anslist = twoquery(splist[0],splist[1],' ')
		elif len(splist) == 3:
			print 3
			anslist = twoquery(splist[0],splist[2],splist[1])
		else:
			print "The error format, please input the correct one.\n"
			continue

		print "^^^^^^^^^some possible options^^^^^^^^^^"
		print "Maybe you want to know:  "
		for cand in candatate:
			print cand,",\t"
		print "if then, please change the keywords."
		# for keyss in reversedic.keys():
		# 	if leDistance(keyss,)
		# print anslist
		print "^^^^^^^^^^^^^^^^^Answer^^^^^^^^^^^^^^^\n"
		if len(anslist) == 0:
			print "No Answer satifies the query."
		else:
			anslist = sorted(anslist)
			print "The ID of the query ",string,"'s answer is: \n"
			for a in anslist:
				print a,"\t"
			print "\n"

