# coding = utf8
'''处理分词，分词前先调用init函数初始化
'''
import os
import pynlpir
import pickle

'''
{	"n": {  #1.	名词  (1个一类，7个二类，5个三类)
		"n":"名词",
		"nr":"人名",
		"nr1":"汉语姓氏",
		"nr2":"汉语名字",
		"nrj":"日语人名",
		"nrf":"音译人名",
		"ns":"地名",
		"nsf":"音译地名",
		"nt":"机构团体名",
		"nz":"其它专名",
		"nl":"名词性惯用语",
		"ng":"名词性语素"},
	"t": {  #2.	时间词(1个一类，1个二类)
		"t":"时间词",
		"tg":"时间词性语素"},
	"s": {  #3.	处所词(1个一类)
		"s":"处所词"},
	"f": {  #4.	方位词(1个一类)
		"f":"方位词"},
	"v": {  #5.	动词(1个一类，9个二类)
		"v":"动词",
		"vd":"副动词",
		"vn":"名动词",
		"vshi":"动词“是”",
		"vyou":"动词“有”",
		"vf":"趋向动词",
		"vx":"形式动词",
		"vi":"不及物动词（内动词）",
		"vl":"动词性惯用语",
		"vg":"动词性语素"},
	"a": {  #6.	形容词(1个一类，4个二类)
		"a":"形容词",
		"ad":"副形词",
		"an":"名形词",
		"ag":"形容词性语素",
		"al":"形容词性惯用语"},
	"b": {  #7.	区别词(1个一类，2个二类)
		"b":"区别词",
		"bl":"区别词性惯用语"},
	"z": {  #8.	状态词(1个一类)
		"z":"状态词"},
	"r": {  #9.	代词(1个一类，4个二类，6个三类)
		"r":"代词",
		"rr":"人称代词",
		"rz":"指示代词",
		"rzt":"时间指示代词",
		"rzs":"处所指示代词",
		"rzv":"谓词性指示代词",
		"ry":"疑问代词",
		"ryt":"时间疑问代词",
		"rys":"处所疑问代词",
		"ryv":"谓词性疑问代词",
		"rg":"代词性语素"},
	"m": {  #10.	数词(1个一类，1个二类)
		"m":"数词",
		"mq":"数量词"},
	"q": {  #11.	量词(1个一类，2个二类)
		"q":"量词",
		"qv":"动量词",
		"qt":"时量词"},
	"d": {  #12.	副词(1个一类)
		"d":"副词"},
	"p": {  #13.	介词(1个一类，2个二类)
		"p":"介词",
		"pba":"介词“把”",
		"pbei":"介词“被”"},
	"c": {  #14.	连词(1个一类，1个二类)
		"c":"连词",
		"cc":"并列连词"},
	"u": {  #15.	助词(1个一类，15个二类)
		"u":"助词",
		"uzhe":"着",
		"ule":"了 喽",
		"uguo":"过",
		"ude1":"的 底",
		"ude2":"地",
		"ude3":"得",
		"usuo":"所",
		"udeng":"等 等等 云云",
		"uyy":"一样 一般 似的 般",
		"udh":"的话",
		"uls":"来讲 来说 而言 说来",
		"uzhi":"之",
		"ulian":"连 " #（“连小学生都会”）},
	"e": {  #16.	叹词(1个一类)
		"e":"叹词"},
	"y": {  #17.	语气词(1个一类)
		"y":"语气词(delete yg)"},
	"o": {  #18.	拟声词(1个一类)
		"o":"拟声词"},
	"h": {  #19.	前缀(1个一类)
		"h":"前缀"},
	"k": {  #20.	后缀(1个一类)
		"k":"后缀"},
	"x": {  #21.	字符串(1个一类，2个二类)
		"x":"字符串",
		"xx":"非语素字",
		"xu":"网址URL"},
	"w":{   #22.	标点符号(1个一类，16个二类)
		"w":"标点符号",
		"wkz":"左括号", 	#（ 〔  ［  ｛  《 【  〖 〈   半角：( [ { <
		"wky":"右括号", 	#） 〕  ］ ｝ 》  】 〗 〉 半角： ) ] { >
		"wyz":"全角左引号", 	#“ ‘ 『
		"wyy":"全角右引号", 	#” ’ 』
		"wj":"全角句号",	#。
		"ww":"问号",	#全角：？ 半角：?
		"wt":"叹号",	#全角：！ 半角：!
		"wd":"逗号",	#全角：， 半角：,
		"wf":"分号",	#全角：； 半角： ;
		"wn":"顿号",	#全角：、
		"wm":"冒号",	#全角：： 半角： :
		"ws":"省略号",	#全角：……  …
		"wp":"破折号",	#全角：——   －－   ——－   半角：---  ----
		"wb":"百分号千分号",	#全角：％ ‰   半角：%
		"wh":"单位符号"	#全角：￥ ＄ ￡  °  ℃  半角：$
	}
}
'''

NEED_WD = {	"n":"名词",
			"nr":"人名",
			# "nr1":"汉语姓氏",
			# "nr2":"汉语名字",
			# "nrj":"日语人名",
			"nrf":"音译人名",
			"ns":"地名",
			"nsf":"音译地名",
			"nt":"机构团体名",
			"nz":"其它专名",
			"nl":"名词性惯用语",
			"ng":"名词性语素"}

# 需要的词性集合
NEED_WD_SET = set()
# 停止词集合
STOPWD_SET = set()

SP_WORD_DICT = {"nr":"张三", "nrf":"汤姆", "ns":"北京", "nsf":"纽约"}
SP_WORD_SET = set()

def worddiv(mpath):
	'''基础分词, 去除单字根据NEED_WD词性取词, 去除停用词
		mpath需要被被分词的文档, 返回分词后的词组成的list, 不输出词性
	'''
	target_file = open(mpath, "rb")
	target_txt = target_file.read()
	target_file.close()
	ret_list = []
	# target_txt = target_txt.replace('\xa0', ' ').replace('\u3000', ' ').replace('\r', '')
	# 使用简称词性
	gen_str = pynlpir.segment(target_txt, pos_names=None)
	for word in gen_str:
		# 挑选所需的词性的词，去除单字, 0为单个分词, 1为该词词性
		if len(word[0]) > 1 and word[1] in NEED_WD_SET and not word[0] in STOPWD_SET:
			# 人名地名归一
			if word[1] in SP_WORD_SET:
				ret_list.append(SP_WORD_DICT[word[1]])
			else:
				tmp_str = word[0]
				tmp_str = tmp_str.replace('\xa0', '').replace('\u3000', '').replace('\r', '')
				if len(tmp_str) < 2:
					break
				# 数字开头去掉数字
				if '0' <=  tmp_str[0] <= '9':
					tmp_str = tmp_str.strip('1234567890.-')
					if len(tmp_str) >= 2:
						ret_list.append(tmp_str)
				else:
					ret_list.append(tmp_str)
	return ret_list


def wordfreq(rel_path, word_list):
	pass
		# if (word[1] in NEE_WD_SET and len(word[0]) > 3):
		# 	if (word_dict.get(word[0]) == None):
		# 		word_dict[word[0]] = [1, word[1]]
		# 	else:
		# 		# 统计词频
		# 		word_dict[word[0]][0] += 1
	# 由词频反序生成数组
	# word_array = sorted(word_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	# for item in word_dict:
	# 	s = '%s\t%s\t%d\n' % (item[0], item[1][1], item[1][0])
	# 	ret_str = ret_str + s

MIN_WORDS_NUM = 10
def genwordpkl(target_path, rel_path, file_names, dir_names, **kwargs):
	'''对每一个类汇总生成一个pkl文件，每一个文件的分词结果列表的汇总列表
		kwargs中需要有 min_words_num 参数指定训练比例否则默认MIN_WORDS_NUM
		生成二维分词list的pkl文件, 一个维度表示一个文件内的分词数, 一个度维表示文本数量
		生成信息的分词二维信息pkl文件, 0,1表示采用的文本的文件名和分词数, 2,3同理未采用的
	'''
	if len(file_names) == 0:
		return
	origin_path = target_path + rel_path
	pkl_path = target_path + '_pkl/'
	info_path = target_path + '_pkl_info/'
	up_dir = rel_path.split('/')[-2]
	words = []
	target_list = [[], [], [], []]
	min_words_num = kwargs.get('min_words_num')
	if min_words_num is None:
		min_words_num = MIN_WORDS_NUM
	if not os.path.isdir(pkl_path):
		os.mkdir(pkl_path)
		os.mkdir(info_path)

	for mfile in file_names:
		word = worddiv(origin_path + mfile)
		if len(word) < min_words_num:
			# 文件名和分词出的数量
			target_list[2].append(mfile)
			target_list[3].append(str(len(word)))
		else:
			words.append(word)
			target_list[0].append(mfile)
			target_list[1].append(str(len(word)))
	# 写入采用和舍弃的文本名和分词数
	f = open(info_path + up_dir + '.pkl', 'wb')
	pickle.dump(target_list, f)
	f.close()

	# 写入分词list数据
	pkl_path = pkl_path + up_dir + '.pkl'
	f = open(pkl_path, 'wb')
	pickle.dump(words, f)
	f.close()

def pkl2text(file_path, splitter=','):
	'''将一个二维字符list的*.pkl文件转成 csv文件, 即逗号和换行分隔
	'''
	dlist = pickle.load(open(file_path, 'rb'))
	dstr = ''
	for l in dlist:
		dstr += splitter.join(l) + '\n'

	csv_file = open(file_path[:file_path.rfind('.')]+'.csv', 'w', errors='ignore')
	csv_file.write(dstr)
	csv_file.close()

STOPWORDSET_PATH = './stopwords.pkl'
def genstopwordset(mpath):
	'''根据mpath文件来生成停用词的set的pickle文件到 STOPWORDSET_PATH
	'''
	f = open(mpath, 'r', encoding='UTF-8')
	wordset = set()
	word = f.readline()
	while word:
		word = word.replace('\n', '').replace('\r', '')
		if word:
			wordset.add(word)
		word = f.readline()
	f.close()
	f = open(STOPWORDSET_PATH, 'wb')
	pickle.dump(wordset, f)
	f.close()

def getstopwordset():
	'''提取STOPWORDSET_PATH文件内容
	'''
	if os.path.isfile(STOPWORDSET_PATH):
		return pickle.load(open(STOPWORDSET_PATH, 'rb'))
	else:
		print('未使用停用词集合')
		return set()

def init():
	'''初始化
	'''
	# 繁体会导致编码错误?
	pynlpir.open(encoding_errors='ignore')
	# pynlpir.open()
	global STOPWD_SET, NEED_WD_SET, SP_WORD_SET, SP_WORD_DICT
	NEED_WD_SET = NEED_WD.keys()
	STOPWD_SET = getstopwordset()
	SP_WORD_SET = SP_WORD_DICT.keys()



import catdiv

if __name__ == "__main__":
	init()
	# genstopwordset('./stop_words.txt')

	# path = "./tmp/fc.txt"
	# path2 = path[:-4] + "_1" + path[-4:]
	# f = open(path2, 'w')
	# # pickle.dump(str(worddiv(path)), f )
	# f.write(str(worddiv(path)))
	# f.close()

	catdiv.walker('../Data_01_train/jk', (genwordpkl), min_words_num=10)
	# pkl2text('../Data_01_test_pkl/yl.pkl', ',')
	# print(worddiv('./tmp/sc_000258.txt'))
	# print(worddiv('./tmp/sc_000258.txt'))

	# d = worddiv('./tmp/sc_000258.txt')
	# dstr = ' '.join(d)
	# csv_file = open('./d.csv', 'w', encoding='utf8')
	# csv_file.write(dstr)
	# csv_file.close()
	