# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s (%(threadName)-10s) %(message)s', )
# event 类提供了一种简单的方法,可以在进程之间传递状态信息,事件可以切换设置和未设置状态.
# 通过使用一个可选的超时值,时间对象的用户可以等待其状态从未设置变为设置

import multiprocessing
import time


def wait_for_event(e):
    print('wait_for_event:starting')
    e.wait()
    print('wait_for_event:e.is_set()_>', e.is_set())


def wait_for_timeout(e, t):
    print('wait_for_timeout: starting')
    e.wait(t)
    print('wait_for_timeout: e.is_set()_>', e.is_set())


e = multiprocessing.Event()

w1 = multiprocessing.Process(name='block', target=wait_for_event, args=(e,))
w1.start()
w2 = multiprocessing.Process(
    name='nonblock', target=wait_for_timeout, args=(e, 2))
w2.start()

print('main : waiting before calling event.set()')
time.sleep(3)
e.set()
print('main:event is set')

# wait()到时间就会返回,而没有任何错误
