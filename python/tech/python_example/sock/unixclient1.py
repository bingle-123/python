# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import socket,os

sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
address='./uds_socket'
sock.connect(address)
try :
    sock.sendall(b'hello there this is client')
    while True:
        data=sock.recv(16)
        if data:
            print(data)
        else:
            break
finally:
    sock.close()