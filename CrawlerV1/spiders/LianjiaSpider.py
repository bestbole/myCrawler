# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import time
from lxml import etree
from .. items import LianjiaItem
from .. mySettings import *
from scrapy.conf import settings

class LianjiaSpider(scrapy.Spider):
	name = 'LianjiaSpider'
	start_urls = 'http://bj.lianjia.com/zufang/'
	area_list=['dongcheng']
	def start_requests(self):
		for area_pin in self.area_list:
			url=self.start_urls+'{}/'.format(area_pin)
			start_req=scrapy.Request(
				url=url,
				method='GET',
				callback=self.area_parse,
				cookies=lj_cookies,
				meta={"proxy":None}
				)
			yield start_req
	def area_parse(self,response):
		for page in range(1,70):
			page_url=response.url+'pg{}/'.format(page)
			page_req=scrapy.Request(
				url=page_url,
				method='GET',
				callback=self.house_parse,
				cookies=lj_cookies,
				meta={"proxy":None}
				)
			yield page_req

	def house_parse(self,response):
		houselist = response.xpath('/html/body/div[4]/div[2]/div[1]/div[2]/ul[1]/li')
		for house in houselist:
			try:
				house_url=house.xpath('div[2]/h2/a/@href').extract()[0]
				house_req=scrapy.Request(
					url=house_url,
					method='GET',
					callback=self.parse,
					cookies=lj_cookies,
					meta={"proxy":None}
					)
				yield house_req

			except Exception as e:
				print e
				pass
			

	def parse(self,response):
		house=response
		html=response.text

		area_re="area:(.+)"
		price_re="totalPrice:(.+)"
		community_re="resblockName:(.+)"
		lat_re="resblockPosition:(.+)"
		int_re="(\w*[0-9]+)\w*"
		float_re="\d+\.?\d*"

		item = LianjiaItem()
		house_url=response.url
		item['ljid']=house_url.split('/')[-1].split('.')[0]
		item['link']=house_url
		item['title']=house.xpath('/html/body/div[4]/div[1]/div/div[1]/h1/text()').extract()[0]
		temp=re.findall(community_re,html)[-1]
		item['community']=temp.strip('\'').strip(',').strip('\'')
		temp=re.findall(area_re,html)[-1]
		temp2=re.findall(float_re,temp)[0]
		item['area']=float(temp2)
		temp=re.findall(price_re,html)[-1]
		temp2=re.findall(int_re,temp)[0]
		item['price']=float(temp2)
		temp=re.findall(lat_re,html)[-1]
		temp2=re.findall(float_re,temp)
		temp3=[float(t) for t in temp2]
		item['loc']=temp3
		dec=house.xpath('//*[@class="zf-room"]/p[2]/text()').extract()[0].split(' ')
		item['model']=dec[0]
		if (len(dec)==1):
			item['isentire']=True
		elif (u'\u6574\u79df' in dec):
			item['isentire']=True
		else:
			item['isentire']=False
		exdeco=house.xpath('//*[@class="tips decoration"]')
		item['isdeco']=(exdeco!=[])
		try:
			watch=house.xpath('//*[@class="time"]/text()').extract()[0]
			watch_num=re.findall(int_re,watch)[0]
			item['watch_num']=int(watch_num)
		except Exception :
			item['watch_num']=int(0)

		print("=========================================")
		print item['title']
		print("=========================================")
		yield item