# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# multiprocessing模块包含一个API,它基于threading API可以在多个进程间划分工作,
# 有些情况下,multiprocessing可以作为临时替换,取代threading来利用多个cpu内核
# 避免python全局解释器锁带来的计算瓶颈

# 要创建第二个进程,最简单的方法就是用一个目标函数实例化一个proess对象,并调用start()让他开始工作

import multiprocessing


def worker():
    print('worker')
    return


jobs = []

for i in range(5):
    p = multiprocessing.Process(target=worker)
    jobs.append(p)
    p.start()

# 不过不能清楚知道哪一个进程先输出,这取决于具体的执行顺序,因为每个进程都在竞争访问输出流
