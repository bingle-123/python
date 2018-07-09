# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 进程退出时生成的状态吗可以通过exitcode属性访问,
# ==0  未生成任何错误
# >0    进程有一个错误,并以该错误吗退出
# <0    进程有一个-1* exitcode信号结束

import multiprocessing, sys, time


def exit_error():
    sys.exit(1)


def exit_ok():
    return


def return_value():
    return 1


def raises():
    raise RuntimeError('there was an error!')


def terminated():
    time.sleep(3)


jobs = []
for f in [exit_error, exit_ok, return_value, raises, terminated]:
    print('starting process for ', f.__name__)
    j = multiprocessing.Process(target=f, name=f.__name__)
    jobs.append(j)
    j.start()
jobs[-1].terminate()
# jobs[-1].join()
for j in jobs:
    j.join()
    print('%15s.exitcode = %s ' % (j.name, j.exitcode))