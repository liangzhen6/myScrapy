#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import scrapy #导入scrapy包
import random
from bs4 import BeautifulSoup
from scrapy.http import Request ##一个单独的request的模块，需要跟进URL的时候，需要用它
from myScrapy.items import MyscrapyItem
from myScrapy.spiders.proxy import Download
from myScrapy.spiders.mongodb import MongoQueue


class Myspider(scrapy.Spider):
	"""docstring for Myspider"""
	name = 'myscrapy'
	allowed_domains = ['23us.com']
	bash_url = 'http://www.23us.com/class/'
	bashurl = '.html'
	proxy = Download()
	mongo_queue = MongoQueue('xiaoshuo', 'novel')
	mongo_ips = MongoQueue('xiaoshuo', 'ips')
	user_agent_list = [
			"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
 			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
 			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
 			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
 			"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
 			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
 			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
 			"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
 			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
 			"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
		]

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
			ipdic = self.mongo_ips.find_ip()
			if ipdic:
				IP = ''.join(str(ipdic['ip']).strip())
				PORT = ''.join(str(ipdic['port']).strip())
				IPPORT = 'http://%s:%s' %(IP,PORT)
				Agent = random.choice(self.user_agent_list)
				yield Request(url, callback = self.get_name, meta = {'proxy':IPPORT, 'User-Agent':Agent})#meta 加代理即可防止ban
			else:
				print('放水了，哈哈哈')
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
		self.mongo_queue.insert_itmes(item)


















# Myspider().start_requests()