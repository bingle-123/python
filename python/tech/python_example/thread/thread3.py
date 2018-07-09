# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
# 使用参数来标志或命名线程很麻烦,也没有必要,每个Thread实例都有一个名称,他又一个默认值
# 可以在创建线程时改变,如果服务器进程由不同的操作的多个服务线程构成,
# 在这样的服务器进程中,对线程命名就很有用
import threading
import time


def worker():
    print(threading.currentThread().getName(), 'Starting')
    time.sleep(2)
    print(threading.currentThread().getName(), 'Exting')


def myservice():
    print(threading.currentThread().getName(), 'Starting')
    time.sleep(3)
    print(threading.currentThread().getName(), 'Exiting')

t=threading.Thread(target=worker,name='worker').start()
s=threading.Thread(target=myservice,name='service').start()
# s2=threading.Thread(target=myservice).start()
