# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 腰向一个multiprocessing Process传递一个参数,这个参数必须能够使用pickle串行化,
import  time,random
import multiprocessing


def worker(num):
    time.sleep(random.choice(range(4)))
    print('worker', num)
    return


jobs = []
for i in range(1, 10):
    fp = multiprocessing.Process(target=worker, args=(i,))
    jobs.append(fp)
    fp.start()
