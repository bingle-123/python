# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 要使用POST而不是GET将表单编码(form-encoded)数据发送到远程服务器,
# 需要将编码的查询参数作为数据传入urlopen()

import urllib.request
import urllib.parse

query = {'login': 'kkkk', 'password': 'kkkk'}
encoded_args = urllib.parse.urlencode(query)
url = 'http://localhost:8069/docmanager/login/'

response = urllib.request.urlopen(url, encoded_args.encode())

print(response.read().decode())

