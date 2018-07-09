# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
# thread 要完成一些基本初始化,然后调用其run()方法,
# 这会调用传递到构造函数的目标函数,腰创建Thread的一个子类,
# 需要覆盖run()来完成所需的工作
import  threading,logging
logging.basicConfig(level=logging.DEBUG,format='%(levelname)s (%(threadName)-10s) %(message)s',)

class mythread(threading.Thread):
    def run(self):
        logging.debug('running')
        return

for i in range(5):
    t=mythread()
    t.start()


