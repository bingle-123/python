# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import socket,sys,os

sevrver_address='./uds_socket'
try:
    os.unlink(sevrver_address)
except OSError:
    if os.path.exists(sevrver_address):
        raise
sock=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
print('starting up on %s'%sevrver_address)
sock.bind(sevrver_address)
sock.listen(1)
while True:
    print('wating for a connection')
    connection,client_address=sock.accept()
    try:
        print('connection from',client_address)
        while True:
            data=connection.recv(16)
            print('received ',data)
            if data:
                print('sending data back to the client')
                connection.sendall(data)
            else:
                print('no data from ', client_address)
                break
    finally:
        connection.close()
