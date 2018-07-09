# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )


# ElementTree,可以使用基于事件和基于文档的api解析xml,用xpath表达式搜索已解析的文档,还可以创建或修改现有文档

from xml.etree import ElementTree
# 用parse()解析一个完整文档时,会返回一个ElementTree实例
# 因为文档一次性加载,所以需要更多的内存

with open('xml.xml','rt') as f:
    tree=ElementTree.parse(f)

# 按顺序访问所有字节点,可以使用iter()创建一个生成器,迭代处理这个ElementTree
for node in tree.iter():
    print(node.tag)

# findall()用来查找包含更多描述性搜索特性的节点
# 可以用一个XPath参数来查找所有outline节点

tree.findall('.//outline')

