# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 与简单表单相比,腰对文件编码以便上传,需要多做一些工作,
# 要在请求体中构造一个完整的MIME消息,
# 使服务器能够区分哪些是收到的表单域,哪些是上传的文件
#
import urllib.request
eq=urllib.request.Request('http:localhost:8069/docmanager/login')
