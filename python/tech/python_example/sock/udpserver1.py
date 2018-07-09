# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("127.0.0.1", 9090)
sock.bind(address)
print('receive data')
while True:
    data,address=sock.recvfrom(4096)
    if data:
        print(data)
        sock.sendto(data,address)