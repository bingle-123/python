# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import signal
import os
import time
# 忽略信号需要注册sig_ign作为处理程序
def doexit(sig,stack):
    raise SystemExit('Exiting')

signal.signal(signal.SIGINT,signal.SIG_IGN)
signal.signal(signal.SIGUSR1,doexit)

print('my pid:',os.getpid())
signal.pause()