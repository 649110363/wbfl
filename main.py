# coding = utf8
'''主测试程序
'''
import os
import pickle
import json

import catdiv
import worddiv

def main():
	config = json.load(open('./config.json'))
	print('start')
	worddiv.init()

	# ret_dict = catdiv.walker('../Data', (catdiv.fetch), fetch_rate=config['fetch_rate'])
	# ret_dict = catdiv.walker(ret_dict['fetch_path'], (catdiv.diver), driver_train_rate=config['driver_train_rate'])
	# catdiv.walker(ret_dict['test_path'], (worddiv.genwordpkl), min_words_num=config['min_words_num'])
	# catdiv.walker(ret_dict['train_path'], (worddiv.genwordpkl), min_words_num=config['min_words_num'])

	# ret_dict = catdiv.walker('../Data', (catdiv.fetch), fetch_rate=config['fetch_rate'])
	# ret_dict = catdiv.walker('../Data_01', (catdiv.diver), driver_train_rate=config['driver_train_rate'])
	# catdiv.walker(ret_dict['test_path'], (worddiv.genwordpkl), min_words_num=config['min_words_num'])
	# catdiv.walker(ret_dict['train_path'], (worddiv.genwordpkl), min_words_num=config['min_words_num'])


	ret_dict = catdiv.walker('../Data', (catdiv.diver), driver_train_rate=config['driver_train_rate'])
	# catdiv.walker(ret_dict['test_path'], (worddiv.genwordpkl), min_words_num=config['min_words_num'])
	# catdiv.walker(ret_dict['train_path'], (worddiv.genwordpkl), min_words_num=config['min_words_num'])

if __name__ == '__main__':
	main()
