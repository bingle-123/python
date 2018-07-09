# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

import mmap
# mmap可以提高I/O性能,
# 内存映射文文件可以看作是可修改的字符串或类文件对象,这取决于具体的需要
