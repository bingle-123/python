# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 用模式匹配修改字符串
# 使用sub()可以将一个模式的所有出现替换为另一个字符串
import re

text = 'make this **bold**. This **too**'
regex = re.compile(r'\*{2}(.*?)\*{2}')
print(regex.sub(r'<b>\1</b>', text))
# 可以用向后引用的\num语法插入与模式匹配的文本的引用

# 要在替换中使用命名组,可以使用语法\g<name>

regex=re.compile(r'\*{2}(?P<bold_text>.*?)\*{2}')
print(regex.sub(r'<b>\g<bold_text></b>', text))
