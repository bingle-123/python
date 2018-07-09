# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 有两种方法指示一个具体类实现了一个抽象API:
# 显示地注册这个类,或者直接从抽象基类创建新的子类,
# 当类提供了所需的api是,可以使用register()类方法显示地添加一个具体类,但他不属于抽象基类的继承树

import abc
from abstract_class.abc1 import pluginbase


class Localbaseclass(object):
    pass


class registerImplementation(Localbaseclass):
    def load(self, input):
        return input.read()

    def save(self, output, data):
        return output.write(data)


pluginbase.register(registerImplementation)

# python2.x 可以

