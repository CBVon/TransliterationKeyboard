#coding: utf-8

import sys
import os
import copy
import cPickle
import time

import difflib

import prefix2mapping


pkl_ind = -1#[0 ~ 7] ; -1代表使用combine_vk.pkl
test_file_ind = 1#[0 ~ 7]


pkl_file = ''
if pkl_ind == -1:
	pkl_file = './pkl/combine_vk.pkl'
else:
	pkl_file = './pkl/' + str(pkl_ind) + '_vk.pkl'
#pkl_file = './pkl/preVk_count.pkl'
#cPickle.dump(preVk_count, open(pkl_file, 'wb'))
preVk_count = cPickle.load(open(pkl_file, 'rb'))

latinPre_maxlen = max([len(i) for i in preVk_count.keys()]) #latin前缀最长前缀为 #latinPre_maxlen = 18


#文件读入
data_dir = '..\data'
files = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
hindi2latins = [prefix2mapping.readData(i) for i in files] #print files[0] = #..\data\Hindi_latin_task_20180511_Abid_Top1w.txt
print 'files : ' + files[test_file_ind]

hindisVob = set() #len(hindisVob) #9980
for i in hindi2latins:
	for j in i:
		hindisVob.add(j)

truncation_length = 100
def latin2hindi_onlyPreLen(latin): #由latin 得到 hindi_pro, 最长匹配原则
	#input: latin
	#output: hindi_pro
	#method: 利用preVk_count, 进行最长前缀匹配
	hindi_pro = {'': 1} # {hindi1: 可能性1, hindi2: 可能性2}
	
	while latin != '':
		find = False
		for prelen in xrange(min(latinPre_maxlen, len(latin)), 0, -1): #每次都只找最长前缀可能有问题，最长前缀说不定会很微弱
			if latin[: prelen] in preVk_count:
				#拼接当前hindi & preVk_count[ latin[: prelen] ] {hindi1: count1, hindi2: count2}
				new_hindi_pro = {}
				for i in hindi_pro:
					for j in preVk_count[ latin[: prelen] ]:
						new_hindi_pro[ i + j ] = hindi_pro[i] * preVk_count[ latin[: prelen] ][j] * prelen #越长越关键
				
				#截断new_hindi, 避免组合爆炸
				if len(new_hindi_pro) > truncation_length:
					new_hindi_pro = dict(sorted(new_hindi_pro.items(), key= lambda d: -d[1])[: truncation_length])
				
				hindi_pro = new_hindi_pro
				latin = latin[prelen: ]
				find = True
				break
		
		if not find:
			latin = latin[1: ]
	return hindi_pro

	
pkl_dir = './pkl/combine'
files = [os.path.join(pkl_dir, i) for i in os.listdir(pkl_dir)]
preVk_count_l = [cPickle.load(open(i, 'rb')) for i in files]
def latin2hindi(latin): #由latin 得到 hindi_pro, 频度划分(.25 ~ .50 ~ 1.00), + 最长频度
	#input: latin
	#output: hindi_pro
	#method: 利用preVk_count, 进行频度划分 + 最长前缀匹配
	hindi_pro = {'': 1} # {hindi1: 可能性1, hindi2: 可能性2}
	
	while latin != '':
		find = False
		for preVk_count in preVk_count_l:
		
			for prelen in xrange(min(latinPre_maxlen, len(latin)), 0, -1): #每次都只找最长前缀可能有问题，最长前缀说不定会很微弱
				if latin[: prelen] in preVk_count:
					#拼接当前hindi & preVk_count[ latin[: prelen] ] {hindi1: count1, hindi2: count2}
					new_hindi_pro = {}
					for i in hindi_pro:
						for j in preVk_count[ latin[: prelen] ]:
							new_hindi_pro[ i + j ] = hindi_pro[i] * preVk_count[ latin[: prelen] ][j] * prelen #越长越关键
					
					#截断new_hindi, 避免组合爆炸
					if len(new_hindi_pro) > truncation_length:
						new_hindi_pro = dict(sorted(new_hindi_pro.items(), key= lambda d: -d[1])[: truncation_length])
					
					hindi_pro = new_hindi_pro
					latin = latin[prelen: ]
					find = True
					break
		
		if not find:
			latin = latin[1: ]
	return hindi_pro


edit_dis_limit = 2 #在模糊匹配, 相似度量步骤中, 编辑距离<=edit_dis_limit, 即算作正例

'''
# get_edit_dis
def edit_dis(a, b): #误差太大
	if abs(len(a) - len(b)) <= edit_dis_limit and abs(len(set(a)) - len(set(b))) <= edit_dis_limit:
		return True
	return False

	
def edit_dis2(a, b): #效果不错,效率太低
	
	if abs(len(a) - len(b)) > edit_dis_limit:
		return edit_dis_limit + 100
	
	#dp[len(a)][len(b)] #利用滚动数组压缩空间
	old = [i for i in xrange(len(a) + 1)]
	new = [0 for i in xrange(len(a) + 1)]
	for i in xrange(len(b)):
		for j in xrange(1, len(a) + 1):
			#new[j] = dp[i][j]
			new[j] = min(old[j], new[j - 1]) + 1
			if b[i] == a[j - 1]:
				new[j] = min(new[j], old[j - 1])
			else:
				new[j] = min(new[j], old[j - 1] + 1)
		old = new
		new = [0 for i in xrange(len(a) + 1)]
	return old[len(a)]
	

print edit_dis('abc', 'abd')
print edit_dis('snowy', 'sunny')
print edit_dis('abc', '')
'''		
	

def latin2rankList(latin):
	#input: latin
	#output: rankList
	#method: 完全匹配 + 近似匹配
	
	#hindi_pro = latin2hindi(latin)
	#hindi_pro = latin2hindi_onlyPreLen(latin) 
	hindi_pro = dict(latin2hindi(latin).items() + latin2hindi_onlyPreLen(latin).items())#very_work #https://www.cnblogs.com/dkblog/archive/2012/02/02/2336089.html
	rank_ans = []
	
	#完全匹配
	filter_hindis = {}
	for hindi in hindi_pro:
		if hindi in hindisVob:
			filter_hindis[hindi] = hindi_pro[hindi]
	
	rank_ans += [item[0] for item in sorted(filter_hindis.items(), key=lambda d: -d[1])]
	
	#近似匹配, 对hindisVob 每个词, 计算 和hindi_pro中词编辑距离 ≤ edit_dis_limit的数目, 作为 近似rank依据
	word2limitCount = {} #{word1: count1} #单词：分数 
	hindi_pro = dict(sorted(hindi_pro.items(), key= lambda d: -d[1])[: min(5, len(hindi_pro))]) #避免计算过多 hindi
	
	for word in hindisVob:
		#print word
		#this_limitCount = 0
		thisdiff = 0.0
		#print len(hindi_pro)
		for hindi in hindi_pro:
			'''
			if edit_dis(word, hindi):
				this_limitCount += 1
			'''
			thisdiff += difflib.SequenceMatcher(None, word, hindi).quick_ratio() #ref: https://docs.python.org/2/library/difflib.html
		word2limitCount[word] = thisdiff
	rank_ans += [word[0] for word in sorted(word2limitCount.items(), key=lambda d: -d[1])[: 1000]] #取相似度最高top10 #top1000做序号统计
	return rank_ans
	

if __name__ == '__main__':
	
	hindi2latin = hindi2latins[test_file_ind]
	test_x = hindi2latin.values() #len(test_x) = 9979
	test_y = hindi2latin.keys() #len(test_y) = 9979
	
	'''
	complete_find_count = 0
	
	for i in xrange(len(test_x)):
		hindis = latin2hindi(test_x[i])
		
		filter_hindis = {}
		for hindi in hindis:
			if hindi in hindisVob:
				filter_hindis[hindi] = hindis[hindi]

		if test_y[i] in filter_hindis:
			complete_find_count += 1
		#else:
			#print test_x[i], test_y[i],
			#print 'noooooo find'
	
	print complete_find_count, len(test_x) 
	#完全匹配, 说明截断100效果比较好
	#10截断：    2969 9979
	#100截断:    4423 9979 #比较好
	#1000截断：  4791 9979
	#10000截断： 4847 9979
	#100000截断：4859 9979
	'''
	
	start_time = time.time()
	complete_find_count = 0
	
	ret_list = [] #返回每个查询所处的 rank位置, 越靠前越好
	
	with open('write.txt','wb') as f:
		for i in xrange(len(test_x)):
			print "i : " + str(i)
			print "find : " + str(complete_find_count)
			
			rank_ans = latin2rankList(test_x[i])
			
			this_ret = -1
			if test_y[i] in rank_ans:
				this_ret = rank_ans.index(test_y[i]) #当前 排序位次
			print 'this_ret : ' + str(this_ret)
			ret_list.append(this_ret)
			
			if test_y[i] in rank_ans[: 10]:
				complete_find_count += 1
				#print "finddddddddd"
			"""
			#错误打印
			else:
				'''
				print test_y[i]
				for ans in rank_ans:
					print ans
				'''
				f.write(test_y[i])
				f.write('\n')
				for ans in rank_ans:
					f.write(ans)
					f.write('\n')
				f.write('########## ##########\n')
			"""
	end_time = time.time()
	
	cPickle.dump(this_ret, open('ret/' + str(end_time) + '.pkl', 'wb'))
	
	print "Running time : " + str(end_time - start_time)
	print complete_find_count, len(test_x) 
	
	print 'pkl_ind : ' + str(pkl_ind)
	print 'test_file_ind : ' + str(test_file_ind)
	print 'file : ' + files[test_file_ind]
	
	#complete_find_count, len(test_x) ： 4423 9979; 完全找到, Abid 测 Abid
	
	#模糊匹配 top10, Abid 测 Abid
	#Running time : 8393.70600009 || 8389.66100001
	#7150 9979
	
	#Abid 测 Lakshya
	#Running time : 10997.464
	#4176 9974
	
	#combine 测 Abid
	#Running time : 8509.90499997
	#7007 9979
	
	#combine 测 Lakshya
	#Running time : 8666.61800003
	#8098 9974
	
	##### #####
	'''
	Running time : 17543.3840001
	7150 9979
	pkl_ind : 0
	test_file_ind : 0
	file : ..\data\Hindi_latin_task_20180511_Abid_Top1w.txt
	
	Running time : 17076.4009998
	7007 9979
	pkl_ind : -1
	test_file_ind : 0
	file : ..\data\Hindi_latin_task_20180511_Abid_Top1w.txt
	
	Running time : 17813.5240002
	8821 9974
	pkl_ind : 1
	test_file_ind : 1
	file : ..\data\Hindi_latin_task_20180511_Lakshya_finished1w.txt
	
	Running time : 17050.0739999
	8098 9974
	pkl_ind : -1
	test_file_ind : 1
	file : ..\data\Hindi_latin_task_20180511_Lakshya_finished1w.txt
	
	Running time : 16309.55
	7966 9979
	pkl_ind : 2
	test_file_ind : 2
	file : ..\data\Hindi_latin_task_20180511_Navpreet_Top1w.txt
	
	Running time : 17496.914
	7664 9979
	pkl_ind : -1
	test_file_ind : 2
	file : ..\data\Hindi_latin_task_20180511_Navpreet_Top1w.txt
	
	Running time : 17021.5109999
	6489 9970
	pkl_ind : 3
	test_file_ind : 3
	file : ..\data\Hindi_latin_task_20180511_PalTop1w.txt
	
	Running time : 17541.1689999
	6572 9970
	pkl_ind : -1
	test_file_ind : 3
	file : ..\data\Hindi_latin_task_20180511_PalTop1w.txt
	
	----- -----
	
	Running time : 18352.164
	7917 9887
	pkl_ind : 4
	test_file_ind : 4
	file : ..\data\Hindi_latin_task_20180511_Shukla_Top1w.txt
	
	Running time : 15824.0280001
	7769 9887
	pkl_ind : -1
	test_file_ind : 4
	file : ..\data\Hindi_latin_task_20180511_Shukla_Top1w.txt
	
	Running time : 9073.57000017
	7108 9980
	pkl_ind : 5
	test_file_ind : 5
	file : ..\data\Hindi_latin_task_20180511_Singh_Top1w.txt
	
	Running time : 9557.3670001
	6940 9980
	pkl_ind : -1
	test_file_ind : 5
	file : ..\data\Hindi_latin_task_20180511_Singh_Top1w.txt
	
	Running time : 18520.654
	7875 9975
	pkl_ind : 6
	test_file_ind : 6
	file : ..\data\Hindi_latin_task_20180511_Sudir_Top1w.txt
	
	Running time : 8613.33300018
	7531 9975
	pkl_ind : -1
	test_file_ind : 6
	file : ..\data\Hindi_latin_task_20180511_Sudir_Top1w.txt
	
	Running time : 18164.477
	8475 9979
	pkl_ind : 7
	test_file_ind : 7
	file : ..\data\Hindi_latin_task_20180511_Sudir_Top1w_Fahad.txt
	
	Running time : 15456.2409999
	7848 9979
	pkl_ind : -1
	test_file_ind : 7
	file : ..\data\Hindi_latin_task_20180511_Sudir_Top1w_Fahad.txt
	
	----- -----
	
	Running time : 8846.61300015
	8827 9979
	pkl_ind : 1
	test_file_ind : 1
	file : ..\data\Hindi_latin_task_20180511_Google_Top1w.txt
	
	Running time : 8673.398
	8105 9979
	pkl_ind : -1
	test_file_ind : 1 #google
	file : ..\data\Hindi_latin_task_20180511_Google_Top1w.txt
	
	----- -----
	
	分频策略
	Running time : 10342.0929999
	6464 9979
	pkl_ind : -1
	test_file_ind : 1 #google
	file : ./pkl/combine\combine_vk50.pkl 
	
	最长 + 分频
	Running time : 11353.6699998
	8178 9979
	pkl_ind : -1
	test_file_ind : 1
	file : ./pkl/combine\combine_vk50.pkl
	
	'''
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	



