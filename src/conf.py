#!/usr/bin/env python3
# -*- coding:utf-8 -*-  
import os
import configparser

class Conf:
	def __init__(self,file='./test.ini'):
		self.file = file  
		self.cfg = configparser.ConfigParser()
		self.cfg_load()

	def cfg_load(self):  
		self.cfg.read(self.file) 
		
	def cfg_dump(self):  
		se_list = self.cfg.sections()
		print('==================>')
		for se in se_list:  
			print(se)
			print(self.cfg.items(se))  
		print('==================>')
		
	def cfg_options(self,se):
		opts = self.cfg.options(se)
		print('options:', opts, type(opts))
		
	def delete_item(self,se,key):
		self.cfg.remove_option(se,key) 

	def delete_section(self,se):  
		self.cfg.remove_section(se)

	def add_section(self,se):
		self.cfg.add_section(se)

	def set_item(self,se,key,value):
		self.cfg.set(se,key,value)

	def save(self):
		if os.path.isfile(self.file):
			os.remove(self.file)
			
		fd = open(self.file, 'a')  
		self.cfg.write(fd)
		fd.close()  
		
	def get_item(self, se):
		kvs = self.cfg.items(se)
		print('db:', kvs)
		
	def get_intval(self,se,key):
		return self.cfg.getint(se, key)
	
	def get_value(self,se,key):
		return self.cfg.get(se,key)
		
		
if __name__ =='__main__':
	info = Conf()  

	
	# info.add_section('ZJE')  
	# info.set_item('ZJE','name','zhujunwen')  
	# info.cfg_dump()  
	# info.save()
	
	print(info.get_value('db', 'db_port'))

