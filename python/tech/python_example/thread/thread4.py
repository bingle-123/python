# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
# 大多数程序不用print来进行测试,logging模块支持线程名嵌入到各个日志消息中
# 使用格式化代码%(threadName)s,通过将线程名包含在日志消息中,这样就能跟踪这些消息的来源
import logging,threading,time

logging.basicConfig(level=logging.DEBUG,format='%(levelname)s (%(threadName)-10s) %(message)s',)

def worker():
    logging.debug('Starting')
    # time.sleep(2)
    logging.debug('Exiting')

def myservice():
    logging.debug('Starting')
    # time.sleep(3)
    logging.debug('Exiting')

t=threading.Thread(target=worker,name='worker').start()
s=threading.Thread(target=myservice,name='worker2').start()
s2=threading.Thread(target=myservice).start()