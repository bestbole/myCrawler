# -*- coding: utf-8 -*-
import scrapy

class LianjiaItem(scrapy.Item):
    isentire=scrapy.Field()
    ljid=scrapy.Field()
    title = scrapy.Field()
    community = scrapy.Field()
    model = scrapy.Field()
    area = scrapy.Field()
    watch_num = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    loc = scrapy.Field()
    isdeco=scrapy.Field()
    
