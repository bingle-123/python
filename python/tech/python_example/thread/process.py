import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s)%(message)s')


def worker():
    t = threading.currentThread()
    pause = random.randint(1, 5)
    logging.debug('sleep %s', pause)
    time.sleep(pause)
    logging.debug('ending')
    return


for i in range(3):
    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()

mainthread = threading.currentThread()
for t in threading.enumerate():
    if t is mainthread:
        continue
    logging.debug('joining %s', t.getName())
    t.join()


#
# def worker():
# logging.debug('Starting')
#     time.sleep(2)
#     logging.debug('Exiting')
#
#
# def myservice():
#     logging.debug('Starting')
#     # time.sleep(2)
#     logging.debug('Exiting')

# d=threading.Thread(name='daemon',target=worker)
# d.setDaemon(True)
# def worker():
# print(threading.currentThread().getName(), 'starting')
#     time.sleep(2)
#     print(threading.currentThread().getName(), 'exiting')
#     return
#
#
# def myservice():
#     print(threading.currentThread().getName(), 'starting')
#     time.sleep(2)
#     print(threading.currentThread().getName(), 'exiting')
#
#
# t = threading.Thread(name='myservice', target=myservice)
# w = threading.Thread(name='worker', target=worker)
# w2 = threading.Thread(target=worker)
# w.start()
# w2.start()
# d.start()
# t.start()
# d.join(1)
# print('d.alive',d.isAlive())
# t.join()

#
