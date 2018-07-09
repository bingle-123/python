# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 与使用列表的代码相比,基于迭代器的算法可以提供更好的内存使用特性
# 在真正需要数据之前,并不从迭代器生成数据,由于这个原因,
# 不需要将所有数据都同时存储在内存中.
# 这种懒处理模型可以减少内存使用,相应的还可以减少交换以及大叔句集的其他副作用,从而改善性能

import itertools

# chain()函数取多个迭代器作为参数,最后返回一个迭代器,他能生成所有输入迭代器的内容,
# 就好像这些内容来自一个迭代器一样

for i in itertools.chain([1, 2, 3], ['a', 'b', 'c']):
# for i in itertools.chain('asdfghjklzxcvbnm'):
    print(i)
print()
# zip_longest返回一个迭代器,他会把多个迭代器的元素结合到一个元祖中
# 他的工作方式类似于zip()函数,只不过他会返回迭代器而不是一个列表

for i in itertools.zip_longest([1, 2, 3], ['a', 'b', 'c'], ['d', 'e', 'f']):
    print(i)
for i in itertools.zip_longest([1, 2, 3], ['a', 'b', 'c']):
    print(i)
for i in itertools.zip_longest([1, 2, 3]):
    print(i)
print()

# islice()函数返回一个迭代器,它按索引返回由输入迭代器所选的元素
# islice()与列表的slice操作符参数相同,同样包括开始,结束和步长,start和step参数是可选的

# 从0,5
for i in itertools.islice(itertools.count(), 5):
    print(i)
# 从5,10
for i in itertools.islice(itertools.count(), 5, 10):
    print(i)
# 从5,100,每个间隔10
for i in itertools.islice(itertools.count(), 5, 100, 10):
    print(i)
print()

# tee()函数根据一个原始输入迭代器返回多个独立的得带起(默认为两个)
# i1和i2内容相同
# tee()返回的迭代器可以用来为将来并行处理的多个算法提供相同的数据集
r = itertools.islice(itertools.count(0), 5)
i1, i2 = itertools.tee(r)
print('i1:', i1)
for i in i1:
    print(i)

print('i2:', i2)
for i in i2:
    print(i)

print()

