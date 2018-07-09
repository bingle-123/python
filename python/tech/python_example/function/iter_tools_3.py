# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )


# dropwhile()函数返回一个迭代器,
# 他会生成输入迭代器中条件第一次为false之后的元素

import itertools


def should_drop(x):
    return (x < 2)


for i in itertools.dropwhile(should_drop, range(6)):
    print(i)

print()
# takewhile()正好与dropwhile()相反,他也会返回一个迭代器,
# 这个迭代器将输入迭代器中保证测试条件为true的元素.
# 一旦should_keep()返回false,takewhile()就会停止处理输入.


def should_keep(x):
    return (x < 4)


for i in itertools.takewhile(should_keep, range(6)):
    print(i)

print()


def check_item(x):
    return (x < 3)


for i in itertools.filterfalse(check_item, range(8)):
    print(i)
    
