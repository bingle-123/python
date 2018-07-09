# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
#除了同步线程操作之外,还有一点很重要,要能够控制对资源的访问,从而避免破坏或丢失数据,
# python的内置数据结构是线程安全的,这是python使用原子字节吗来管理这些数据结构的一个副作用(更新过程不会释放GIL)
# python中实现的其他数据结构或更简单的类型,则没有这个保护,要保证同时安全的访问一个对象,可以使用一个Lock对象


import threading,random,time

class Counter(object):
    def __init__(self,start=0):
        self.lock=threading.Lock()
        self.value=start

    def increment(self):
        logging.debug('waiting for lock')
        self.lock.acquire()
        try:
            logging.debug('acquire lock')
            self.value+=1

        finally:
            self.lock.release()

def worker(c):
    for i in range(2):
        pause=random.random()
        logging.debug('sleeping %0.02f',pause)
        time.sleep(pause)
        c.increment()
    logging.debug('Done')

counter=Counter()
for i in range(4):
    t=threading.Thread(target=worker,args=(counter,))
    t.start()

logging.debug('waiting for worker threads')

mainthread=threading.currentThread()

for t in threading.enumerate():
    if t is not mainthread:
        t.join()

logging.debug('counter: %d',counter.value)
