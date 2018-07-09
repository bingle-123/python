# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 用组解析匹配
# 通过将模式包围在小括号中来分组
# 'a(a*b*)' 'a(ab)+'

# 要访问一个模式中单个组锁匹配的字串,可以使用Match对象的groups()方法
import re

text = 'this is some text -- with punctuation'
patterns = [r'(\w+)(.*)', r'(\w+)\S*$']
for pattern in patterns:
    regex = re.compile(pattern)
    match = regex.search(text)
    print('------------------')
    print(match.groups())

    # Match.gourps()会匹配表达式中与字符串匹配的组的顺序返回一个字符串序列.

    # 使用group()可以达到某个组的匹配,如果使用分组来查找字符串的各个部分,
    # 不过结果中并不需要某些与组匹配的部分,此时group()会很有用
    print(match.group(0))
    print(match.group(1))
    print('++++++++++++++++')



# python对基本分组语法做了z扩展,增加了命名组,通过使用名字来指示组
# 这样以后就可以更容易的修改模式,而不必同时修改使用了匹配结果的代码,
# 要设置一个组的名字,可以使用一下语法(?P<name>pattern)

patterns = [r'^(?P<first_word>\w+)', r'(?P<last_word>\w+)\S*$']
for pattern in patterns:
    regex=re.compile(pattern)
    match=regex.search(text)
    print(match.groups())
    print(match.groupdict())


