# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# abc的做法是将基类标志为抽象,然后注册具体类作为这个抽象基类的实现,
# 可以使用issubclass()或assistance()根据抽象类检查对象
# 设置新基类的__metaclass__为ABCMeta
# 使用abstractmethod()装饰符为这个类建立公共API
import abc


class pluginbase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def load(self, input):
        '''retrieve data'''

    @abc.abstractmethod
    def save(self, output, data):
        '''save data'''