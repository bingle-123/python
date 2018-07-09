# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

import os

# 临时文件
# TemporaryFile()打开并返回一个未命名的文件,
# NamedTemporaryFile()打开并返回一个命名文件
# mkdtemp()会创建一个临时目录,并返回其目录名


import tempfile
# TemporaryFile不论通过close()还是结合上下文管理器api和with语句来关闭文件,文件都会在关闭时自动删除

with tempfile.TemporaryFile(mode='w+t') as temp:
    temp.write('some data')
    temp.seek(0)
    print(temp.readline())
#     写文件之后,必须使用seek()"回转"文件句柄,这样才能够读取数据

# 有时候需要多个进程间使用临时文件,这时用namedtemporaryfile,创建后并不立即删除链接,所以会保留文件名
# 句柄关闭后文件会被删除


# shutil高级文件操作
# copyfile复制文件
# copytree()复制目录,递归便利源目录树
# rmtree()删除目录及其中内容,第二个参数为true,可以忽略异常


