# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import threading
# 创建一个线程,并向他传递参数告诉他腰完成什么工作,这回很有用,任何类型的对象都可以作为
# 参数传递到线程
def worker(num):
    print('worker:%s'%num)

for i in range(5):
    threading.Thread(target=worker,args=(i,)).start()
