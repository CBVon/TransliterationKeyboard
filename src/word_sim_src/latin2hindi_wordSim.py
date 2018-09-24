#coding: utf-8

import sys
import os
import copy
import cPickle
import time

from collections import defaultdict 

import difflib


def readData(path): 
	file = open(path, 'rb')
	#return {i.split()[0]: i.split()[1] for i in file.readlines()[: 100] if len(i.split()) == 2} #小样例测试
	return {i.split()[0]: i.split()[1] for i in file.readlines() if len(i.split()) == 2}

	
data_dir = '../../data'
files = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
hindi2latins = [readData(i) for i in files if 'Google' not in i]


train = [] #len(train) = 79723
for i in hindi2latins:
	train += i.items()

train = list(set(train)) #去重 + 乱序 #len(train)=45726 #一个词出现两次或者一次区别不大

test = [readData(i) for i in files if 'Google' in i][0].items() #len(test)=9979


def latin2rankList(latin):
	#input: latin
	#output: rankList
	#method: 直接匹配
	#sim_l = [[difflib.SequenceMatcher(None, latin, train[i][1]).quick_ratio(), train[i][0]] for i in xrange(len(train))]
	'''
	return [i[1] for i in sorted([[difflib.SequenceMatcher(None, latin, train[i][1]).quick_ratio(), train[i][0]] for i in xrange(len(train))], \
		key=lambda d: -d[0])]
	'''
	return [i[1] for i in sorted([[difflib.SequenceMatcher(None, latin, train[i][1]).quick_ratio() 
		if abs(len(set(latin)) - len(set(train[i][1]))) <= 0 else -1,  #set加速, 元素相差过大 则 不必进行编辑距离计算
		train[i][0]] for i in xrange(len(train))], 
		key=lambda d: -d[0])]
		
start_time = time.time()

ind2count = defaultdict(int) 
find_count = 0
for i in xrange(len(test)):
	print "i : " + str(i)
	print "find : " + str(find_count)
	
	rankList = latin2rankList(test[i][1])
	
	this_ret = -1
	if test[i][0] in rankList:
		this_ret = rankList.index(test[i][0])
	print 'this_ret : ' + str(this_ret)
	if this_ret < 10:
		find_count += 1
	ind2count[this_ret] += 1

end_time = time.time()
print "Running time : " + str(end_time - start_time)

ind2count = sorted(ind2count.items(), key=lambda d: d[0])

for i in ind2count:
	print i
'''
i : 9978
find : 9978
this_ret : 0
Running time : 7229.78900003
(0, 8125)
(1, 1228)
(2, 371)
(3, 136)
(4, 65)
(5, 30)
(6, 9)
(7, 8)
(8, 3)
(9, 4)

----------

abs(len(set(latin)) - len(set(train[i][1]))) <= 2

i : 9978
find : 9978
this_ret : 0
Running time : 6084.86000013
(0, 8125)
(1, 1228)
(2, 371)
(3, 136)
(4, 65)
(5, 29)
(6, 9)
(7, 9)
(8, 3)
(9, 4)

-----------

abs(len(set(latin)) - len(set(train[i][1]))) <= 1

i : 9978
find : 9977
this_ret : 0
Running time : 5141.90799999
(0, 8125)
(1, 1228)
(2, 371)
(3, 136)
(4, 65)
(5, 29)
(6, 9)
(7, 8)
(8, 3)
(9, 4)
(14367, 1)
'''











