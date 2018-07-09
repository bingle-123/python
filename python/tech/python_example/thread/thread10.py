# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 处于某种原因,需要派生Thread,Timer就是这样一个列子,
# Timer也包含在threading中,Timer在一个延迟之后开始工作,
# 可以在这个延迟时间内的任意时刻取消.

import threading, time


def delayed():
    logging.debug('worker running')
    return


t1 = threading.Timer(3, delayed)
t1.setName('t1')

t2 = threading.Timer(3, delayed)
t2.setName('t2')

logging.debug('starting timers')

t1.start()
t2.start()

logging.debug('waiting before canceling %s', t2.getName())
time.sleep(2)

logging.debug('canceling %s', t2.getName())
t2.cancel()
logging.debug('done')