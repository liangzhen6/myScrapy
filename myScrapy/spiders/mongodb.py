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

	def insert(self,items):
		try:
			name = items['name']
			author = items['author']
			novelurl = items['novelurl']
			category = items['category']
			name_id = items['name_id']
			self.db.insert({'name':name, 
							'author':author, 
							'novelurl':novelurl, 
							'category':category, 
							'name_id':name_id})
			print('写入数据成功')
		except:
			print('写入数据出错')

	def findalldb(self):
		allmongodb = self.db.find()
		a = 0
		for db in allmongodb:
			a+=1
			print(db,a)

# mon = MongoQueue('xiaoshuo', 'novel')
# mon.findalldb()

