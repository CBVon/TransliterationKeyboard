#coding: utf-8
import os
import cPickle

'''
#?? hindis.txt
with open('..\data\Hindi_latin_task_20180511_Abid_Top1w.txt', 'rb') as fr, open('hindis.txt', 'wb') as fw:
	
	for i in fr.readlines():
		#print i.strip().split()[0]
		fw.write(i.strip().split()[0])
		fw.write('\n')
'''




'''
#??Google???
with open('latins.txt', 'rb') as latins_f, open('hindis.txt', 'rb') as hindis_f, \
	open('..\data\Hindi_latin_task_20180511_Google_Top1w.txt', 'wb') as Google:
	
	latins = latins_f.readlines()
	hindis = hindis_f.readlines()
	
	for i in xrange(len(latins)):
		Google.write(hindis[i].strip())
		Google.write('\t')
		Google.write(latins[i].strip())
		Google.write('\n')
'''

"""
#????, ?? 3??? pkl
#??? ???? ????????
with open('pkl/combine_vk.pkl', 'rb') as f:
	vk = cPickle.load(f)
	print len(vk) 
	vk_l = [[v, k, vk[v][k]] for v in vk for k in vk[v]] 
	print len(vk_l)
	#google_vk
	#5831
	#11207
	
	#combine ???0-7
	#19068
	#48278
	#print len(vk['']) #2514 ??????
	#print len(vk['a']) #787
	#print vk['angara']
	
	vk_l_sort = sorted(vk_l, key= lambda d: -d[-1])
	print vk_l_sort[int(len(vk_l) * 0.25)]
	print vk_l_sort[int(len(vk_l) * 0.5)]
	print vk_l_sort[int(len(vk_l) * 0.6)]
	print vk_l_sort[int(len(vk_l) * 0.8)]
	print vk_l_sort[int(len(vk_l) * 1) - 1]
	'''
	['abhaav', '\xe0\xa4\x85\xe0\xa4\xad\xe0\xa4\xbe\xe0\xa4\xb5', 22]
	['in', '\xe0\xa4\x87\xe0\xa4\xa8\xe0\xa4\x95\xe0\xa5', 6]
	['achhoote', '\xe0\xa4\x85\xe0\xa4\x9b\xe0\xa5\x82\xe0\xa4\xa4\xe0\xa5', 4]
	['Abyabas', '\xe0\xa4\x85\xe0\xa4\xb5\xe0\xa5\x8d\xe0\xa4\xaf\xe0\xa4\xb5\xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xa5\xe0\xa4', 2]
	['Uttavali', '\xe0\xa4\x89\xe0\xa4\xa4\xe0\xa4\xbe\xe0\xa4\xb5\xe0\xa4\xb2\xe0\xa5\x80', 2]
	'''
	
	y25 = vk_l_sort[int(len(vk_l) * 0.25)][2]
	y50 = vk_l_sort[int(len(vk_l) * 0.5)][2]
	print y25, y50 #22, 6 ????, ??3?pkl
	
	vk25 = {} #top25%
	vk50 = {} #top25~50%
	vk100 = {} #top50~100%
	
	for v in vk:
		for k in vk[v]:
			if vk[v][k] > y25:
				#vk25
				if v not in vk25:
					vk25[v] = {k: vk[v][k]}
				else:
					vk25[v][k] = vk[v][k]
			elif vk[v][k] > y50:
				#vk50
				if v not in vk50:
					vk50[v] = {k: vk[v][k]}
				else:
					vk50[v][k] = vk[v][k]
			else:
				#vk100
				if v not in vk100:
					vk100[v] = {k: vk[v][k]}
				else:
					vk100[v][k] = vk[v][k]
	
	pkl_25 = open('pkl/combine/combine_vk25.pkl', 'wb')
	pkl_50 = open('pkl/combine/combine_vk50.pkl', 'wb')
	pkl_100 = open('pkl/combine/combine_vk100.pkl', 'wb')
	cPickle.dump(vk25, pkl_25)
	cPickle.dump(vk50, pkl_50)
	cPickle.dump(vk100, pkl_100)
"""
	
'''
pkl_dir = './pkl/combine'
files = [os.path.join(pkl_dir, i) for i in os.listdir(pkl_dir)]
print files
preVk_count = [cPickle.load(open(i, 'rb')) for i in files]
print len(preVk_count[0]), len(preVk_count[1]), len(preVk_count[2]) #3713 6588 14951
'''









		
		
