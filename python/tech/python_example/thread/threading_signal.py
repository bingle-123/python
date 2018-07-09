# # -*- coding:utf-8 -*-
# __author__ = 'mering Gao'
# # 信号和线程通常不能很好的结合,因为只有进程的主线程可以接受信号,
# # 下面的列子建立了一个信号处理程序,他在一个线程中等待信号,
# # 而从另一个线程发送信号.
# import signal
# import threading
# import os
# import time
#
#
# def signalhandler(num, stack):
# print('received signal %d in %s' % (num, threading.currentThread().getName()))
# # signal.pause()
#
# signal.signal(signal.SIGUSR1, signalhandler)
#
#
# def waitforsignal():
#     print('waiting for sinal in ', threading.currentThread().getName())
#     signal.pause()
#     print('done waiting')
# # 尽管接受这线程调用恶狼signal.pause(),但它不会接受信号,
# # 这个列子接近结束时的signal.alarm(2)调用避免无线阻塞,
# # 因为接受者线程永远不会退出
#
# receiver=threading.Thread(target=waitforsignal,name='reveiver')
# receiver.start()
# time.sleep(0.1)
#
# def sendsignal():
#     print('sending signal in ',threading.currentThread().getName())
#     os.kill(os.getpid(),signal.SIGUSR1)
#
# sender=threading.Thread(target=sendsignal,name='sender')
# sender.start()
# sender.join()
#
# print('waiting for ',receiver.name)
# signal.alarm(2)
#
# receiver.join()
#
import threading
# # main_thread=threading.currentThread()
# # for i in threading.enumerate():
# #     if i is main_thread:
# #         break
# #     else:
# #         i.join()

class MyThread(threading.Thread):
    def __init__(self, target=None, group=None, name=None, args=(), kwargs=None):
        threading.Thread.__init__(self, group=group, name=name, target=target, args=args, kwargs=kwargs)
        self.args = args
        self.kwargs = kwargs
        self.target=target

    def run(self):
        self.target(self.args)
        print(self.args, self.kwargs)


def threadfun(ss):
    print(ss,threading.currentThread().name)


for i in range(4):
    t = MyThread(args=(1, 2, 4), kwargs={}, target=threadfun)
    t.start()


