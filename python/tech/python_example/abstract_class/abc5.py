# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )
# 如果api规范除了方法外还包含属性,可以用@abstractpropertydingier来要求具体类中应包含这些属性

import abc


class Base():
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def value(self):
        return 'should never get here'

    @abc.abstractproperty
    def constant(self):
        return 'should never get here'


class Implementation(Base):
    @property
    def value(self):
        return 'concrete property'

    constant = 'set by a class attribute'


try:
    b = Base()
    print('base.value', b.value)
except Exception as err:
    print('Error', str(err))

i=Implementation()
print('Implementation.value',i.value)
print('Implementation.constant',i.constant)