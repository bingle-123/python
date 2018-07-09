# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 向进程传递消息,利用multiprocessing完成进程间通信的一种简单方法是使用一个Queue来回传递消息,
# 能够用pickle串行化的任何对象都可以通过Queue传递

import multiprocessing
import time
import random
from threading import Thread

class Myfancyclass(object):
    def __init__(self, name):
        self.name = name

    def do_something(self):
        time.sleep(random.randint(2,5))
        proc_name = multiprocessing.current_process().name
        print('Doing someting fancy in %s for %s!' % (proc_name, self.name))


def worker(q):
    obj = q.get()
    time.sleep(random.randint(1,3))
    print(i)


queue = multiprocessing.Queue()

for i in range(3):
    p = multiprocessing.Process(target=worker, args=(queue,))
    p.start()
    queue.put(i)
queue.close()
queue.join_thread()
p.join()
