# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# threading与multiprocessing例子之间有一个区别,multiprocessing例子中,

import multiprocessing

jobs = []
for i in range(1, 10):
    fp = multiprocessing.Process(target=multiprocessing.worker, args=(i,))
    jobs.append(fp)
    fp.start()
