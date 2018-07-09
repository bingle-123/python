# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# count()函数返回一个迭代器,能够无限的生成连续整数,第一个可以作为参数传入(默认为0)
# 这里没有上界参数
import itertools

for i in zip(itertools.count(1), ['a', 'b', 'c']):
    print(i)

print()
# cycle()函数返回一个迭代器,他会无限的重复非定参数的内容,由于必须记住输入迭代器的全部内容
# 因此如果这个迭代器很长,可能会消耗大量的内存

for i in zip(range(5), itertools.cycle(['a', 'b', 'c'])):
    print(i)

# repeat()函数返回一个迭代器,每次访问时都会生成相同的值
# repeat()会一直返回数据,除非提供了可选的times参数来限制次数
for i in itertools.repeat('hello', 5):
    print(i)
print()

# 将repeat()与zip结合起来

for i, s in zip(itertools.count(), itertools.repeat('hello', 5)):
    print(i, s)
