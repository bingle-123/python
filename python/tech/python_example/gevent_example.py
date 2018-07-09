import gevent.monkey
gevent.monkey.patch_socket()

import gevent
import urllib2
import simplejson as json
urllib2.Request


def fetch(pid):
    response = urllib2.urlopen('http://www.baidu.com')

    print('Process %s:' % (pid, ))


def synchronous():
    for i in range(1, 10):
        fetch(i)


def asynchronous():
    threads = []
    for i in range(1, 10):
        threads.append(gevent.spawn(fetch, i))
    import pdb
    pdb.set_trace()
    gevent.joinall(threads)

asynchronous()


class A:
    def __init__(self, name):
        self.name = name
