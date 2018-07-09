# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import socket, sys, os

sevrver_address = './uds_socket'
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect(sevrver_address)
try:
    msg = b'this is a messave it will be repeated'
    sock.sendall(msg)
    amount = 0
    excepted = len(msg)
    while amount < excepted:
        data = sock.recv(16)
        amount += len(data)
        print('received ', data)
finally:
    sock.close()