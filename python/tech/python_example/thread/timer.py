import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s)%(message)s')

def delayed():
    logging.debug('worker running')
    # time.sleep(3)
    print('worker done %S',threading.currentThread().getName())
    return

t1=threading.Timer(3,delayed)
t1.setName('t1')
t2=threading.Timer(6,delayed)
t2.setName('t2')

logging.debug('starting timers')
t2.setDaemon(True)
t1.start()
t2.start()
t2.join()

logging.debug('waiting before canceling %s',t2.getName())
time.sleep(3)
logging.debug('canceling %s',t2.getName())
t2.cancel()


logging.debug('done')