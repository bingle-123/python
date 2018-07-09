# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )

# UUID 1值使用主机的MAC地址计算,uuid模块使用getnode()来获取当前系统的MAC值
# 如果一个系统有多个网卡,相应有多个MAC地址,可能返回其中任意一个值


import uuid
# 要为一个主机生成UUID,由其MAC地址表示需要使用uuid1()函数
u = uuid.uuid1()

# UUID3和5----基于名字的值
# 有些情况下可能需要根据名字创建UUID,而不是根据随机值或基于时间的值来创建.
# uuid3和5规范使用密码散列值(分别使用MD5和SHA1),将特定于命名空间的种子值与名字相结合.


# UUID4
# 有时基于主机和基于命名空间的UUID值差别还不够大,这就需奥区分度更大,更随机的值序列来避免散列表冲突

u = uuid.uuid4()