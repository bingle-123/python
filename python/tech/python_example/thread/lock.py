import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s)%(message)s')


class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        self.value = start

    def increment(self):
        logging.debug('waiting for lock')
        self.lock.acquire()
        try:
            logging.debug('Acquire lock')
            self.value = self.value + 1
            print('count:::', self.value)
        finally:
            # return
            self.lock.release()


def worker(c):
    for i in range(2):
        pause = random.random()
        logging.debug('sleeping %0.02f', pause)
        time.sleep(pause)
        c.increment()
    logging.debug('Done')


counter = Counter()
for i in range(2):
    t = threading.Thread(target=worker, args=(counter,))
    t.start()

logging.debug('waiting for worker threads')
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        # t.join()
        continue

logging.debug('Counter: %d', counter.value)