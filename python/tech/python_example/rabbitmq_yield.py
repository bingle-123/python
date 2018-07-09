# -*- coding: utf-8 -*-
import logging
import threading
from dateutil.relativedelta import relativedelta
import pika
from gevent import event
from time import sleep
import random
import sys
from Queue import Queue
from datetime import datetime
import gevent

_logger = logging.getLogger(__name__)


# 协程异步

# class Event(object):
#     def __init__(self, name):
#         self.name = name
#         self.listeners = set()
#
#     def listen(self, listener):
#         self.listeners.add(listener)
#
#     def fire(self):
#         for listener in self.listeners:
#             listener()
#
#
# class EventManager(object):
#     def __init__(self):
#         self.events = {}
#
#     def register(self, name):
#         self.events[name] = Event(name)
#
#     def fire(self, name):
#         self.events[name].fire()
#
#     def await(self, event_name):
#         self.events[event_name].listen(getcurrent().switch)
#         getcurrent().parent.switch()
#
#     def use(self, func):
#         return greenlet(func).switch


# event = EventManager()
# event.register("done")


def coroutine(func):
    def ret(*args, **kwargs):
        f = func(*args, **kwargs)
        f.next()
        return f

    return ret


@coroutine
def consumer(*args, **kwargs):
    # print "Wait to getting a task"
    # while 1:
    n = (yield)
    sleep(random.random() * 2)
    print args[-1]


messages = Queue(10)


def produce():
    global messages
    while 1:
        msg = messages.get()
        sleep(random.random() * 2)
        print msg


def consume(*args, **kwargs):
    print 'get %s at' % args[-1], datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    gevent.sleep()
    sleep(random.random() * 5)
    print 'doe %s at' % args[-1], datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def handler(ch, method, properties, body):
    global messages
    messages.put(body)
    # c = consumer(ch, method, properties, body)
    # c.send("task")


def start_consume():
    queues = ['street', 'name', 'age']
    credentials = pika.PlainCredentials('admin', 'admin')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.111',
                                                                   credentials=credentials))
    try:
        t = threading.Thread(target=produce)
        t.start()
        channel = connection.channel()
        for queue in queues:
            channel.queue_declare(queue=queue)
            channel.basic_consume(handler, queue=queue, no_ack=True)
        print "connected"
        channel.start_consuming()

    except KeyboardInterrupt:
        _logger.info('RabbitMQ connection close')
    except Exception as e:
        _logger.error(e.message)
        _logger.error('RabbitMQ Connection Error')
    finally:
        connection.close()
