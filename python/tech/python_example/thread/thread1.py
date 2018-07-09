# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import threading

# 用一个目标函数实例化一个Thread对象,并调用start()让它开始工作

def worker():
    print('Worker')


threads = []
for t in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()

