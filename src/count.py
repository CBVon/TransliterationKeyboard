#coding: utf-8
import sys
import os


#ref: https://www.ipasource.com/media/ipasource/cms/extra/diction/Latin%20Chart.pdf
#音标id映射：http://en-yinbiao.xiao84.com/yinbiaofayin/   #有发音
latin2interpho = {
	'a': ['6'],
	'æ': ['3'],
	'au': ['11\'8'],
	'ay': ['11\'1'],
	
	'b': ['23'],
	
	#'c': ['36', '22'], 
	'c': ['22'],
	#22表示|k|的音,包含情况最多; 
	#36表示|tf|发shi的音, before [|i|(1)] or [(ai的音)3]
	#28 after ex- and before [|i|(1)] or [(ai的音)3] #exc 设置专门的匹配, 此处 按下不表
	#'cc': ['36', '22\'22'],
	'cc': ['22\'22'],
	#36表示|tf|发shi的音, before [|i|(1)] or [(ai的音)3]
	'ch': ['22'],
	
	#c衍生：
	'cy': ['36\'1'],
	'ccy': ['36\'1'],
	'ci': ['36\'1'],
	'cci': ['36\'1'],
	'ce': ['36\'3'],
	'cce': ['36\'3'],
	'ceu': ['36\'3\'8'],
	'cceu': ['36\'3\'8'],
	
	'd': ['24'],
	
	'e': ['3'],
	'eu': ['3\'8'],
	
	'f': ['26'],
	'ff': ['26\'26'],
	
	#'g': ['39', '25'], #39需要后拼接1、3 #25其余所有情况
	'g': ['25'],
	'gn': ['44\'44'],
	
	#g衍生
	'gy': ['39\'1'],
	'gi': ['39\'1'],
	'ge': ['39\'3'],
	'geu': ['39\'3\'8'],
	
	#'h': ['', '22'], #''表示silent, 只有这两种组合 míhi, níhil发22音
	'h': [''], #情况过少, 忽略'22'
	
	'i': ['1', '46'], #46需要i在两个元音之间, 发 ye 的音 #双元音组合有点多, 此处不剪枝
	
	'j': ['46'],
	
	'k': ['22'],
	
	'l': ['45'],
	'll': ['45\'45'],
	
	'm': ['42'],
	
	#'n': ['43', '44'], #44后跟 22[k] or 25 [g] – (c or g)
	'n': ['43'],
	'nn': ['43\'43'],
	
	#n衍生 
	'nc': ['44\'22'],
	'ncc': ['44\'22\'22'],
	'nch': ['44\'22'], #n不会和c衍生组合, 因为c衍生不发|k|音, 发36|tf|的音
	
	'o': ['10'],
	'œ': ['3'],
	
	'p': ['20'],
	'pp': ['20\'20'],
	'ph': ['26'],
	
	'q': [],
	'qu': ['22\'47'],
	
	'r': ['35'],
	'rr': ['35\'35'],
	
	#'s': ['27', '32'], #32(voiced consonant 浊辅音)最后一个字母, 在外围特判
	's': ['27'],
	'ss': ['27\'27'],
	#'sc': ['28', '27\'22'], #28 shi的音, before [|i|(1)] or [(ai的音)3]
	'sc': ['27\'22'],
	
	#sc衍生
	'scy': ['28\'1'],
	'sci': ['28\'1'],
	'sce': ['28\'3'],
	'sceu': ['28\'3\'8'],
	
	't': ['21'],
	'tt': ['21\'21'],
	'ti': ['21\'27', '21\'1'], #21'27元音之前，before a vowel and after any other letter except s, t, or x; 规则复杂,不剪枝
	'th': ['21'],
	
	'u': ['8', '47'], #47 following ng- or q- and before a vowel ; 规则复杂, 不剪枝
	
	'v': ['31'],
	
	'w': [], #not used in Latin
	
	#'x': ['22\'27', '22'], #22'27 在中间或者结尾 #22需要希腊语特殊写法,很少出现
	'x': ['22\'27'],
	'ex': ['25\'27', '22\'27'], #25'27 元音之前,-h之前,s之前
	'exc': ['22\'28', '22\'27\'22'], #|kf|22'28, before [|i|(1)] or [(ai的音)3]
	
	#exc衍生
	'excy': ['22\'28\'1'],
	'exci': ['22\'28\'1'],
	'exce': ['22\'28\'3'],
	'exceu': ['22\'28\'3\'8'],
	
	
	'y': ['1'],
	'z': ['24\'32'],
} #International Phonetic Alphabet

hindi2interpho = {
	
	#Vowels and Diphthongs, 元音和双元音
	#note1: 只列出元音居于音节开头的部分
	#跟在辅音后的元音可以在语法书中找到
	#音译中，二者没差
	
	#I. Independent vowel characters , 独立元音字符
	#a
	'अ': '6',
	#a~
	'आ': '11',
	#i
	'इ': '1',
	#i~
	'ई': '0',
	#u
	'उ': '8',
	#u~
	'ऊ': '7',
	#r
	'ॠ': '35',
	'ॠ': '35',
	#l
	'ऌ': '45',
	#e
	'ए': '2',
	#ai
	'ऐ': '13',
	#o
	'ओ': '16',
	#au
	'औ': '15',
	
	##### #####
	#II. Abbreviated vowel characters
	#a
	'क': '6',
	#a~
	'का': '11',
	#i
	'क': '1',
	#i~
	'क': '0',
	#u
	'कु': '8',
	#u~
	'कू': '7',
	#r
	'कृ': '35',
	#e
	'क': '2',
	#ai
	'कै': '13',
	#o
	'को': '16',
	#au
	'कौ': '15',
	
	##### #####
	#III. Other symbols
	
	##### #####
	#IV. Consonant characters, 辅音
	'क': '22\'6', #ka
	'ख': '22\'30\'6', #kha
	'ग': '25\'6', #ga
	'घ': '25\'30\'5', #gha
	'ङ': '43\'6', #na
	'च': '36\'6', #cha
	'छ': '36\'30\'6', #chha
	'ज': '46\'6', #ja
	'झ': '46\'30\'6', #jha
	'ञ': '43\'6', #na
	'ट': '21\'6', #ta
	
	'ठ': '21\'30\'6', #tha
	'ड': '24\'6', #ḍa
	'ढ': '24\'30\'6', #ḍha
	'ण': '43\'6', #ṇa
	'त': '21\'6', #ta
	'थ': '21\'30\'6', #tha
	'द': '24\'6', #da
	'ध': '24\'30\'6', #dha
	'न': '43\'6', #na
	'प': '20\'6', #pa
	'फ': '20\'30\'6', #pha
	
	'ब': '23\'6', #ba
	'भ': '23\'30\'6', #bha
	'म': '42\'6', #ma
	'य': '1\'6', #ya
	'र': '35\'6', #ra
	'ल': '45\'6', #la
	'व': '31\'6', #va
	'श': '27\'30\'6', #sha
	'ष': '27\'30\'6', #ṣha
	'स': '27\'6', #sa
	'ह': '30\'6', #ha
	
	'क़': '22\'46\'8\'6', #qa
	'ख़': '22\'30\'6', #ḳha
	'ग़': '25\'6', #ga
	'ज़': '32\'6', #za
	'ड़': '35\'6', #ṙa
	'ढ़': '35\'30\'6', #ṙha
	'फ़': '26\'6', #fa
	
	##### #####
	#V. Ligatures, 联结
	'Hक': '22\'22\'6', #kka
	'Hख': '22\'22\'30\'6', #kkha
	'Hत': '22\'21\'6', #kta
	'HIव': '22\'21\'31\'6', #ktva
	'Hय': '22\'1\'6', #kya
	'J': '22\'35\'6', #kra
	'Hल': '22\'45\'6', #kla
	'Hव': '22\'31\'6', #kva
	'K': '22\'27\'30\'6', #kṣha
	'Lण': '22\'27\'30\'43\'6', #kṣhṇa
	'Lम': '22\'27\'30\'42\'6', #kṣhma
	'Lय': '22\'27\'30\'1\'6', #kṣhya
	'Lव': '22\'27\'30\'31\'6', #kṣhva
	
	'Hस': '22\'27\'6', #ksa
	'Mय': '22\'30\'1\'6', #khya
	'ख़श': '22\'30\'27\'30\'6', #ḳhsha
	'Nद': '25\'24\'6', #gda
	'Nध': '25\'24\'30\'6', #gdha
	'Nन': '25\'43\'6', #gna
	'Nभ': '25\'23\'30\'6', #gbha
	'Nम': '25\'42\'6', #gma
	'Nय': '25\'1\'6', #gya
	'O': '25\'35\'6', #gra
	'Nल': '25\'45\'6', #gla
	'Pन': '25\'30\'43\'6', #ghna
	'Pय': '25\'30\'1\'6', #ghya
	
	'Q': '25\'30\'35\'6', #ghra
	'Rक': '43\'22\'6', #ṅka
	'Rख': '43\'22\'30\'6', #ṅkha
	'Rग': '43\'25\'6', #ṅga
	'Rघ': '43\'25\'30\'6', #ṅgha
	'Sच': '36\'36\'6', #chcha
	'Sछ': '36\'36\'30\'6', #chchha
	'ST': '36\'36\'30\'35\'6', #chchhra
	'Sय': '36\'1\'6', #chya
	'U': '36\'35\'6', #chra
	'Vज': '46\'46\'6', #jja
	'Vझ': '46\'46\'30\'6', #jjha
	'W': '46\'43\'6', #jña
	
	'Vय': '46\'1\'6', #jya 
	'X': '46\'35\'6', #jra
	'Vव': '', #jva
	'Yच': '', #ñcha
	'Yछ': '', #ñchha
	'Yज': '', #ñja
	'Z': '', #ṭṭa
	'[': '', #ṭṭha
	'\\': '', #ṭhṭha
	']ड': '', #ḍḍa
	']ढ': '', #ḍḍha
	'^ढ': '', #ḍhḍha
	'_ट': '', #ṇṭa
	
	'_ठ': '', #ṇṭha
	'_ड': '', #ṇḍa
	'_य': '', #ṇya
	'Iक': '', #tka
	'Iत': '', #tta
	'IIय': '', #ttya
	'IIव': '', #ttva
	'Iथ': '', #ttha
	'Iन': '', #tna
	'Iप': '', #tpa
	'Iम': '', #tma
	'I`य': '', #tmya
	'Iय': '', #tya
	
	'a': '', #tra
	'bय': '', #trya
	'Iव': '', #tva
	'Iस': '', #tsa
	'Icन': '', #tsna
	'Icय': '', #tsya
	'dय': '', #thya
	'e': '', #thra
	'fग': '', #dga
	'g': '', #dda
	'h': '', #ddha
	'i': '', #dbha
	'j': '', #dma
	
	'fय': '', #dya
	'k': '', #dra
	'fव': '', #dva
	'lन': '', #dhna
	'lम': '', #dhma
	'lय': '', #dhya
	'm': '', #dhra
	'lव': '', #dhva
	'nत': '', #nta
	'nIय': '', #ntya
	'na': '', #ntra
	'nथ': '', #ntha
	'nद': '', #nda
	
	'nk': '', #ndra
	'nध': '', #ndha
	'nlय': '', #ndhya
	'nm': '', #ndhra
	'nन': '', #nna
	'nम': '', #nma
	'nय': '', #nya
	'o': '', #nra
	'nव': '', #nva
	'nस': '', #nsa
	'nह': '', #nha
	'pत': '', #pta
	'pIय': '', #ptya
	
	'pन': '', #pna
	'pय': '', #pya
	'q': '', #pra
	'pल': '', #pla
	'pस': '', #psa
	'rय': '', #phya
	'rल': '', #phla
	'sद': '', #bda
	'sन': '', #bna
	'sय': '', #bya
	't': '', #bra
	'uय': '', #bhya
	'v': '', #bhra
	
	'`न': '', #mna
	'`ब': '', #mba
	'`भ': '', #mbha
	'`म': '', #mma
	'`य': '', #mya
	'w': '', #mra
	'`ल': '', #mla
	'`व': '', #mva
	'`ह': '', #mha
	'xय': '', #yya
	'y': '', #yra
	'zक': '', #lka
	'zप': '', #lpa
	
	'zम': '', #lma
	'zय': '', #lya
	'zल': '', #lla
	'zव': '', #lva
	'zस': '', #lsa
	'{य': '', #vya
	'|': '', #vra
	'}च': '', #shcha
	'}Sय': '', #shchya
	'}छ': '', #shchha
	'}न': '', #shna
	'}य': '', #shya
	'~': '', #shra
	
	'}ल': '', #shla
	'}व': '', #shva
	'क': '', #ṣhka
	'J': '', #ṣhkra
	'ट': '', #ṣhṭa
	'': '', #ṣhṭra
	'ठ': '', #ṣhṭha
	'ण': '', #ṣhṇa
	'प': '', #ṣhpa
	'q': '', #ṣhpra
	'म': '', #ṣhma
	'य': '', #ṣhya
	'व': '', #ṣhva
	
	'cक': '', #ska
	'cख': '', #skha
	'cत': '', #sta
	'ca': '', #stra
	'cथ': '', #stha
	'cन': '', #sna
	'cप': '', #spa
	'cफ': '', #spha
	'cम': '', #sma
	'c`य': '', #smya
	'cय': '', #sya
	'': '', #sra
	'cव': '', #sva
	
	'न': '', #hna
	'म': '', #hma
	'य': '', #hya
	'': '', #hra
	'ल': '', #hla
	'व': '', #hva
	
}

print hindi2interpho['ढ़']

def readData(path): 
	file = open(path, 'rb')
	return {i.split()[0]: i.split()[1] for i in file.readlines() if len(i.split()) == 2}

	
def latin2interpho_func(latin): 
	#向右最长匹配 + 规则限制 #可能返回很多很多种组合
	#返回 list[['1', '47', '38'], [], []]
	if latin == '':
		return ['']
	letf = []
	right = []
	if latin[: 3] in latin2interpho:
		letf = latin2interpho[latin[: 3]]
		right = latin2interpho_func(latin[3: ])
	elif latin[: 2] in latin2interpho:
		letf = latin2interpho[latin[: 2]]
		right = latin2interpho_func(latin[2: ])
	else: #一定能找到？
		#print latin[: 1] + "?"
		letf = latin2interpho[latin[: 1]]
		right = latin2interpho_func(latin[1: ])
	
	#combine, left + right
	ans = []
	for i in letf:
		for j in right:
			is_pruning = False
			if (i == '36' or i == '28') and not (j[0] == '1' or j[0] == '3'): #c发shi的音,need before [|i|(1)] or [(ai的音)3]
				is_pruning = True
			if not is_pruning:
				ans.append(i + '\'' + j)
	return ans
 
#print max([len(i) for i in hindi2interpho.keys()]) #6
max_key_len = 6
def hindi2interpho_func(hindi):
	if hindi == '':
		return ''
	ans = ''
	
	pos = 0
	#for i in xrange(len(hindi)):
	while pos < len(hindi):
		jump = False
		for leng in xrange(min(max_key_len, len(hindi) - pos + 1), 0, -1):
			if hindi[pos: pos + leng - 1] in hindi2interpho:
				ans += hindi2interpho[hindi[pos: pos + leng - 1]]
				ans += '\''
				pos += leng
				jump = True
				break
		if not jump:
			pos += 1
		
	return ans
#print len('एक्सट्रीम')
#print hindi2interpho_func('एक्सट्रीम')
	
def final_latin2interpho_func(latin):
	
	if latin[-1] == 's' and latin[-2] in ['b', 'g', 'd', 'v', '', 'r', 'g', 'z', 'm', 'n', 'n', 'u', 'i', 'j', 'l']:
		#return latin2interpho_func(latin[: -1]) + '32\'' #s位于final, 在浊辅音之后, 发 |z|32的音
		before_final = latin2interpho_func(latin[: -1])
		return [i + '32\'' for i in before_final]
	return latin2interpho_func(latin)
	
#预处理得到 top10000中每个hindi对应的音标链
def match(latins):
	#对于每个数据集, 计算每个latin的 [音标链], 然后其中每个latin音标链都去和计算好的hindi音标链计算相似度,
	#相似度到达一定程度(共现字符), 然后计算匹配度Rank, 予以返回	
	# trick: hindi 和 latin 互相去除,对方没有出现的音标字符/ 
	# 对于转移概率, 先做到bi-gram, 类似的引入 这个概念. 同时限制,二者必须同时出现在两个集合当中,否则没有意义,然后归纳总结规律
	hindis = ''
	return hindis
	
if __name__ == '__main__':
	
	data_dir = '..\data'
	files = [os.path.join(data_dir, i) for i in os.listdir(data_dir)]
	#print files
	hindi2latins = [readData(i) for i in files]
	#print len(hindi2latins[3]) #9970
	hindi_set = set([j for i in hindi2latins for j in i.keys()])
	#print len([j for i in hindi2latins for j in i.keys()]) #79723
	#print len(hindi_set) #9980
	unique_hindi2latin = {} #这里只计算, hindi2latins[0]相对其他
	for i in hindi2latins[0]:
		unique = True
		for hindi2latin in hindi2latins[1:2 ]:
			if i in hindi2latin and hindi2latin[i] != hindi2latins[0][i]:
				#print hindi2latin[i], hindi2latins[0][i]
				unique = False
				break
		if unique:
			unique_hindi2latin[i] = hindi2latins[0][i]
	#print len(hindi2latins[0]) #9979
	#print len(unique_hindi2latin) #38 #0 vs 1~7 
	#1912 #0 vs 1   #由此可见差异巨大, 不同地区,不同人标的差距非常大
	#print '11\'8'
	
	#print latin2interpho #打印映射表
	
	hindis = hindi2latins[0].keys()[: 10]
	latins = hindi2latins[0].values()[: 10]
	#print latins
	interphosOfHindis = [hindi2interpho_func(i) for i in hindis[: 10]]
	interphosOfLatins = [final_latin2interpho_func(i) for i in latins[: 10]]
	#print interphosOfLatins
	for i in xrange(len(interphosOfLatins)):
		print hindis[i], interphosOfHindis[i]
		print latins[i], interphosOfLatins[i]
	
	print files[0]
	
	
	
	
	
	
	
	
	
	
	
	
	
	