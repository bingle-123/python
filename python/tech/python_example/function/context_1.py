# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 上下温管理器腰负责一个代码块中的资源,可能在进入代码块时创建资源,然后在退出代码块时清理这个资源
# 例如支持上下文管理器api,可以很容易的确保完成文件读写后关闭文件

with open('/tmp/ss.test', 'wt') as f:
    f.write('something lost')

# 上下文管理器由with语句启用,这个api包括两个方法,
# 当执行流进入with中的代码块的时会运行__enter__()方法,他会返回一个对象,在这个上下文中使用
# 当执行流离开with块时,则调用这个上下文管理器的__exit__()方法来清理所使用的资源

# class Context():
#     def __init__(self):
#         print('__init__')
#
#     def __enter__(self):
#         print('__enter')
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('__exit__')
#
#
# with Context():
#     print('Do something work in the context')

# 结合上下文管理器与with语句是try:finally块的一种更为紧凑的写法
# 因为上下文管理器的__exit__()方法总会调用,即使产生异常也是如此

# 如果在with语句的as字句制定了名称,__enter__()方法可以返回与这个名称相关联的任何对象

class WithinContext():
    def __init__(self):
        print('withincontext __init__')

    def do_something(self):
        print("withincontext do something")

    def __del__(self):
        print('withincontext __del__')


class Context():
    def __init__(self):
        print('Context __init__')

    def __enter__(self):
        print('Context __enter__')
        return WithinContext()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Context __exit__')


with Context() as c:
    c.do_something()


# __exit__()方法接收一些参数,其中包含with块中产生的异常的详细信息

class Context():
    def __init__(self):
        print('Context __init__')

    def __enter__(self):
        print('Context __enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Context __exit__')
        print(exc_type)
        print(exc_val)
        print(exc_tb)

with Context():
    raise RuntimeError('erro ')