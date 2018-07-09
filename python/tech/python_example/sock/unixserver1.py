# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import socket
import os
import sys
# unix套接字的地址是文件系统上的一个路径而不是一个包含服务器名和端口的元祖,
# 其次,文件系统中创建的表示套接字的节点会持久保存,即使套接字关闭也人然存在
# 所以每次服务器启动时都要将其删除

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
address = './uds_socket'
try:
    os.unlink(address)
except Exception:
    if os.path.exists(address):
        raise
sock.bind(address)
sock.listen(1)

while True:
    conn, client_addr = sock.accept()
    try:
        data = conn.recv(64)
        print(data)
        conn.sendall(b'hello there this is server')

    finally:
        conn.close()
        sys.exit(0)



