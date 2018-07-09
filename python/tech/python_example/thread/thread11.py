# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 有时需要在两个或多个线程中同步操作,事件对象是实现线程间安全通信的一个简单方法
# Event管理一个内部标志,调用这可以用set()和clear()方法控制这个标志,其他线程可以使用wait()暂停,
# 直到设置这个标志,其他效果就是在允许继续之前阻塞线程的运行
import threading, time


def waitforevent(e):
    logging.debug('wait for event starting')
    time.sleep(5)
    e.set()
    eventisset = e.wait()
    logging.debug('event set:%s', eventisset)


def waitfortimeout(e, t):
    while not e.isSet():
        logging.debug('wait fot event timeout starting')
        eventiset = e.wait(t)  # 等待时间结束后继续运行
        logging.debug('event set:%s', eventiset)
        if eventiset:
            logging.debug('processing event')
        else:
            logging.debug('doing other work')


e = threading.Event()
t1 = threading.Thread(name='block', target=waitforevent, args=(e,))
t1.start()
t2 = threading.Thread(name='nonblock', target=waitfortimeout, args=(e, 1))
t2.start()
logging.debug('waiting before calling event.set()')
# time.sleep(5)
# e.set()
logging.debug('event is set')
