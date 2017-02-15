# -*- coding: utf-8 -*-

BOT_NAME = 'CrawlerV1'

SPIDER_MODULES = ['CrawlerV1.spiders']
NEWSPIDER_MODULE = 'CrawlerV1.spiders'

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 0
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
DEFAULT_REQUEST_HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
}
EXTENSIONS = {
	'scrapy.extensions.telnet.TelnetConsole': None,
}
ITEM_PIPELINES = {
	'CrawlerV1.pipelines.CrawlerV1Pipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
	'CrawlerV1.myProxyMiddleware.ProxyMiddleware': 543,
}
TELNETCONSOLE_ENABLED = False

#COOKIES_DEBUG=True

#DUPEFILTER_DEBUG = True

LOG_LEVEL = "INFO"

REDIRECT_ENABLED=False

RETRY_ENABLED=False


MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = "lianjia"
MONGODB_DOCNAME = "ljDOC"

