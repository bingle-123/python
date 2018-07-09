# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
# 示例程序都隐含的等待所有线程完成工作之后才退出,程序有时会创建一个线程作为守护线程
# 这个线程可以一直运行而不阻塞主程序退出,如果一个服务无法用一种容易的方法来中断,
# 或者希望线程工作到一半时终止而不损失或破坏数据,对于这些服务,使用守护线程就很有用,
# 要标志一个线程位守护线程,需要调用妻setDeamon()方法并提供参数True,默认情况下线程不作为守护线程
import threading,time,logging
logging.basicConfig(level=logging.DEBUG,format='%(levelname)s (%(threadName)-10s) %(message)s',)

def daemon():
    logging.debug('Starting')
    time.sleep(2)
    logging.debug('Exiting')

d=threading.Thread(target=daemon,name='daemon')
d.setDaemon(True)

def non_daemon():
    logging.debug('Starting')
    logging.debug('Exiting')

t=threading.Thread(target=non_daemon,name='non_daemon')
d.start()
t.start()
t.join()
# 要等待一个守护线程完成工作,需要使用join()
# d.join()
# t.join()
# 默认情况下join会无线阻塞,表示等待线程变为不活动所需要的时间