#!/usr/bin/env python3
## -*- coding: utf-8 -*-
import requests
import re
import random
import time
from bs4 import BeautifulSoup

class Download(object):
	"""docstring for Download"""
	def __init__(self):
		# super(Download, self).__init__()
		self.user_agent_list = [
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
		self.iplist = []
		headers = {'User-Agent':random.choice(self.user_agent_list)}
		try:
			html = requests.get('http://www.66ip.cn/areaindex_19/index.html',headers = headers)
			# iplistn = re.findall(r'r/>(.*?)<b',html.text,re.S)  ##表示从html.text中获取所有r/><b中的内容，re.S的意思是包括匹配包括换行符，findall返回的是个list哦！				
			html_soup = BeautifulSoup(html.text, 'lxml')
			div = html_soup.find('div',id = 'footer').find('div',align = 'center')
			table = div.find('table')
			array = table.find_all('tr')
			array.pop(0)
			for tr in array:
				arr_td = tr.find_all('td')
				dic = {'ip':arr_td[0].get_text(), 'port':arr_td[1].get_text()}
				self.iplist.append(dic)
			# print(self.iplist)
			# for ip in iplistn:
			# 	i = re.sub('\n','',ip)#re.sub 是re模块替换的方法，这儿表示将\n替换为空
			# 	print(i.strip())
			# 	self.iplist.append(i.strip())
		except :
			print('error')
			self.iplist = None

# req = Download()

# print(req.iplist, req.user_agent_list)


