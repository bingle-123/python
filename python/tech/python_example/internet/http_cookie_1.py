# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )


# 可以用cookie为基于浏览器的应用实现状态管理,
# 因此,cookie通常有服务器设置,并有客户存储和返回.

import http.cookies

scookie = http.cookies.SimpleCookie()
scookie['session'] = 'asdfasdf'
print(scookie)

# 还可以控制cookie的其他方面,入到期时间,路径,和域
# 实际上所有RFC属性都可以通过表示cookie的Morsel对象来管理
session = scookie['session']
print(session.key)
print(session.value)
print(session.coded_value)
print(dir(session))

c = http.cookies.SimpleCookie()
c['restricted_cookie'] = 'cookie_value'
c['restricted_cookie']['path'] = '/sub/path'
c['restricted_cookie']['domain'] = 'PyMOTW'
c['restricted_cookie']['secure'] = True
c['with_max_age']='expires in 5 minutes'
c['with_max_age']['max-age']=300
# .............
