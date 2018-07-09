# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

import urllib.request


# urlopen是典型的get方法

response = urllib.request.urlopen('http:localhost:8080')
# response包含很多属性和方法用于度与响应内容,响应头



