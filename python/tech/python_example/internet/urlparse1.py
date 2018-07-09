# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import urllib.parse

url = 'http://netloc.com/path/path;param?query=arg#frag'
parsed = urllib.parse.urlparse(url)
print(parsed)
# urlparse()返回一个包含6个元素的tuple
# 分别是:机制,网络位置,路径,路径参数(由分号与路径分开),查询,片段
# 这个元祖是一个namedtuple,可以通过命名属性访问

# 反解析
# 还可以利用一些方法把分解的url的各个部分重新组装在一起,形成一个串适应 geturl()

url=parsed.geturl()
print(url)

# 链接
# 除了解析url外,urlparse还包括一个urljoin(),可以有相对片段构造绝对url

print(urllib.parse.urljoin('http://www.example.com/path/file.html','../another.html'))



# 参数编码,可以对参数编码并追加到URL,从而将他们传递到服务器.

query_args={'q':'query string','foo':'bar'}
encoded_args=urllib.parse.urlencode(query_args)

print(encoded_args)
url='http://localhost:8080/?'+encoded_args
print(url)


# 查询参数中可能有一些特殊字符,在服务器端对URL解析会出现问题,此时要用quote()或者quote_plus()进行编码
# unquote()和unquote_plus()可以逆解析url

print(urllib.parse.quote(urllib.parse.quote(url)))




