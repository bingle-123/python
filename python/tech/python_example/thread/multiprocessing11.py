# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 如果需要在多个进程间共享一个资源,在这种情况下,可以使用一个lock来避免访问冲突

import multiprocessing
import sys


def worker(lock, stream):
    with lock:
        stream.write('Lock acquired via with\n')


def worker_no_with(lock, stream):
    lock.acquire()
    try:
        stream.write('Lock acquired directly\n')
    finally:
        lock.release()


lock = multiprocessing.Lock()

w = multiprocessing.Process(target=worker, args=(lock, sys.stdout))
nw = multiprocessing.Process(target=worker_no_with, args=(lock, sys.stdout))

w.start()
nw.start()
w.join()
nw.join()

# 如果两个进程没有用锁同步其输出流访问,打印到控制台的消息可能就会纠结在一起



