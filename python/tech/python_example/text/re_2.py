# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# . 表示该位置的任何单字符
# * 表示前面的字符出现多次或不出现
# + 前面的字符出现一次或多次
# ? 前面的字符出现一次或不出现
# [ab]表示字符集中的一个出现
# [^ab]表示不出现字符集中的任意一个
# {3},{2,4}表示前面字符出现的次数
# [a-z][A-Z][0-9][a-zA-Z0-9]

# 可以对一些预定义的字符集使用转义码
# \d 一个数字
# \D 一个非数字
# \s 空白格
# \S 非空白格
# \w 字母数字
# \W 非字母数字
# 对转义字符要使用原始字符串 r'\d+' 或者'\\d+'

# 除了描述腰匹配的模式的内容外,还可以指定锚定指令指定输入文本模式应当出现的相对位置
# ^ 字符串或行的开始
# $ 字符串或行的结束
# \A 字符串开始
# \Z 字符串结束
# \b 一个单词开头或末尾的空串
# \B 不再一个单词开头或末尾的空串



# 以编译的正则表达式的search()方法还接受可选的start和end位置参数
import re

text = r'this is some text'
pattern = re.compile(r'\b\w*is\w*\b')
m = pattern.findall(text)
for i in m:
    print(i)
