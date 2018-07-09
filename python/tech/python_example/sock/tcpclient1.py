# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
address=('0.0.0.0',8090)
sock.connect(address)

message='hello there server ,this is client'
sock.sendall(message.encode())

while True:
    data=sock.recv(16)
    if data:
        print(data)
    else:
        sock.close()
        break
