# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
import hashlib
# hashlib用于生成消息内容的签名,
# hmac用于验证age消息在传输过程中未被修改

# md5
s = b'askjfajshduwhfjwqkfhqiuhwjkslhfduaslhdkjfwqhfiuhsdfkasfdjhk'
h = hashlib.md5()
h.update(s)
print(h.hexdigest())

print()
# sha1
h = hashlib.sha1()
h.update(s)
print(h.hexdigest())

# hmac
# new()函数会创建一个新的对象来计算消息签名

import hmac

digest_maker = hmac.new(b'secret-shared-key-goes-here')
with open('example.text', 'rb') as f:
    while True:
        block = f.read(1024)
        if not block:
            break
        digest_maker.update(block)
print(digest_maker.hexdigest())
# 这里会读取一个数据文件,为它计算一个HMAC签名

# hmac的默认密码算法是MD5,但这并不是最安全的方法,一般使用sha1更健壮

digest_maker = hmac.new(b'secret-shared-key-goes-here', b'', hashlib.sha1)
with open('example.text', 'rb') as f:
    while True:
        block = f.read(1024)
        if not block:
            break
        digest_maker.update(block)
print(digest_maker.hexdigest())


