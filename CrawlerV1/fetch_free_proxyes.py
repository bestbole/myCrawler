# -*- coding: utf-8 -*-
import urllib2
import logging
from lxml import etree
import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

logger = logging.getLogger(__name__)

def new_fetch_kxdaili(pages=2):
    proxyes = []
    for pg in range(pages):
        pg=pg+1
        url = "http://www.kxdaili.com/dailiip/1/%d.html" % pg
        headers = {'user-agent': USER_AGENT}
        response = requests.get(url,headers=headers)
        contents=etree.HTML(response.text)
        tab=contents.xpath('//*[@class="ui table segment"]/tbody/tr')
        for tr in tab:
            try:
                address=tr.xpath('td[1]/text()')[0]
                port=int(tr.xpath('td[2]/text()')[0])
                proxyes.append("%s:%s" % (address, port))
            except:
                pass
    return proxyes
def new_fetch_xici():
    proxyes = []
    url = "http://www.xicidaili.com/nn/"
    headers = {'user-agent': USER_AGENT}
    response = requests.get(url,headers=headers)
    contents=etree.HTML(response.text)
    ip1=contents.xpath('//tr[@class="odd"]')
    ip2=contents.xpath('//tr[@class=""]')
    iplist=ip1+ip2
    for ip in iplist:
        try:
            iscn = ip.xpath('td[1]/img')!=[]
            address = ip.xpath('td[2]/text()')[0]
            port = ip.xpath('td[3]/text()')[0]
            speed=ip.xpath('td[7]/div/@title')[0]
            try:
                speed=float(speed.strip(speed[-1]))
            except:
                speed=10.0
            if speed<2.5:
                proxyes.append("%s:%s" % (address, port))
        except:
            pass
    return proxyes
def new_fetch_httpdaili():
    proxyes = []
    url = "http://www.httpdaili.com/mfdl/"
    headers = {'user-agent': USER_AGENT}
    response = requests.get(url,headers=headers)
    contents=etree.HTML(response.text)
    li=contents.xpath('//*[@style="position: absolute; left: 10.5px; top: 0px;"]')[0]
    tab=contents.xpath('//table[1]/tr')
    for tr in tab:
        try:
            info=tr.xpath('*/text()')
            address=info[0]
            port=int(info[1])
            proxyes.append("%s:%s" % (address, port))
        except:
            pass
    return proxyes
def new_fetch_66ip():
    proxyes = []
    url = "http://www.66ip.cn/areaindex_1/1.html"
    headers = {'user-agent': USER_AGENT}
    response = requests.get(url,headers=headers)
    contents=etree.HTML(response.text)
    tab=contents.xpath('//*[@width="100%"]/tr')
    for tr in tab:
        try:
            address=tr.xpath('td[1]/text()')[0]
            port=int(tr.xpath('td[2]/text()')[0])
            proxyes.append("%s:%s" % (address, port))
        except:
           pass
    return proxyes
    
def check(proxy):
    import urllib2
    url = "http://www.baidu.com/js/bdsug.js?v=1.0.3.0"
    proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
    try:
        response = opener.open(url,timeout=3)
        return response.code == 200 and response.url == url
    except Exception:
        return False

def new_get_all(endpage=2):
    proxyes = []
    proxyes += new_fetch_xici()
    proxyes += new_fetch_httpdaili()
    proxyes += new_fetch_66ip()
    print("I have fetched %i proxyes!"%(len(proxyes)))
    return proxyes

def get_all_test(endpage=2):
    from datetime import datetime
    print datetime.now()
    proxyes = []

    proxyes += new_fetch_xici()
    print datetime.now()

    proxyes += new_fetch_httpdaili()
    print datetime.now()

    proxyes += new_fetch_66ip()
    print datetime.now()

    proxyes += new_fetch_kxdaili(endpage)
    print datetime.now()

    print("I have fetched %i proxyes!"%(len(proxyes)))
    return proxyes

def remove(a,b):
    tar=a[0]
    b.append(tar)
    a.remove(tar)
    return tar

    
if __name__ == '__main__':
    #print check("111.76.133.218:808")
    d=get_all_test(5)



'''
def get_html(url):
    request = urllib2.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36")
    html = urllib2.urlopen(request)
    return html.read()

def get_soup(url):
    soup = BeautifulSoup(get_html(url), "lxml")
    return soup

def fetch(npts):
    new_proxyes=[]
    proxyes=read_all()
    if proxyes==[]:
        proxyes=get_all()
    for p in proxyes:
        proxyes.remove(p)
        if check(p):
            print ("%s response successfully."%p)
            new_proxyes.append(p)
            if len(new_proxyes)>npts:
                break
    write_all(proxyes)
    return new_proxyes


http://www.66ip.cn/
http://www.httpdaili.com/mfdl/
http://www.kxdaili.com/
http://proxy.mimvp.com/free.php
http://www.ip181.com/
http://www.xicidaili.com/nn/
'''