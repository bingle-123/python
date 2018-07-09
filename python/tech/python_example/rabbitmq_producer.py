# -*- coding: utf-8 -*-
import threading
import pika
import schedule
import time
import multiprocessing
import random


class Producer(object):
    def __init__(self, queue):
        self.queue = queue
        self.channel.queue_declare(queue=queue)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Producer, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
            try:
                credentials = pika.PlainCredentials('admin', 'admin')
                connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.111',
                                                                               credentials=credentials))
                cls._instance.connection = connection
                cls._instance.channel = connection.channel()

            except Exception as e:
                print e
                return None
        return cls._instance

    def publish(self, body):
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=body)

    def close(self):
        self.connection.close()
        self.__class__._instance = None

    def __del__(self):
        self.connection.close()
        self.__class__._instance = None
