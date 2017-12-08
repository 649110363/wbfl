# coding = utf8
'''处理划分、重命名文件夹和文件
'''
import os
import shutil

# walker回调模板
def call_back(target_path, rel_path, file_names, dir_names, **kwargs):
	'''target_path 末尾无/, rel_path前后有/, file_names前后无/,  dir_names前后无/
		target_path 如 ./Data
		kwargs字典为不同函数提供其单独的参数
	'''
	for mfile in file_names:
		pass
	for mdir in dir_names:
		pass
	return {'call':'call once'}

# 有序化名称的对齐位数
RENAME_ALIGN = 6
def ordername(target_path, rel_path, file_names, dir_names, **kwargs):
	'''有序化重命名文件,有序化后的文件名为 上一层文件夹名_XXXXX ,其中XX长度由RENAME_ALIGN决定
		kwargs中需要有 rename_align 参数指定有序化名称的对齐位数否则默认RENAME_ALIGN
	'''
	mpath = target_path + rel_path
	# 计数开始数值
	file_cnt = 0
	rename_align = kwargs.get('rename_align')
	if rename_align is None:
		rename_align = RENAME_ALIGN
	tfilename = rel_path.split('/')[-2] + '_%%0%dd.txt'%rename_align
	for mfile in file_names:
		os.rename(mpath+mfile, mpath + tfilename%file_cnt)
		file_cnt += 1

# 训练比例
DIVER_TARIN_RATE = 0.5
def diver(target_path, rel_path, file_names, dir_names, **kwargs):
	'''根据DIVER_TARIN_RATE划分训练集和测试集
		kwargs中需要有 driver_train_rate 参数指定训练比例否则默认DIVER_TARIN_RATE
		返回一个字典, test_path和train_path分别为测试和训练的文件夹路径末尾
	'''
	origin_path = target_path + rel_path
	train_mpath = target_path + '_train'
	test_mpath = target_path + '_test'
	train_path = train_mpath + rel_path
	test_path = test_mpath + rel_path
	driver_train_rate = kwargs.get('driver_train_rate')
	if driver_train_rate is None:
		driver_train_rate = DIVER_TARIN_RATE
	test_cnt = int(len(file_names)*driver_train_rate) # 向下取整
	if not os.path.isdir(train_path):
		os.mkdir(train_path)
		os.mkdir(test_path)

	for mdir in dir_names:
		os.mkdir(train_path + mdir)
		os.mkdir(test_path + mdir)
	for mfile in file_names:
		if test_cnt > 0:
			shutil.copy(origin_path + mfile, test_path + mfile)
		else:
			shutil.copy(origin_path + mfile, train_path + mfile)
		test_cnt -= 1
	return {'test_path':test_mpath, 'train_path':train_mpath}


# 子集比例
FETCH_RATE = 0.2
def fetch(target_path, rel_path, file_names, dir_names, **kwargs):
	'''取子集,子集名为 原名称 + _ +FETCH_RATE去小数点
		kwargs中需要有 fetch_rate 参数指定训练比例否则默认FETCH_RATE
		返回一个字典, fetch_path为生成的子集文件夹路径末尾无 /	
	'''
	origin_path = target_path + rel_path
	fetch_rate = kwargs.get('fetch_rate')
	if fetch_rate is None:
		fetch_rate = FETCH_RATE
	fetch_mpath = target_path + '_' + str(fetch_rate).replace('.', '')
	fetch_path = fetch_mpath + rel_path
	test_cnt = int(len(file_names)*fetch_rate) # 向下取整
	if not os.path.isdir(fetch_path):
		os.mkdir(fetch_path)

	for mdir in dir_names:
		os.mkdir(fetch_path + mdir)
	for mfile in file_names:
		if test_cnt > 0:
			shutil.copy(origin_path + mfile, fetch_path + mfile)
		else:
			# 去掉末尾 /
			return {'fetch_path':fetch_mpath}
		test_cnt -= 1

def walker(target_path, *callbacks, **kwargs):
	'''target_path目标文件夹末尾不带 / ,可以嵌套分类
		*callbacks 回调函数的tuple集合
	'''
	ret_dict = {}
	target_path = target_path.replace('\\', '/')
	dir_walk = os.walk(target_path)
	for root, dirs, files in dir_walk:
		rel_path = root.replace('\\', '/').replace(target_path, '') + '/'
		print(rel_path)
		for func in callbacks:
			tmp_dict = func(target_path, rel_path, files, dirs, **kwargs)
			# 返回值不为空更新返回字典
			if tmp_dict:
				ret_dict.update(tmp_dict)
	return ret_dict

if __name__ == '__main__':
	funcs = (ordername,)
	walker('../tmp', (ordername), rename_align=6)
	# walker('./Data', (fetch), fetch_rate=0.1)
	# walker('./Data', (diver), driver_train_rate=0.5)
	# walker('../Data_01/sc', (checkcode))


