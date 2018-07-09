# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# functools模块提供的主要工具是partial类,它可以用来包装一个默认参数的可回掉对象,
#
import functools


def myfunc(a, b=2):
    print('called myfunc with', (a, b))
    return


def showdetials(name, f, is_partial=False):
    print(name)
    # print(f)
    if not is_partial:
        print(f.__name__)
    if is_partial:
        print(f.func)
        print(f.args)
        print(f.keywords)


showdetials('myfunc', myfunc)
myfunc('a', 3)
print()

p1 = functools.partial(myfunc, b=4)
print(dir(p1))
showdetials('partial with named default', p1, True)
p1('passing a')
p1('override b', b=5)
print()

p2 = functools.partial(myfunc, 'default a', b=99)
showdetials('partial with defaluts', p2, True)
p2()
p2(b='override b')

print()

