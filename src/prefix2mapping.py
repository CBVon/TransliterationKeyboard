#coding: utf-8

import sys
import os
import copy
import cPickle
	

def readData(path): 
	file = open(path, 'rb')
	#return {i.split()[0]: i.split()[1] for i in file.readlines()[: 100] if len(i.split()) == 2} #小样例测试
	return {i.split()[0]: i.split()[1] for i in file.readlines() if len(i.split()) == 2}

	
data_dir = '..\data'
files = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
hindi2latins = [readData(i) for i in files]


def biPrefix(k1, k2, v1, v2):
	#input: 4个str
	#output: 2个str;分别是str1和str2,str3和str4的共同前缀
	k = ''
	v = ''
	for i in xrange(min(len(k1), len(k2))):
		if k1[i] == k2[i]:
			k += k1[i]
		else:
			break
	for i in xrange(min(len(v1), len(v2))):
		if v1[i] == v2[i]:
			v += v1[i]
		else:
			break
	return k, v


def update_preKv_count(hindi2latin, preKv_count):
	#主要目的: 利用hindi2latin 刷新preKv_count
	
	k_maxPreLen = {} #{k: maxPreLen}
	v_maxPreLen = {} #{k: maxPreLen}
		
	for i in hindi2latin:
		for j in hindi2latin:
			if i != j:
				k, v = biPrefix(i, j, hindi2latin[i], hindi2latin[j])
				if k == '':
					continue
				if k not in preKv_count:
					preKv_count[k] = {v: 1}
				elif v not in preKv_count[k]:
					preKv_count[k][v] = 1
				else:
					preKv_count[k][v] += 1
				#update k_maxPreLen
				if i not in k_maxPreLen or len(k) > k_maxPreLen[i]:
					k_maxPreLen[i] = len(k)
					v_maxPreLen[i] = len(v)
				if j not in k_maxPreLen or len(k) > k_maxPreLen[j]:
					k_maxPreLen[j] = len(k)
					v_maxPreLen[j] = len(v)
	return k_maxPreLen, v_maxPreLen #副产物 #服务于二次刷新


def proccess(files, hindi2latins):
	
	for index in xrange(len(hindi2latins)): #控制 xrange 范围, 来获取对应的 vk_mapping
		
		print "index : " + str(index)
		print files[index] #..\data\Hindi_latin_task_20180511_Abid_Top1w.txt
		hindi2latin = hindi2latins[index] #dict类型  #hindi2latin['अपकेंद्री'] #apkendre #apakendree 存在一词多音,习惯现象
		
		preKv_count = {} #{k:{v: count}} 
		k_maxPreLen, v_maxPreLen = update_preKv_count(hindi2latin, preKv_count)
		#print len(preKv_count) #Abid: 有6688组共同前缀
		
		avg_len = 0.0
		for i in preKv_count:
			avg_len += float(len(preKv_count[i]))
		avg_len /= float(len(preKv_count)) #avg_len=1.65056818182 对每个hindi前缀的发音稳定性;Abid
		
		#二次发现
		hindi2latin_next = {}
		for k in hindi2latin:
			if k in k_maxPreLen:
				new_k = k[k_maxPreLen[k]: ] 
				v = hindi2latin[k]
				new_v = v[v_maxPreLen[k]: ] #hindi2latin[k] = v
				
				if new_k != '' and new_v != '':
					#print new_k, new_v
					hindi2latin_next[new_k] = new_v
		update_preKv_count(hindi2latin_next, preKv_count)
		#print len(preKv_count) #Abid: 二次刷新后 有8278组共同前缀
		
		avg_len = 0.0
		for i in preKv_count:
			avg_len += float(len(preKv_count[i]))
		avg_len /= float(len(preKv_count)) #avg_len=1.71261174197 对每个hindi前缀的发音稳定性;Abid
		
		#想清楚,v本身就是声音,只是v中音标比如 a 有波动性/多义性
		#preKv_count 相当于, 给出所有的 hindi到latin发音的 映射
		pkl_file = 'pkl\\' + str(index) + '_kv.pkl'
		cPickle.dump(preKv_count, open(pkl_file, 'wb'))
	
		#preKv_count 转换到  preVk_count; 倒排
		preVk_count = {} #{v: {k: count}}
		for k in preKv_count:
			for v in preKv_count[k]:
				if v not in preVk_count:
					preVk_count[v] = {k: preKv_count[k][v]}
				else:
					preVk_count[v][k] = preKv_count[k][v]
		#print len(preVk_count) #5310
		avg_len = 0.0
		for i in preVk_count:
			avg_len += float(len(preVk_count[i]))
		avg_len /= float(len(preVk_count)) #avg_len=2.66986817326 #由此可见, 从latin到hindi更加不稳定,不稳定意味不同情况更多
		
		pkl_file = 'pkl\\' + str(index) + '_vk.pkl' #序号0~7
		#pkl_file = 'pkl\google_vk.pkl'
		cPickle.dump(preVk_count, open(pkl_file, 'wb'))


vk_pkl_paths = ['pkl\\' + str(i) + '_vk.pkl' for i in xrange(len(hindi2latins))]
def combine(vk_pkl_paths):
	#获得8个测试文档的对应的pkl的合集
	ans = {}
	for vk_pkl in vk_pkl_paths:
		vk = cPickle.load(open(vk_pkl, 'rb'))
		
		'''
		#print len(vk)
		5310
		5816
		5224
		5295
		5672
		5293
		5502
		5785
		'''
		
		for v in vk:
			if v not in ans:
				ans[v] = {}
			for k in vk[v]:
				if k not in ans[v]:
					ans[v][k] = vk[v][k]
				else:
					ans[v][k] += vk[v][k]
	#print len(ans) #19068
	pkl_file = 'pkl\\conbine_vk.pkl'
	cPickle.dump(ans, open(pkl_file, 'wb'))

	return ans
		
		
if __name__ == "__main__":
	
	hindi2latins = [readData('../data/Hindi_latin_task_20180511_Google_Top1w.txt')] #只处理 google_vk
	proccess(files, hindi2latins) #单独生成每一个
	#combine(vk_pkl_paths) #生成combine
	
	'''
	index : 0
	..\data\Hindi_latin_task_20180511_Abid_Top1w.txt
	index : 1
	..\data\Hindi_latin_task_20180511_Lakshya_finished1w.txt
	index : 2
	..\data\Hindi_latin_task_20180511_Navpreet_Top1w.txt
	index : 3
	..\data\Hindi_latin_task_20180511_PalTop1w.txt
	index : 4
	..\data\Hindi_latin_task_20180511_Shukla_Top1w.txt
	index : 5
	..\data\Hindi_latin_task_20180511_Singh_Top1w.txt
	index : 6
	..\data\Hindi_latin_task_20180511_Sudir_Top1w.txt
	index : 7
	..\data\Hindi_latin_task_20180511_Sudir_Top1w_Fahad.txt
	'''							
	
	
	
	
	
	
	
	
	
	
	

	
	
			
	
	
	
	
	
	
	
	
	
	
	
	'''
	#二次发现 #该策略无法保证 v 一定满足前缀
	hindi2latin_next = copy.deepcopy(hindi2latin)
	#砍掉,最长前缀
	for k in hindi2latin_next:
		#k, v
		max_len = len(k)
		while max_len > 0 and k[: max_len] not in preKv_count:
			max_len -= 1
		if max_len == 0: #没找到
			continue
		
		pre = k[: max_len]
		max_count = 0
		max_v = '' #找对应最长v前缀    '某hindi串':{'pre1': count1, 'pre2': count2} #目的就是找置信度最高的
		for v in preKv_count[pre]:
			if preKv_count[pre][v] > max_count:
				max_count = preKv_count[pre][v]
				max_v = v
		
		v = hindi2latin_next[k]
		hindi2latin_next.pop(k)
	'''
	
	
	
	
	
	
	
	
	
	
	