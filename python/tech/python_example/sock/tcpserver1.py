# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('', 8090)
sock.bind(address)
sock.listen(1)

print('wati accept')
conn, client_addr = sock.accept()
while True:
    data = conn.recv(16)
    if data:
        print(data)
        conn.sendall(data)
    else:
        conn.close()
        sock.close()
        break
