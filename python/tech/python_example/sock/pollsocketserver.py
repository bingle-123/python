# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

import select, socket, sys, queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
server.bind(server_address)
server.listen(5)
message_queues = {}
# 传入poll()的超时值用毫秒表示,而不是秒
TIMEOUT = 1000
# python用一个类来实现poll(),由这个类来管理锁监视的注册数据通道,
# 通道通过调用register()添加,同时利用标志指示该通道关注哪些事件
# POLLIN  输入准备就绪
# POLLPRI 优先级输入准备就绪
# POLLOUT 能够接受输出
# POLLERR 错误
# POLLHUP 通道关闭
# POLLNVAL 通道未打开

READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
READ_WRITE = READ_ONLY | select.POLLOUT
poller = select.poll()
poller.register(server, READ_ONLY)
# 由于poll（）返回一个元祖列表，云组中包含套接字的文件描述符和事件标志，因此需要一个文件
# 描述符编号到对象的映射来获取socket，以便读取或写入

fd_to_socket={server.fileno():server}
# 服务器的循环调用poll（）然后处理通过查找套接字返回的“事件”，并根据事件中的标志采取行动
while True:
    print('waiting for the next event')
    events=poller.poll(TIMEOUT)
    for fd,flag in events:
        s=fd_to_socket[fd]
        if flag&(select.POLLIN|select.POLLPRI):
            if s is server:
                connection,client_address=s.accept()
                print('connection',client_address)
                connection.setblocking(0)
                fd_to_socket[connection.fileno()]=connection
                poller.register(connection,READ_ONLY)
                message_queues[connection]=queue.Queue()
# 除了服务器以外，其他套接字都是现有的客户，其数据已经缓存
# 并等待读取，可以用recv()从缓冲区获取数据。
            else:
                data=s.recv(1024)
                if data:
                    print('received %s from %s'%(data,s.getpeername()))
                    message_queues[s].put(data)
                    poller.modify(s,READ_ONLY)
#recv()返回空串表示客户已经断开了链接，所以使用unregister（）告诉poll对象忽略这个套接字

                else:
                    print('closing',client_address)
                    poller.unregister(s)
                    s.close()
                    del message_queues[s]
# POLLHUP表示一个客户‘挂起’链接而没有将其妥善的关闭，服务器不会轮寻消失的客户
        elif flag & select.POLLHUP:
            print('closing ',client_address)
            poller.unregister(s)
            s.close()
# 可写套接字的处理看起来与select（）例子中的版本类似，
# 不过使用了modify（）来改变轮寻服务器中套接字的标志，
# 而不是将其从输出列表中删除
        elif flag|select.POLLOUT:
            try:
                next_msg=message_queues[s].get_nowait()
            except queue.Empty:
                print('queue empty')
                poller.modify(s,READ_ONLY)
            else:
                print('sending %s to %s'%(next_msg,s.getpeername()))
                s.send(next_msg)
# 任何有POLLERR标志的事件会导致服务器关闭套接字
        elif flag & select.POLLERR:
            print('exception on ',s.getpeername())
            poller.unregister(s)
            s.close()
            del message_queues[s]







