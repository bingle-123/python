# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 守护进程,在所有子进程退出主进程之前不会退出,有些情况下,可能需要启动一个后台进程
# 它可以一直运行而不阻塞主进程退出,如果一个服务无法用一种容易的方法来中断进程
# 或者希望进程工作到一半时终止而不损坏或破坏数据,对于这些服务,使用守护进程就很有用
# 腰标志一个进程位守护进程,可以将其daemon属性设置为True,

import multiprocessing, time, sys


def daemon():
    p = multiprocessing.current_process()
    print('starting:', p.name, p.pid)
    sys.stdout.flush()
    time.sleep(5)
    print('exiting :', p.name, p.pid)
    sys.stdout.flush()
    sys.stdout.flush()


def nondaemon():
    p = multiprocessing.current_process()
    print('starting:', p.name, p.pid)
    sys.stdout.flush()
    print('exiting :', p.name, p.pid)
    sys.stdout.flush()


d = multiprocessing.Process(name='daemon', target=daemon)
d.daemon = True
n = multiprocessing.Process(name='nondaemon', target=nondaemon)
n.daemon = False
d.start()
time.sleep(1)
n.start()

# 要等待一个进程完成工作并退出,可以使用join()
d.join()


# 默认情况下join会无线阻塞,可以传入一个超时参数,即使进程没有在这个超时时间内完成,join()也会返回
d.join(2)
print(d.is_alive())
# 由于超时时间小于睡眠时间,所以join()返回之后进程仍然存活
