# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import threading,time,logging,random
logging.basicConfig(level=logging.DEBUG,format='%(levelname)s (%(threadName)-10s) %(message)s',)
# 没有必要为所有守护线程维护一个显示的句柄来确保他们在退出主进程之前已经完成.
# enumerate()会返回活动Thread的实例的一个列表,这个列表也包含但前线程,由于等待
# 当前线程结束会引入一种死锁情况,所以必须将其跳过

def worker():
    # t=threading.currentThread()
    pause=random.randint(1,5)
    time.sleep(pause)
    logging.debug('ending')
    return

for i in range(3):
    t=threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()

mainthread=threading.currentThread()
for t in threading.enumerate():
    if t is mainthread:
        continue
    logging.debug('joining %s',t.getName())
    t.join()
