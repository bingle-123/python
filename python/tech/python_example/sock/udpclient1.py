# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print('send data')
sock.sendto(b'hello there this is client', ('localhost', 9090))
data, server = sock.recvfrom(4096)
print(data)
sock.close()