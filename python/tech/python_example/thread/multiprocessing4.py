# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging
import random
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 传递参数来标识或命名进程很麻烦,也没有什么必要,每个process实例都有一个名称
# 其默认值可以在创建进程时改变,给进程命名对于跟踪进程很有用,特别是当应用中有多种类型
# 进程z在同时运行时

import multiprocessing, time


def worker():
    name = multiprocessing.current_process().name
    print(name, 'starting')
    time.sleep(2)
    print(name, 'Exiting')


def mysevice():
    name = multiprocessing.current_process().name
    print(name, 'Starting')
    time.sleep(random.randint(1,5))
    print(name, 'Exiting')


service = multiprocessing.Process(name='myservice', target=mysevice)
worker1 = multiprocessing.Process(name='worker 1', target=worker)
worker2 = multiprocessing.Process(target=worker)

service.start()
worker1.start()
worker2.start()
