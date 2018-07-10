question





线程池的回调函数

*   将前面函数的返回值作为后面的结果进行传递
*   `future.add_done_callback(add1000)`
*   `num = future.result()`

```python
import time

from concurrent.futures import ThreadPoolExecutor


def add100(num):
    print('我是 100 ')
    return num + 100


def add1000(future):
    print('我是 + 1000')
    num = future.result()
    time.sleep(5)
    print(num + 1000)


def main():
    pool = ThreadPoolExecutor(3)  # 设置线程为 3
    for num in range(1,50):
        print('开始计算数字：%s ！' % num)
        future = pool.submit(add100, num)
        future.add_done_callback(add1000)  # 前面的结果返回后进行下个函数的调用


if __name__ == '__main__':
    main()
```



运行结果, （为什么结果会出现一次增加很多到线程池中）

```python
开始计算数字：1 ！  # 开始为什么是一个一个执行的
我是 100 
我是 + 1000
1101
开始计算数字：2 ！
我是 100 
我是 + 1000
1102
开始计算数字：3 ！
我是 100 
我是 + 1000
1103
开始计算数字：4 ！
开始计算数字：5 ！
我是 100 
开始计算数字：6 ！
我是 + 1000
我是 100 
开始计算数字：7 ！
我是 + 1000
我是 100 
开始计算数字：8 ！
我是 + 1000
开始计算数字：9 ！   # ？？？？
开始计算数字：10 ！
开始计算数字：11 ！
开始计算数字：12 ！
开始计算数字：13 ！
开始计算数字：14 ！
开始计算数字：15 ！
开始计算数字：16 ！
开始计算数字：17 ！
开始计算数字：18 ！
开始计算数字：19 ！
开始计算数字：20 ！
开始计算数字：21 ！
开始计算数字：22 ！
开始计算数字：23 ！
开始计算数字：24 ！
开始计算数字：25 ！
开始计算数字：26 ！
开始计算数字：27 ！
开始计算数字：28 ！
开始计算数字：29 ！
开始计算数字：30 ！
开始计算数字：31 ！
开始计算数字：32 ！
开始计算数字：33 ！
开始计算数字：34 ！
开始计算数字：35 ！
开始计算数字：36 ！
开始计算数字：37 ！
开始计算数字：38 ！
开始计算数字：39 ！
开始计算数字：40 ！
开始计算数字：41 ！
开始计算数字：42 ！
开始计算数字：43 ！
开始计算数字：44 ！
开始计算数字：45 ！
开始计算数字：46 ！
开始计算数字：47 ！
开始计算数字：48 ！
开始计算数字：49 ！
1104
1106
1105
我是 100 
我是 100 
我是 100 
我是 + 1000
我是 + 1000
我是 + 1000
1109
1107
1108
我是 100 
我是 100 
我是 100 
我是 + 1000
我是 + 1000
我是 + 1000
1111
1110
1112
我是 100 
我是 100 
我是 100 
我是 + 1000
我是 + 1000
我是 + 1000
1115
1113
1114
我是 100 
我是 100 
我是 100 
我是 + 1000
我是 + 1000
我是 + 1000
1117
1118
1116
我是 100 
我是 100 
我是 100 
我是 + 1000
我是 + 1000
我是 + 1000
1119
1120
1121
我是 100 
我是 100 
我是 100 
我是 + 1000
我是 + 1000
我是 + 1000
1122
我是 100 
我是 + 1000
1123
我是 100 
我是 + 1000
1124
我是 100 
我是 + 1000
1125
1126
1127
我是 100 
我是 100 
我是 100 
我是 + 1000
我是 + 1000
我是 + 1000
1129
1128
1130
```




