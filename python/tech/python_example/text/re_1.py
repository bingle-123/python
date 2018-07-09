# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# re最常见的用法就是搜索文本中的模式,search()函数取模式和要扫描的文本作为输入
# 如果找到这个模式则返回一个Match对象,如果未找到则返回None
# 每个Match对象包含有关匹配性质的信息,包括原输入字符串,
# 使用的正则表达式,以及模式在原字符串中处向的位置.
import re

pattern = 'this'
text = 'doese this text match the pattern'
match = re.search(pattern, text)
print([i for i in dir(match) if not i.startswith('__')])
print(match.start())
print(match.end())
print(match.endpos)
print(match.re)
print(match.string)


# 编译表达式
# re包含依稀模块级函数,用于处理作为文本字符串的正则表达式,
# 不过对于程序频繁使用的表达式,编译这些表达式会更为高校,
# compile()函数会把一个表达式字符串转换为一个RegexObject

import re

regexs = [re.compile(p) for p in ['this', 'that']]
text = 'dose this text match that pattern'
print('Text: ', text)
print([i for i in dir(regexs[0]) if not i.startswith('__')])
for regex in regexs:
    print('seeking: ', regex.pattern)

    if regex.search(text):
        print('match')
    else:
        print('no match')


# 多重匹配
# findall()函数会返回输入中与模式匹配而不重叠的所有字串
import re

text = 'abadsdfasfabaasdsadbbbb'
pattern = 'ab'
for match in re.findall(pattern, text):
    print('Found : ', match)

# finditer()会返回一个迭代器,它将生成Match实例,而不像findall()返回字符串
for match in re.finditer(pattern, text):
    s = match.start()
    e = match.end()
    print("Found: at", s, e)