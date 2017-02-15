# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings
from .items import LianjiaItem


class CrawlerV1Pipeline(object):
	def __init__(self):
		host = settings['MONGODB_HOST']
		port = settings['MONGODB_PORT']
		db_name = settings['MONGODB_DBNAME']
		client = pymongo.MongoClient(host=host,port=port)
		tdb = client[db_name]
		self.post = tdb[settings['MONGODB_DOCNAME']]

	def process_item(self, item, spider):
		if isinstance(item,LianjiaItem):
			info = dict(item)
			self.post.insert(info)
		return item