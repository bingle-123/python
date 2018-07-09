# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# condition对象可以用来同步一个工作流的各个部分,使其中一部分并发的运行,而另外一些顺序运行,即使他们在单独的进程中

import multiprocessing, time


def stage1(cond):
    name = multiprocessing.current_process().name
    print('Starting: ', name)
    with cond:
        print('%s done and ready for stage 2' % name)
        cond.notify_all()


def stage2(cond):
    name = multiprocessing.current_process().name
    print('Starting: ', name)
    with cond:
        cond.wait()
        print('%s running' % name)


condition = multiprocessing.Condition()
s1 = multiprocessing.Process(name='s1', target=stage1, args=(condition,))
s2_clients = [multiprocessing.Process(name='stage2[%d]' % i, target=stage2, args=(condition,)) for i in range(1, 3)]
for c in s2_clients:
    c.start()
    time.sleep(1)
s1.start()
s1.join()
for c in s2_clients:
    c.join()