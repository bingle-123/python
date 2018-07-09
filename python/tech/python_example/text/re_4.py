# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 搜索选项
# 不区分大小写
import re

text = 'this is some text --with punctuation'
pattern = r'\bT\w+'
regex = re.compile(pattern, re.IGNORECASE)


# python中str对象使用的是ASCII字符集,而且正则表达式处理会假设模式和输入文本都是ASCII字符
# 需要在编译模式时调用
regex = re.compile(pattern, re.UNICODE)
