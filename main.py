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
	catdiv.walker('../Data', (catdiv.fetch), fetch_rate=config['fetch_rate'])

if __name__ == '__main__':
	main()
