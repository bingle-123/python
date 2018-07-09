# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# gzip

import gzip
# open()函数创建类文件的类GzipFile的一个实例,提供读写数据的常用方法

outfile = 'file.txt.gz'
with gzip.open(outfile, 'wb') as output:
    output.write(b'contents of the example file go here.\n')

# 通过传入一个压缩级别参数(1~9),可以使用不同的压缩量,
outfile = 'file2.txt.gz'
with gzip.open(outfile, 'wb', 9) as output:
    output.write(b'contents of the example file go here.\n')

# 读压缩文件
outfile = 'file2.txt.gz'
with gzip.open(outfile, 'rb') as output:
    print(output.read())

print()


# tarfile
import tarfile

# is_tarfile函数返回一个布尔值,指示作为参数传入的文件名是否指向一个合法的tar归档文件
from contextlib import closing
# 读tar文件
with closing(tarfile.open('example.tar', 'r')) as t:
    t.getnames()

# 抽取tar中文件
# 要在程序中访问一个归档成员的数据,可以使用extractfile(),并传入这个成员名
# 他的返回值是一个类文件对象,可以从这个对象读取归档成员的内容
f = t.extractfile('filename')

# 解压缩tar文件
# extract()或extractall(),extractall()比extract()更安全所以通常使用extractall()
t.extractall('dirname')
t.extract('filename', 'dirname')


# 创建归档文件
# 创建归档文件是使用'w'打开TarFile

with closing(tarfile.open('tarfilename.tar','w')) as out:
    out.add('filename')
# 追加到归档文件以 'a' 打开tar文件


# zipfile
import zipfile
# is_zipfile函数返回一个布尔值,指示作为参数传入的文件名是否指向一个合法的zip归档文件

# 读取zip文件

with zipfile.ZipFile('filename.zip','r') as zf:
    zf.getinfo()

# 从zip中抽取文件
with zipfile.ZipFile('filename.zip','r') as zf:
    zf.read('filename')

# 创建新的zip文件 使用'w'
with zipfile.ZipFile('filename.zip','w') as zf:
    zf.write('filename')
# 追加zip文件 使用'a'
with zipfile.ZipFile('filename.zip','a') as zf:
    zf.write('filename')



