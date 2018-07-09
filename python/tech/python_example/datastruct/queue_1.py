# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# Queue模块提供了一个适用于多线程编程的先进先出数据结构,
# 可以哟拿来在生产者和消费者线程之间安全的传递消息或其他数据,
# 它会为h调用者处理锁定,使多个线程可以安全的处理一个Queue实例,
# Queue的大小可能要受限,以限制内存使用或处理

import queue

q = queue.Queue()
for i in range(5):
    q.put(i)
while not q.empty():
    print(q.get())


# LIFO Queue使用了先进后出顺序(通常与栈数据结构关联)

s = queue.LifoQueue()
for i in range(5):
    s.put(i)

while not s.empty():
    print(s.get())

# 优先队列
# 有些情况下,队列中元素的处理顺序要根据这些元素的特性来决定,
# 而不只是在队列中创建或插入的顺序,
# 例如财务本门打印作业可能优先于一个开发人员

q = queue.PriorityQueue()

import threading


class Job:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
        print('new job')

    def __cmp__(self, other):
        return self.priority-other.priority


q.put(Job(3, 'job 3'))
q.put(Job(10, 'job 10'))
q.put(Job(1, 'job 1'))


def process_job(q):
    while True:
        next_job = q.get()
        print('processing job:', next_job.description)
        q.task_done()


workers = [
    threading.Thread(target=process_job, args=(q,)),
    threading.Thread(target=process_job, args=(q,))
]

for w in workers:
    w.setDaemon()
    w.join()

q.join()
