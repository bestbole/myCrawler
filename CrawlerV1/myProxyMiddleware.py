# -*- coding: utf-8 -*-
import os
import time
import logging
import threading
from scrapy import signals
from twisted.web._newclient import ResponseNeverReceived
from twisted.internet.error import TimeoutError, ConnectionRefusedError, ConnectError
from fetch_free_proxyes import *
logger = logging.getLogger(__name__)

class Checker2(threading.Thread):
    def __init__(self, event, name):
        super(Checker2, self).__init__()
        self.event = event
        self.name = name

    def run(self):
        while True:
            self.event.wait()
            if catch0==[]:
                logger.info("Nothing to check,I will stop.")
                self.kill()
            else:
                if len(catch1) < catch1_len:
                    p=catch0[0]
                    if check(p):
                        print("[%i/%i/%i]::%s is OK"%(len(catch2),len(catch1),len(catch0),p))
                        remove(catch0,catch1)
                        sgnPusher.set()
                    else:
                        print("[%i/%i/%i]::%s is BAD"%(len(catch2),len(catch1),len(catch0),p))
                        catch0.remove(p)
                else:
                    self.event.clear()

class Pusher2(threading.Thread):
    def __init__(self, event, name):
        super(Pusher2, self).__init__()
        self.event = event
        self.name = name

    def run(self):
        while True:
            self.event.wait()
            if len(catch2)<catch2_len and len(catch1)!=0:
                p=remove(catch1,catch2)
                print("%s is pushed"%p)
                sgnChecker.set()
            else:
                self.event.clear()

catch0=new_get_all()
catch1     =[]
catch2     =[]
catch1_len = 5
catch2_len = 2
sgnChecker = threading.Event()
sgnPusher = threading.Event()
kitty=Checker2(sgnChecker,'kitty')
bill=Pusher2(sgnPusher,'bill')
kitty.start()
bill.start()
sgnChecker.set()
sgnPusher.set()

class ProxyMiddleware(object):
    # 遇到这些类型的错误直接当做代理不可用处理掉, 不再传给retrymiddleware
    DONT_RETRY_ERRORS = (TimeoutError, ConnectionRefusedError, ResponseNeverReceived, ConnectError, ValueError)

    def __init__(self):
        self.proxy = None

    @classmethod
    def from_crawler(cls, crawler):
        pm=cls()
        crawler.signals.connect(pm.spider_closed, signal=signals.spider_closed)
        return pm

    def process_response(self, request, response, spider):

        logger.info("I receive response from %s by %s status is %s" % (request.url,request.meta["proxy"],response.status))

        if response.status==302:

            if request.meta['proxy']==self.proxy:
                self.next_index()            

            new_request = request.copy()
            new_request.dont_filter = True
            new_request.meta['proxy']=self.proxy
            return new_request

        return response


    def process_request(self, request, spider):

        request.meta['proxy']=self.proxy

        logger.info("I send request by %s to %s"%(request.meta['proxy'],request.url))

        return None

    def process_exception(self, request, exception, spider):
        
        logger.info('exception happend')
        try:
            logger.info(exception.message)
        except:
            logger.info('cant print error message')

        if request.meta['proxy']==self.proxy:
            self.next_index()

        new_request = request.copy()
        new_request.dont_filter = True
        
        return new_request

    def next_index(self):
        sleep_time=0
        while len(catch2)<catch2_len:
            time.sleep(1)
            sleep_time+=1
            if (sleep_time % 50) == 0:
                logger.info('One 50 sec')
        
        self.proxy="http://"+catch2[0]

        catch2.remove(catch2[0])

        print("%s is moved"%catch2[0])

    def spider_closed(self):
		kitty._Thread__stop()
		bill._Thread__stop()

		logger.info("Bill&Kitty IS LOVED")
'''
class Pusher(threading.Thread):
    def __init__(self, event, name):
        super(Pusher, self).__init__()
        self.event = event
        self.name = name

    def run(self):
        while True:
            self.event.wait()
            if len(catch2)<catch2_len and len(catch1)!=0:
                p=remove(catch1,catch2)
                print("%s is pushed"%p)
                sgnChecker.set()
            else:
                pass
class Checker(threading.Thread):
    def __init__(self, event, name):
        super(Checker, self).__init__()
        self.event = event
        self.name = name

    def run(self):
        while True:
            self.event.wait()
            if len(catch1)<catch1_len:
                p=catch0[0]
                if check(p):
                    print("%s is ok"%p)
                    remove(catch0,catch1)
                else:
                    print("%s is error"%p)
                    catch0.remove(p)
            else:
                pass
'''