# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

import threading

# 由于传递到Thread构造函数的args和kwargs值保存在私有变量中(这些变量名前面都有__)
# 所以不能很容易的从子类中访问这些值,要向一个定制的线程类传递参数,需要重新定义构造函数,
# 将这些值保存在子类可见的一个实例属性中

class mythread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        return

    def run(self):
        logging.debug('running with %s and %s', self.args, self.kwargs)
        return


for i in range(5):
    t = mythread(args=(i,), kwargs={'a': i, 'b': i + 1})
    t.start()