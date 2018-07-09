# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# urlopen是一个便利函数,可以隐藏建立和处理请求的一些细节,
# 通过直接使用Request实例可以提供更精确的控制
# 例如:定制首部,控制返回数据的格式,指定本地缓存的版本,
# 还可以告诉远程服务器与之通信的软件客户名

import urllib.request

request = urllib.request.Request('http://localhost:8069/docmanager/login')
request.add_header('User-agent', 'hello-world')
response = urllib.request.urlopen(request)
data = response.read()
print(response.info().items())
print(data.decode())



# 从请求提交表单数据
query = {'login': 'kkkk', 'password': 'kkkk'}
encoded_args = urllib.parse.urlencode(query)
request = urllib.request.Request('http://localhost:8069/docmanager/login')
request.data = encoded_args.encode()
request.headers = {'charset':'utf-8'}
response = urllib.request.urlopen(request)
print(response.read().decode())