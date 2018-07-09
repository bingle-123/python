# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 有些情况下,所需要完成的工作可以分解并独立的分布到多个工作进程,对于这中简单的情况
# 可以用Pool类来管理固定数目的工作进程,作业的返回值会收集并作为一个列表返回,
# 池(Pool),参数包括进程数以及启动任务进程时要运行的函数
import time,random
import multiprocessing


def do_calculation(data):
    return data * 2


def start_process():
    print('Starting', multiprocessing.current_process().name)


inputs = list(range(10))
print('Input :', inputs)
builtin_outputs = map(do_calculation, inputs)
print('built_in:', builtin_outputs)

pool_size = multiprocessing.cpu_count() * 2
pool = multiprocessing.Pool(processes=pool_size, initializer=start_process, )
pool_outputs = pool.map(do_calculation, inputs)
pool.close()
pool.join()
print('Pool :', pool_outputs)