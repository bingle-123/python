# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import select,socket,sys,queue

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setblocking(0)
server.bind(('localhost',10000))
server.listen(5)
inputs=[server]
outputs=[]
# '''
# 由服务器主循环向这些列表中添加或删除链接,
# 由于这个版本的服务器在发送数据之前要等待一个套接字变为可写
# 而不是立即发送应答,所以每个输出链接都需要一个队列,
# 作为通过这个套接字发送的数据的缓冲区
# '''
message_queue={}
while inputs:
    readable,writebale,exceptional=select.select(inputs,outputs,inputs)

# select()返回3个新列表,包含锁传入列表内容的子集,
# readable列表中的所有套接字会缓存到来的数据,可供读取
# writeable列表中所有套接字的缓冲区中有自由空间,可以写入数据.
# exceptional中返回的套接字都有一个错误('异常条件'的具体定义取决于平台)
# '可读'套接字表示3种可能的情况
# 如果套接字是主'服务器'套接字,即用来监听链接的套接字,'可读'条件以为着他已经准备就绪,可以接受另一个到来的链接
# 除了将新链接添加到腰监视的输入列表之外,这一部分还将客户套接字设置为非阻塞.

    for s in readable:
        if s is server:
            connection,client_address=s.accept()
            print('connection from ',client_address)
            connection.setblocking(0)
            inputs.append(connection)
#           设置一个链接队列,用来发送数据
            message_queue[connection]=queue.Queue()
# '''
# 下一种情况是已建立的链接,客户已经发送了数据,数据用recv()读取,
# 然后放置在队列中,以便通过套接字发送并返回给客户
# '''
        else:
            data=s.recv(1024)
            if data:
                print('received from ',s.getpeername())
                message_queue[s].put(data)
                if s not in outputs:
                    outputs.append(s)
# '''
# 没有可用数据的可读套接字来字节断开链接的客户,此时可以关闭流
# '''
            else:
                print('closing ',client_address)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queue[s]

# '''
# 对于可写链接,情况腰少一些,如果对应一个链接的队列中有数据,则发送下一个消息,
# 否则,将这个链接从输出链接列表中删除,下一次循环时,
# select()不再指示这个套接字以准备好就绪可以发送数据
# '''
    for s in writebale:
        try:
            next_msg=message_queue[s].get_nowait()
        except queue.Empty:
            print('queue empty')
            outputs.remove(s)
        else:
            print('sending data to ',s.getpeername())
            s.send(next_msg)
# '''
# 最后一点,如果一个套接字有错误,则会关闭
# '''
    for s in exceptional:
        print('exception condition on ',s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queue[s]
