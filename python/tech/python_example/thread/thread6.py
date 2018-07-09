# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import threading,time,logging
logging.basicConfig(level=logging.DEBUG,format='%(levelname)s (%(threadName)-10s) %(message)s',)

def daemon(n):
    logging.debug('Starting')
    time.sleep(n)
    logging.debug('Exiting')

d=threading.Thread(target=daemon,name='daemon',args=[5])
d.setDaemon(True)

def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')

t=threading.Thread(target=non_daemon,name='non_daemon')
d.start()
t.start()

# 默认情况下join会无线阻塞,表示等待线程变为不活动所需要的时间


d.join(1)
# t.join()
print('d.isAlive',d.isAlive())