# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 通过派生实现

import abc
from abstract_class.abc1 import pluginbase


class subclassimplementation(pluginbase):
    def load(self, input):
        return input.read()

    def save(self, output, data):
        return output.write(data)


print('sbclass', issubclass(subclassimplementation, pluginbase))
print('instance', isinstance(subclassimplementation, pluginbase))

# 除非 子类 完全实现了api的抽象部分,否则子类不能被实例化

