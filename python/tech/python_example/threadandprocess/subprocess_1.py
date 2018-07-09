#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import logging
import queue
import threading
import sys

def func_a(a, b):
    return a + b


def func_b():
    pass


def func_c(a, b, c):
    return a, b, c

# 异步任务队列
task_queue = queue.Queue()


class minque(object):
    def __init__(self):
        self.queue=queue.Queue()
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(minque, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def async_call(self, function, callback, *args, **kwargs):
        self.queue.put({
            'function': function,
            'callback': callback,
            'args': args,
            'kwargs': kwargs
        })

    def _task_queue_consumer(self):
        """
        异步任务队列消费者
        """
        while True:
            try:
                task = self.queue.get()
                function = task.get('function')
                callback = task.get('callback')
                args = task.get('args')
                kwargs = task.get('kwargs')
                try:
                    if callback:
                        callback(function(*args, **kwargs))
                except Exception as ex:
                    if callback:
                        callback(ex)
                finally:
                    self.queue.task_done()
            except Exception as ex:
                logging.warning(ex)

    def handle_result(self, result):
        print(type(result), result)

    def run(self):
        t = threading.Thread(target=_task_queue_consumer)
        t.daemon = True
        t.start()
        # t.join()


task_queue = minque()
task_queue.queue = queue.Queue()


def async_call(function, callback, *args, **kwargs):
    task_queue.queue.put({
        'function': function,
        'callback': callback,
        'args': args,
        'kwargs': kwargs
    })


def _task_queue_consumer():
    """
    异步任务队列消费者
    """
    while True:
        try:
            task = task_queue.queue.get()
            function = task.get('function')
            callback = task.get('callback')
            args = task.get('args')
            kwargs = task.get('kwargs')
            try:
                if callback:
                    callback(function(*args, **kwargs))
            except Exception as ex:
                if callback:
                    callback(ex)
            finally:
                task_queue.queue.task_done()
        except Exception as ex:
            logging.warning(ex)


def handle_result(result):
    sys.stdout.write(str(result))


if __name__ == '__main__':
    t = threading.Thread(target=_task_queue_consumer)
    t.daemon = True
    t.start()
    import time
    # for i in range(10):
    # time.sleep(5)

    async_call(func_a, handle_result, 1, 2)
    async_call(func_b, handle_result)
    async_call(func_c, handle_result, 1, 2, 3)
    async_call(func_c, handle_result, 1, 2, 3, 4)

    task_queue.queue.join()
    t.join()
