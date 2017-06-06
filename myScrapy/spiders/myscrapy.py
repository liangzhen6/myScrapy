#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import scrapy #导入scrapy包
from bs4 import BeautifulSoup
from scrapy.http import Request ##一个单独的request的模块，需要跟进URL的时候，需要用它
from myScrapy.items import MyscrapyItem

class Myspider(scrapy.Spider):
	"""docstring for Myspider"""
	name = 'myscrapy'
	allowed_domains = ['23us.com']
	bash_url = 'http://www.23us.com/class/'
	bashurl = '.html'

	def start_requests(self):
		for i in range(1,11):
			url = self.bash_url + str(i) + '_1' + self.bashurl
			yield Request(url, self.parse)
		yield Request('http://www.23us.com/quanben/1', self.parse)

	def parse(self, response):
		max_num = BeautifulSoup(response.text, 'lxml').find('div', class_ = 'pagelink').find_all('a')[-1].get_text()
		bashurl = str(response.url)[:-7]
		for num in range(1, int(max_num) + 1):
			url = bashurl + '_' + str(num) + self.bashurl
			yield Request(url, callback = self.get_name)
		# print(response.text)

	def get_name(self, response):
		tds = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor = '#FFFFFF')
		for td in tds:
			novelname = td.find('a')['title']
			novelurl = td.find('a')['href']
			yield Request(novelurl, callback = self.get_chapterurl, meta = {'name':novelname, 'url':novelurl})



	def get_chapterurl(self, response):
		item = MyscrapyItem()
		item['name'] = str(response.meta['name'])[0:-2]
		item['novelurl'] = response.meta['url']
		item['name_id'] = str(response.meta['url']).split('/')[-1]
		trs = BeautifulSoup(response.text, 'lxml').find('table', id = 'at', bgcolor = '#E4E4E4').find_all('tr')
		tr = trs[0]
		category = tr.find('a').get_text()
		author = tr.find_all('td')[1].get_text()
		item['category'] = category.strip()
		item['author'] = author.strip()
		print(item)


















# Myspider().start_requests()