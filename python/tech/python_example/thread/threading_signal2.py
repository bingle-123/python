# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
# 尽管在任何线程中都能设置闹铃,但总是有主线程接收

import signal, time, threading


def signalhandler(num, stack):
    print(time.ctime(), 'Alarm in ', threading.currentThread().getName())

signal.signal(signal.SIGALRM,signalhandler)
def usealarm():
    tname=threading.currentThread().getName()
    print(time.ctime(),'Setting alarm in ',tname)
    signal.alarm(1)
    print(time.ctime(),'Sleeping in ',tname)
    time.sleep(1)
    print(time.ctime(),'Done with sleep in ',tname)

alarmt=threading.Thread(target=usealarm,name='alarm_thread')
alarmt.start()

print(time.ctime(),'waiting for ',alarmt.name)
alarmt.join()
time.sleep(1)
print(time.ctime(),'Exiting normally')