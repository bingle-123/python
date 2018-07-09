# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# json模块提供了一个与pickle类似的API,
# 可以将内存中的python对象转换为一个串行化表示,
# 称为javascript对象记法

import json

data = [{'a': 'A', 'b': (2, 4), 'c': 3.0}]
data_string = json.dumps(data)
print(type(data_string))

# 编码后再重新解码时,可能会得到完全不同的对象类型

decoded=json.loads(data_string)
print(type(decoded))

