# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# 具体类必须提供所有抽象方法的实现,不仅如此,抽象基类也可以提供实现,
# 可以通过super()来调用,这就允许将公共逻辑放在基类中从而得到重用,而要求子类用
# 定制逻辑提供一个覆盖方法

import abc


class abcbase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def prints(self, inputs):
        print(inputs)
        return inputs


class imabcbase(abcbase):
    def prints(self, inputs):
        basedata = super(imabcbase, self).prints(inputs)
        print(basedata)
        return


inputs = 'some string'
reader = imabcbase()
reader.prints(inputs)