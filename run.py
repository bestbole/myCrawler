# -*- coding: utf-8 -*-
import os
import subprocess 
import pymongo
import time
from CrawlerV1 import settings
from CrawlerV1.items import LianjiaItem

PrintLOG=True

server=subprocess.Popen(
	['mongod','--dbpath','D:\database'],
	shell=False,
	creationflags=subprocess.CREATE_NEW_CONSOLE
	)


print(u'数据库启动成功，准备初始化，按任意键继续...')
raw_input()

host = settings.MONGODB_HOST
port = settings.MONGODB_PORT
db_name = settings.MONGODB_DBNAME
col_name= settings.MONGODB_DOCNAME
client = pymongo.MongoClient(host=host,port=port)
db=client[db_name]
db.drop_collection(col_name)

print(u'初始化成功，开始提取数据...\n')

if PrintLOG:
	p=subprocess.Popen('runLog.cmd',shell=False)
else:
	p=subprocess.Popen('run.cmd',shell=False)
p.wait()
p.kill()

print(u'数据提取完成，导出CSV...\n')

fieldlist=LianjiaItem.fields.keys()
fieldlist=','.join(fieldlist)

command=['mongoexport','-d',db_name,'-c',col_name,'-f',fieldlist,'/type','csv','-o','"bjlj.csv"']
export=subprocess.Popen(command,shell=False)
export.wait()

print(u'文件导出完成~~\n')

export.kill()
server.kill()

raw_input()