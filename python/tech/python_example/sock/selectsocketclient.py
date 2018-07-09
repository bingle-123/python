# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import select, socket, sys, queue

messages = [b'this is the message.',
            b'it will be sent',
            b'in parts', ]

socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM),
         socket.socket(socket.AF_INET, socket.SOCK_STREAM)]

for s in socks:
    s.connect(('localhost',10000))
for message in messages:
    for s in socks:
        print(' sending ')
        s.send(message)
    for s in socks:
        data=s.recv(1024)
        print(' received ')
        if not data:
            s.close()