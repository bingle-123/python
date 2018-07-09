# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 要在一个单独的进程中开始工作,尽管最简单的方法是使用process并传入一个目标函数
# 不过也可以使用一个定制类

import multiprocessing


class Worker(multiprocessing.Process):
    def run(self):
        print('In %s' % self.name)
        return


jobs = []
for i in range(5):
    p = Worker()
    jobs.append(p)
    p.start()