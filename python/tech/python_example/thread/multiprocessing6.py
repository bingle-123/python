# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 尽管最好使用'毒丸'(poison pill)方法向进程发出信号告诉他应当退出,但是如果一个进程看起来已经挂起,或陷入死锁,
# 则需要能够强制性地将其结束,
# 对一个进程对象调用terminate()会结束进程

import multiprocessing, time


def slow_worker():
    print('Starting worker')
    time.sleep(0.1)
    print('finished worker')


p = multiprocessing.Process(target=slow_worker)
print('before:', p, p.is_alive())
p.start()
print('during:', p, p.is_alive())
p.terminate()
print('terminated', p, p.is_alive())
p.join()
print('joined:', p, p.is_alive())

# 终止进程腰使用join()退出进程,使进程管理代码有时间更新对象的状态,以反映进程已经终止
