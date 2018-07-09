# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# base64包含一些函数,可以将二进制数据转换为适合使用纯文本协议传输的ascii子集
#
import base64

xx = bytes('你好中国'.encode())
print(xx)
ss = base64.b64encode('你好中国'.encode('GBK'))
print(ss)

sde = base64.b64decode(ss)
print(sde.decode('GBK'))


