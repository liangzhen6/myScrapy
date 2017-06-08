#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from datetime import datetime, timedelta
from pymongo import MongoClient, errors
from myScrapy.items import MyscrapyItem

class MongoQueue():

	def __init__(self, db, collection, timeout = 300):
		self.client = MongoClient()
		self.Client = self.client[db]
		self.db = self.Client[collection]
		self.timeout = timeout

	def insert_itmes(self,items):
		if items == None:
			print('没有内容数据')
			return
		try:
			name = items['name']
			author = items['author']
			novelurl = items['novelurl']
			category = items['category']
			name_id = items['name_id']
			self.db.insert({'name':name, 
							'author':author, 
							'_id':novelurl, 
							'category':category, 
							'name_id':name_id})
			print('写入数据成功')
		except:
			print('写入数据出错')

	def findall_itmesdb(self):
		allmongodb = self.db.find()
		a = 0
		for db in allmongodb:
			a+=1
			print(db,a)


	def insert_ips(self,dic):
		if dic == None:
			print('没有ip数据')
			return
		try:
			self.db.insert({'ip':dic['ip'], 'port':dic['port'], 'timestamp':datetime.now()})
			print('插入IP地址成功')
		except:
			port('插入IP地址出错')


	def find_ip(self):
		try:
			record = self.db.find_and_modify(
			query = {
				'timestamp':{'$lt':datetime.now() - timedelta(seconds = 1)}
			},
			update = {'$set':{'timestamp':datetime.now()}}
			)
			if record:
				return record
			else:
				print('没发现可用的ip')
				return None
		except:
			print('没发现可用的ip')
			return None
	def clear(self):
		'''这个函数只有第一次才会调用、后面不要调用，是删除数据库中的  集合'''
		self.db.drop()

# mon = MongoQueue('xiaoshuo', 'novel')
# mon.findalldb()

