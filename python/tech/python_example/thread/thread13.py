# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 除了使用Event,还可以通过使用一个Condition对象来同步线程.
# 由于condition使用了一个lock,它可以绑定到一个共享资源,允许多个线程等待资源更新,
# 在这个列自重consumer()线程腰等待设置了Condition才能继续,
# producer()线程复杂设置条件,并通知其他线程可以继续


import threading, time


def consumer(cond):
    logging.debug('Starting consumer thread')
    with cond:
        cond.wait(1)
        logging.debug('Resource is available to consumer')


def producer(cond):
    logging.debug('Starting producer thread')
    with cond:
        logging.debug('making resource availble')
        cond.notifyAll()


condition = threading.Condition()
c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
c2 = threading.Thread(name='c2', target=producer, args=(condition,))
p = threading.Thread(name='p', target=producer, args=(condition,))
c1.start()
time.sleep(3)
c2.start()
time.sleep(2)
p.start()

# 这些线程使用with来获得与condition关联的锁,也可以使用 acquire和release
