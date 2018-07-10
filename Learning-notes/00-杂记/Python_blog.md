# Python_blog



# 博客-note

## `一`LuoH-blog



```python
import matplotlib.pyplot as plt


def main():
    x_values = [x for x in range(10)]
    y_values = [x ** 2 for x in range(1, 11)]
    plt.title('Square Number')
    plt.xlabel('Value', fontsize=18)
    plt.ylabel('Square', fontsize=18)
    plt.tick_params(axis="both", labelsize=16)
    plt.scatter(x_values, y_values)  # plot可绘制曲线图
    plt.show()
    可能大家已经注意到了，1和10对应的‘x’记号在图形边角的位置不太明显，要解决这个问题可以通过添加下面的代码调整x轴和y轴的坐标范围。

	plt.axis([0, 12, 0, 120])
```



## `二`廖雪峰_博客 Python

## `2.1`高阶函数小结

```python 
1.  
enumerate([1, 2 , 4])  :   将列表中的元素以及对应的下标组成一个元组输出   没有返回值 需要进行实体化操作(用容器进行)  如:list/tuple/dict

2.
isinstance(object, type)   判断传入的 object 是否是 type 类型 返回布尔值
 
3. 
map()  接受两个参数,一个是函数, 一个是Iterable, 将传入的函数依次作用在序列的每个元素上, 并吧结果作为新的Iterator返回, 需要容器才能将返回的Iterator显示出来  例如:
list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))
['1', '2', '3', '4', '5', '6', '7', '8', '9']
    
4.
reduce()      from functools import reduce
再看reduce的用法。reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算，其效果就是：
reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)

map() 和 reduce()  ##################################
001(精简算法)
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def char2num(s):
    return DIGITS[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))
002(实际流程)
*****************************************************************
>>> from functools import reduce
>>> def fn(x, y):
...     return x * 10 + y
...
>>> def char2num(s):
...     digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
...     return digits[s]
...
>>> reduce(fn, map(char2num, '13579'))
13579
0000000000000000000
5.
filter()  用于过滤序列
filter() 和 map() 相似, 也是吧传入的函数依次作用于序列的每一个元素, 不同的是 filter() 是根据返回值的 bool 来确定是保留还是丢弃该元素
def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n
def _not_divisiable(n):
    return lambda x: x % n > 0
def primes():
    yield 2
    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisiable(n), it)
for n in primes():
    if n < 20:
        print(n)
    else:
        break
```





```css
list:
	insert: 插入元素, 插入到指定索引的为位置
	
tuple : 
		中的每个元素是不可的  但是 如果里面有列表  列表中的元素是可任意变			得, 但是元组中的还是列表这个元素,列表内部发变换相对元组是元素来说			是没有发生改变的, 所以说tuple 并没有发生改变  
```

#### dict.get()

```css
get 当字典中没有所要查找的元素时,返回的是None 
	也可以自己设置返回值   dict.get(key, setting)

要删除一个key，用pop(key)方法，对应的value也会从dict中删除
```

#### set

```css
相当于以个只有key 的字典
通过add(key)方法可以添加元素到set中
通过remove(key)方法可以删除元素
```

#### 函数

```css
函数可以同时返回多个值，但其实就是一个tuple。
默认参数选择不可变的对象, 尽量不可选择列表
def add_end(L=[]):
    L.append('END')
    return L
>>> add_end()
['END', 'END']
>>> add_end()
['END', 'END', 'END']   每次调用都会改变默认参数的值

参数: 
	*args   可变参数
	**kw    关键字参数
	*, a, b ...   命名关键字参数   必传参数, 格式  a='', b=''

函数的调用是通过 stack 栈 的数据结构实现的

尾递归优化
def fact(n):
    return fact_iter(n, 1)

def fact_iter(num, producter):
    if num == 1:
        return producter    # 最后返回的是此值
    return fact_iter(num - 1, num * producter)
```

#### 迭代(Iteration)

```python
如果给定一个list或tuple，我们可以通过for循环来遍历这个list或tuple，这种遍历我们称为迭代（Iteration）。

#字典的迭代
因为dict的存储不是按照list的方式顺序排列，所以，迭代出的结果顺序很可能不一样。
默认情况下，dict迭代的是key。如果要迭代value，可以用for value in d.values()，如果要同时迭代key和value，可以用for k, v in d.items()


```

#### 列表生成式(List Comprehensions)

```python
可以直接创建一个列表, 由于内存的限制, 但是容量是有限的

>>> [x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]

>>> import os # 导入os模块，模块的概念后面讲到
>>> [d for d in os.listdir('.')] # os.listdir可以列出文件和目录
['.emacs.d', '.ssh', '.Trash', 'Adlm', 'Applications', 'Desktop', 'Documents', 'Downloads', 'Library', 'Movies', 'Music', 'Pictures', 'Public', 'VirtualBox VMs', 'Workspace', 'XCode']
```

#### 生成器(generator)

```python
如果列表中的元素可以通过某种算法推算出来, 我们可可以在不断的循环中推算出需要的元素, 这种一边循环一边计算的机制,称为生成器   generator

>>> L = [x * x for x in range(10)]
>>> L
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> g = (x * x for x in range(10))
>>> g
<generator object <genexpr> at 0x1022ef630>

next(g) # 可以依次得到 generator g 的下一个元素
也可以用  for in 循环进行遍历 整个 generator
generator保存的是算法，每次调用next(g)，就计算出g的下一个元素的值，直到计算到最后一个元素，没有更多的元素时，抛出StopIteration的错误。

yield
函数是顺序执行，遇到return语句或者最后一行函数语句就返回。而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行。
  
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)
    
>>> o = odd()
>>> next(o)
step 1
1
>>> next(o)
step 2
3
>>> next(o)
step 3
5
>>> next(o)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
    

```

#### 迭代器(Iterator)

```python
可以直接作用于for循环的数据类型有以下几种：  ##都是可迭代对象,但是不是迭代器

一类是集合数据类型，如list、tuple、dict、set、str等；

一类是generator，包括生成器和带yield的generator function。

这些可以直接作用于for循环的对象统称为可迭代对象：Iterable。

# 可任意用iter() 将可迭代对象转化为迭代器

为什么list、dict、str等数据类型不是Iterator？
这是因为Python的Iterator对象表示的是一个数据流，Iterator对象可以被next()函数调用并不断返回下一个数据，直到没有数据时抛出StopIteration错误。可以把这个数据流看做是一个有序序列，但我们却不能提前知道序列的长度，只能不断通过next()函数实现按需计算下一个数据，所以Iterator的计算是惰性的，只有在需要返回下一个数据时它才会计算。


##小结
凡是可作用于for循环的对象都是Iterable类型；

凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；

集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。

Python的for循环本质上就是通过不断调用next()函数实现的
```

#### 返回函数(闭包)

```python
返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。

注意到返回的函数在其定义内部引用了局部变量args，所以，当一个函数返回了一个函数后，其内部的局部变量还被新函数引用，所以，闭包用起来简单，实现起来可不容易。

另一个需要注意的问题是，返回的函数并没有立刻执行，而是直到调用了f()才执行。我们来看一个例子：

def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()
在上面的例子中，每次循环，都创建了一个新的函数，然后，把创建的3个函数都返回了。

你可能认为调用f1()，f2()和f3()结果应该是1，4，9，但实际结果是：

>>> f1()
9
>>> f2()
9
>>> f3()
9

全部都是9！原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。

如果一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变：

def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs

```

#### 匿名函数

```python
a = map(lambda x: x * x, [1, 2, 3, 4, 5, 6])
print(list(a))
```

#### 装饰器(Decorator)

```python
现在，假设我们要增强now()函数的功能，比如，在函数调用前后自动打印日志，但又不希望修改now()函数的定义，这种在代码运行期间动态增加功能的方式，称之为“装饰器”（Decorator）。
本质上，decorator就是一个返回函数的高阶函数。所以，我们要定义一个能打印日志的decorator，可以定义如下：

def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

观察上面的log，因为它是一个decorator，所以接受一个函数作为参数，并返回一个函数。我们要借助Python的@语法，把decorator置于函数的定义处：

@log
def now():
    print('2015-3-25')

调用now()函数，不仅会运行now()函数本身，还会在运行now()函数前打印一行日志：

>>> now()
call now():
2015-3-25

把@log放到now()函数的定义处，相当于执行了语句：

now = log(now)
由于log()是一个decorator，返回一个函数，所以，原来的now()函数仍然存在，只是现在同名的now变量指向了新的函数，于是调用now()将执行新函数，即在log()函数中返回的wrapper()函数。

wrapper()函数的参数定义是(*args, **kw)，因此，wrapper()函数可以接受任意参数的调用。在wrapper()函数内，首先打印日志，再紧接着调用原始函数。

如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本：

def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

这个3层嵌套的decorator用法如下：

@log('execute')
def now():
    print('2015-3-25')

执行结果如下：

>>> now()
execute now():
2015-3-25
和两层嵌套的decorator相比，3层嵌套的效果是这样的：

>>> now = log('execute')(now)
我们来剖析上面的语句，首先执行log('execute')，返回的是decorator函数，再调用返回的函数，参数是now函数，返回值最终是wrapper函数。

以上两种decorator的定义都没有问题，但还差最后一步。因为我们讲了函数也是对象，它有__name__等属性，但你去看经过decorator装饰之后的函数，它们的__name__已经从原来的'now'变成了'wrapper'：

>>> now.__name__
'wrapper'

因为返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。

不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事的，所以，一个完整的decorator的写法如下：

import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

或者针对带参数的decorator：

import functools

def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

import functools是导入functools模块。模块的概念稍候讲解。现在，只需记住在定义wrapper()的前面加上@functools.wraps(func)即可。
```

#### 偏函数(Partial)

```python
functools.partial就是帮助我们创建一个偏函数的，不需要我们自己定义int2()，可以直接使用下面的代码创建一个新的函数int2：

>>> import functools
>>> int2 = functools.partial(int, base=2)
>>> int2('1000000')
64
>>> int2('1010101')
85

所以，简单总结functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。
**********************************************
max2 = functools.partial(max, 10)  #  创建一个比10 小返回10 比10大返回最大值的函数

实际上会把10作为*args的一部分自动加到左边，也就是：

max2(5, 6, 7)

相当于：

args = (10, 5, 6, 7)
max(*args)
```

## `2.2`面向对象

```python
class Student(object):

    def __init__(self, name):
        self.name = name
    
     def __str__(self):   # 在调用创建的对象时避免产生一个 object 而设置的返回一个字符串的作用
         return 'sad'
     __repr__ = __str__


a = Student('abc')    
print(a)


#   __getattr__
现在很多网站都搞REST API，比如新浪微博、豆瓣啥的，调用API的URL类似：

http://api.server/user/friends
http://api.server/user/timeline/list
如果要写SDK，给每个URL对应的API都写一个方法，那得累死，而且，API一旦改动，SDK也要改。

利用完全动态的__getattr__，我们可以写出一个链式调用：

class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__
试试：

>>> Chain().status.user.timeline.list
'/status/user/timeline/list'
这样，无论API怎么变，SDK都可以根据URL实现完全动态的调用，而且，不随API的增加而改变！

还有些REST API会把参数放到URL中，比如GitHub的API：

GET /users/:user/repos
调用时，需要把:user替换为实际用户名。如果我们能写出这样的链式调用：

Chain().users('michael').repos
就可以非常方便地调用API了。有兴趣的童鞋可以试试写出来。


### __call__()
任何类，只需要定义一个__call__()方法，就可以直接对实例进行调用。请看示例：

class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)
调用方式如下：

>>> s = Student('Michael')
>>> s() # self参数不要传入
My name is Michael.
__call__()还可以定义参数。对实例进行直接调用就好比对一个函数进行调用一样，所以你完全可以把对象看成函数，把函数看成对象，因为这两者之间本来就没啥根本的区别。
```

### 元类

```python
class Field(object):
    
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type
        
    def __str__(self):
        return '<%s : %s>' % (self.__class__.__name__, self.name)
    
    
class StringField(Field):
    
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')
        
        
class InterField(Field):
    
    def __init__(self, name):
        super(InterField, self).__init__(name, 'bigint')
        
        
class ModelMetaclass(type):
    
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mapping = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping : %s --> %s' % (k, v))
                mapping[k] = v
        for k in mapping.keys():
            attrs.pop(k)
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)


class Model(object, metaclass=ModelMetaclass):
    
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)
        
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model'object has no attribute : %s" % key)
        
    def __setattr__(self, key, value):
        self[key] = value
        
    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mapping__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = r'insert into %s (%s) values(%s)' % (self.__table__, ','.join(fields), ','join.(params))
        print("SQL: %s" % sql)
        print("ARGS: %s" % str(args))
            
    
```

## `2.3`IO 文件编程

### 文件读写

```python
f = open('file_path', 'r')  # 读写模式  r w r+ w+ a rb wb rb+ wb+
操作完成后必须调用 f.close()  来关闭文件 释放内存

with open('file_path', 'r') as f:
    content = f.read()
操作万之后文件会自动 关闭


```

### StringIO和BytesIO

```python
StringIO :  在内存中读写 str
    from io import StringIO
    f = StringIO
>>> f.write('hello')   # 返回值是字符串的长度
5
>>> f.write(' ')
1
>>> f.write('world!')
6
>>> print(f.getvalue())
hello world!


BytesIO : 在内存中读写bytes  二进制数据
    >>> from io import BytesIO
>>> f = BytesIO()
>>> f.write('中文'.encode('utf-8'))
6
>>> print(f.getvalue())    ## 写入的不是str 而是经过UTF-8编写的 bytes
b'\xe4\xb8\xad\xe6\x96\x87'


```

### 操作文件和目录

```python
Pyhton 内置的 os 模块也可以直接调用操作系统提供的借口函数
>>> import os
>>> os.name # 操作系统类型
'posix'
os.environ  #查看环境变量   得到的是一个字典
要获取某个环境变量的值，可以调用os.environ.get('key')：

# 查看当前目录的绝对路径:
>>> os.path.abspath('.')
'/Users/michael'
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
>>> os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
# 然后创建一个目录:
>>> os.mkdir('/Users/michael/testdir')
# 删掉一个目录:
>>> os.rmdir('/Users/michael/testdir')

把两个路径合成一个时，不要直接拼字符串，而要通过os.path.join()函数，这样可以正确处理不同操作系统的路径分隔符。

同样的道理，要拆分路径时，也不要直接去拆字符串，而要通过os.path.split()函数，这样可以把一个路径拆分为两部分，后一部分总是最后级别的目录或文件名：

>>> os.path.split('/Users/michael/testdir/file.txt')
('/Users/michael/testdir', 'file.txt')

os.path.splitext()可以直接让你得到文件扩展名，很多时候非常方便：

>>> os.path.splitext('/path/to/file.txt')
('/path/to/file', '.txt')

最后看看如何利用Python的特性来过滤文件。比如我们要列出当前目录下的所有目录，只需要一行代码：
>>> [x for x in os.listdir('.') if os.path.isdir(x)]
['.lein', '.local', '.m2', '.npm', '.ssh', '.Trash', '.vim', 'Applications', 'Desktop', ...]

要列出所有的.py文件，也只需一行代码：
>>> [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
['apis.py', 'config.py', 'models.py', 'pymonitor.py', 'test_db.py', 'urls.py', 'wsgiapp.py']

```

### 序列化 pickling

```python
d = dict(name='Bob', age=20, score=88)

可以随时修改变量，比如把name改成'Bill'，但是一旦程序结束，变量所占用的内存就被操作系统全部回收。如果没有把修改后的'Bill'存储到磁盘上，下次重新运行程序，变量又被初始化为'Bob'。

我们把变量从内存中变成可存储或传输的过程称之为序列化，在Python中叫pickling，在其他语言中也被称之为serialization，marshalling，flattening等等，都是一个意思。

反过来，把变量内容从序列化的对象重新读到内存里称之为反序列化，即unpickling。
```



## `2.4`进程和线程

------

### 多进程

* Unix /Linux 系统提供了一个fork() 系统调用,它非常特殊, fork() 调用,每次会自动把当前进程复制一份,然后分别放在父进程和子进程中返回
* 子进程返回的是 0 而父进程返回的是子进程的ID, 这样就可以一个父进程fork出多个子进程, 父进程要记下每个子进程是ID,而子进程只需要调用getppid()就可以拿到父进程的ID
* Python中的os模块就封装了常见的系统调用, 包含fork
* multiprocessing 模块下的Process类 代表一个进程对象

```python
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
```

* Pool 如果要创建大量的子进程.可以用进程池的方式批量创建

```python
from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
```

* 进程间通信

  `Process`之间肯定是需要通信的，操作系统提供了很多机制来实现进程间的通信。Python的`multiprocessing`模块包装了底层的机制，提供了`Queue`、`Pipes`等多种方式来交换数据。

  我们以`Queue`为例，在父进程中创建两个子进程，一个往`Queue`里写数据，一个从`Queue`里读数据：

```python
from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()
```

### 多线程

* 引用threading 模块 中的Thread
* 在多线程进行时,要注意在多个线程同时操作修改同一个数据时(全局变量),应该加线程锁来确保数据的安全性

```python
from time import sleep
from threading import Thread


balance = 0
def change_it(n):
    global balance
    balance += n
    balance -= n
    sleep(0.00001)

def run_thread(n):
    for i in range(10000):
        threading.lock.acquir()
        try:
            change_it(n)
        finally:  ## 确保锁一定能够被释放
            threading.lock.realese()

t1 = Thread(target=run_thread, args=(5,))
t2 = Thread(target=run_thread, args=(6,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)

```

* threading.local()   将要用到的全局变量绑定在其上, 式每个分支的线程都有一个可以直接用threading.local()调用的副本

```python
import threading

# 创建全局ThreadLocal对象:
local_school = threading.local()

def process_student():
    # 获取当前线程关联的student:
    std = local_school.student
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    # 绑定ThreadLocal的student:
    local_school.student = name
    process_student()

t1 = threading.Thread(target= process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target= process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
```

### 分布式进程

* 在 Thread和Process中应该优先选 Process 因为它更加稳定,而且 Process可以分布到多台机器上,  而 Thread 只能分布在一台机器的多个cpu上
* multiprocessing 模块支持多进程 其中mangers子模块 支持吧子模块分布在多个机器上
* liaoxuefeng-blog

```

```



## `2.5`正则表达式

* match()   匹配成功返回一个match对象 否则 返回None

```python
import re

string = '010-23123123'
pattern = re.compile(r'^\d{3}-\d{3,8}$')
result = pattern.findall(string)


result = re.findall(r'^\d{3}-\d{3,8}$', string)
print(result)
```



## `2.6`常用的内建模块

### `datetime`

* 时间戳的转换

```python
from datetime import datetime
time = datetime.now()
# time = datetime(2013, 2, 13, 12, 23, 33)

time_stamp = time.timestamp()  #转为时间戳
a = datetime.fromtimestamp(time_stamp)  # 还原
print(a)
```

### `collections`

* `namedtuple ` 创建一个元组,可以用属性而不是索引来引用tuple的元素

```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
temp = p
print(temp)
# namedtuple('名称', [属性list]):
Circle = namedtuple('Circle', ['x', 'y', 'r'])
```

* deque 创建一个可以双向添加和删除的列表

```python
>>> from collections import deque
>>> q = deque(['a', 'b', 'c'])
>>> q.append('x')
>>> q.appendleft('y')   #  popleft()   appendledt()
>>> q
deque(['y', 'a', 'b', 'c', 'x'])
```

* defaultdict()   创建一个字典,在查找出错时抛出指定的 default 可以写函数名来调用函数

```python
from collections import defaultdict
def test():
    return 'sdfsdf'
dd = defaultdict(test)
print(dd['key1'])

>>> from collections import defaultdict
>>> dd = defaultdict(lambda: 'N/A')
>>> dd['key1'] = 'abc'
>>> dd['key1'] # key1存在
'abc'
>>> dd['key2'] # key2不存在，返回默认值
'N/A'

```

* `orderedDict `产生有序的`dict `

```python
如果要保持Key的顺序，可以用OrderedDict：

>>> from collections import OrderedDict
>>> d = dict([('a', 1), ('b', 2), ('c', 3)])
>>> d # dict的Key是无序的
{'a': 1, 'c': 3, 'b': 2}
>>> od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
>>> od # OrderedDict的Key是有序的
OrderedDict([('a', 1), ('b', 2), ('c', 3)])

注意，OrderedDict的Key会按照插入的顺序排列，不是Key本身排序：

>>> od = OrderedDict()
>>> od['z'] = 1
>>> od['y'] = 2
>>> od['x'] = 3
>>> list(od.keys()) # 按照插入的Key的顺序返回
['z', 'y', 'x']

OrderedDict可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key：
```

* counter  简单的计数器 统计字符出现的个数

```python
from collections import Counter
c = Counter()
for ch in 'programmer':
    c[ch] += 1

print(c)
```

### `struct`

* `struct`的`pack`函数把任意数据类型变成`bytes` 

```python
>>> import struct
>>> struct.pack('>I', 10240099)
b'\x00\x9c@c'
pack的第一个参数是处理指令，'>I'的意思是：
>表示字节顺序是big-endian，也就是网络序，I表示4字节无符号整数。
后面的参数个数要和处理指令一致。

unpack把bytes变成相应的数据类型：
>>> struct.unpack('>IH', b'\xf0\xf0\xf0\xf0\x80\x80')
(4042322160, 32896)
根据>IH的说明，后面的bytes依次变为I：4字节无符号整数和H：2字节无符号整数。
所以，尽管Python不适合编写底层操作字节流的代码，但在对性能要求不高的地方，利用struct就方便多了
```

### `base 64`

```python
Base64是一种用64个字符来表示任意二进制数据的方法。
a-zA-Z0-9 + /  64个字符
Python内置的base64可以直接进行base64的编解码：

>>> import base64
>>> base64.b64encode(b'binary\x00string')
b'YmluYXJ5AHN0cmluZw=='
>>> base64.b64decode(b'YmluYXJ5AHN0cmluZw==')
b'binary\x00string'

如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节怎么办？Base64用\x00字节在末尾补足后，再在编码的末尾加上1个或2个=号，表示补了多少字节，解码的时候，会自动去掉。
由于=字符也可能出现在Base64编码中，但=用在URL、Cookie里面会造成歧义，所以，很多Base64编码后会把=去掉：
# 标准Base64:
'abcd' -> 'YWJjZA=='
# 自动去掉=:
'abcd' -> 'YWJjZA'
去掉=后怎么解码呢？因为Base64是把3个字节变为4个字节，所以，Base64编码的长度永远是4的倍数，因此，需要加上=把Base64字符串的长度变为4的倍数，就可以正常解码了。

```

### `hashlib`

* 摘要算法  对文本进行类似 指纹化 加密
* `MD5`是最常见的摘要算法，速度很快，生成结果是固定的128 bit字节，通常用一个32位的16进制字符串表示。

```python
import hashlib

md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
计算结果如下：

d26a53750bc40b38b65a520292f69306
```

* 另一种常见的摘要算法是`SHA1`，调用`SHA1`和调用`MD5`完全类似：`SHA1`的结果是160 bit字节，通常用一个40位的16进制字符串表示。

* ```python
  import hashlib

  sha1 = hashlib.sha1()
  sha1.update('how to use sha1 in '.encode('utf-8'))
  sha1.update('python hashlib?'.encode('utf-8'))
  print(sha1.hexdigest())
  ```

### `hmac`

* 通过哈希算法，我们可以验证一段数据是否有效，方法就是对比该数据的哈希值，例如，判断用户口令是否正确，我们用保存在数据库中的`password_md5`对比计算`md5(password)`的结果，如果一致，用户输入的口令就是正确的。

  为了防止黑客通过彩虹表根据哈希值反推原始口令，在计算哈希的时候，不能仅针对原始输入计算，需要增加一个salt来使得相同的输入也能得到不同的哈希，这样，大大增加了黑客破解的难度。

  如果`salt`是我们自己随机生成的，通常我们计算`MD5`时采用`md5(message + salt)`。但实际上，把salt看做一个“口令”，加salt的哈希就是：计算一段message的哈希时，根据不通口令计算出不同的哈希。要验证哈希值，必须同时提供正确的口令。

  这实际上就是`Hmac`算法：`Keyed-Hashing for Message Authentication`。它通过一个标准算法，在计算哈希的过程中，把key混入计算过程中。

  和我们自定义的加salt算法不同，`Hmac`算法针对所有哈希算法都通用，无论是`MD5`还是`SHA-1`。采用`Hmac`替代我们自己的`salt`算法，可以使程序算法更标准化，也更安全。

```python
>>> import hmac
>>> message = b'Hello, world!'
>>> key = b'secret'
>>> h = hmac.new(key, message, digestmod='MD5')
>>> # 如果消息很长，可以多次调用h.update(msg)
>>> h.hexdigest()
'fa4ee7d173f2d97ee79022d1a7355bcf'
```

* 可见使用`hmac`和普通hash算法非常类似。`hmac`输出的长度和原始哈希算法的长度一致。需要注意传入的`key`和`message`都是``bytes``类型，`str`类型需要首先编码为`bytes`。

### `itertools`

* `itertools`提供了非常有用的用于操作迭代对象的函数

```python
>>> import itertools
>>> natuals = itertools.count(1)
>>> for n in natuals:
...     print(n)
因为count()会创建一个无限的迭代器，所以上述代码会打印出自然数序列

cycle()会把传入的一个序列无限重复下去：
>>> import itertools
>>> cs = itertools.cycle('ABC') # 注意字符串也是序列的一种
>>> for c in cs:
...     print(c)

repeat()负责把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数：

>>> ns = itertools.repeat('A', 3)
>>> for n in ns:
...     print(n)

chain()可以把一组迭代对象串联起来，形成一个更大的迭代器：

>>> for c in itertools.chain('ABC', 'XYZ'):
...     print(c)

groupby()把迭代器中相邻的重复元素挑出来放在一起：

>>> for key, group in itertools.groupby('AAABBBCCAAA'):
...     print(key, list(group))
...
A ['A', 'A', 'A']
B ['B', 'B', 'B']
C ['C', 'C']
A ['A', 'A', 'A']
实际上挑选规则是通过函数完成的，只要作用于函数的两个元素返回的值相等，这两个元素就被认为是在一组的，而函数返回值作为组的key。如果我们要忽略大小写分组，就可以让元素'A'和'a'都返回相同的key：

>>> for key, group in itertools.groupby('AaaBBbcCAAa', lambda c: c.upper()):
...     print(key, list(group))
```

### `contextlib`

```python
class Query(object):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print('begin')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            print('End')

    def query(self):
        print('Query info abiut %s' % self.name)

# with Query('bob') as q:
#     q.query()
from contextlib import contextmanager


class Query(object):

    def __init__(self, name):
        self.name = name

    def query(self):
        print('query info about %s' % self.name)
@contextmanager
def create_query(name):
    print('begin')
    q = Query(name)
    yield q
    print('End')

with create_query('pop') as p:
    p.query()

with create_query('pop') as p:
    p.query()

@contextmanager
def tag(name):
    print('<%s>' %name)
    yield
    print('<%s>' % name)

with tag('h1'):
    print('hello')
    print('world')
    print('world')

from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('https://www.python.org')) as page:
    for line in page:
        print(line)
```

### `urllib`

```python
from urllib import request


with request.urlopen('https://api.douban.com/v2/book/2129650') as f:
    data = f.read()
    print('**************************' * 3)
    print(f.getheaders())
    print('**************************' * 3)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('data:', data.decode('utf-8'))

# 模拟浏览器发送GET 请求
from urllib import request

req = request.Request('http://www.douban.com/')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')

with request.urlopen(req) as f:
    print('status', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))
```

**Post**

```

```



**Handler**

```

```

### `xml`

* ML虽然比JSON复杂，在Web中应用也不如以前多了，不过仍有很多地方在用，所以，有必要了解如何操作XML。

* **DOM** vs **SAX**

  操作XML有两种方法：DOM和SAX。DOM会把整个XML读入内存，解析为树，因此占用内存大，解析慢，优点是可以任意遍历树的节点。SAX是流模式，边读边解析，占用内存小，解析快，缺点是我们需要自己处理事件。

  正常情况下，优先考虑SAX，因为DOM实在太占内存。

  在Python中使用SAX解析XML非常简洁，通常我们关心的事件是`start_element`，`end_element`和`char_data`，准备好这3个函数，然后就可以解析`xml`了。

### `HTMLParser`

```python
如果我们要编写一个搜索引擎，第一步是用爬虫把目标网站的页面抓下来，第二步就是解析该HTML页面，看看里面的内容到底是新闻、图片还是视频。

假设第一步已经完成了，第二步应该如何解析HTML呢？

HTML本质上是XML的子集，但是HTML的语法没有XML那么严格，所以不能用标准的DOM或SAX来解析HTML。

好在Python提供了HTMLParser来非常方便地解析HTML，只需简单几行代码：

from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)

parser = MyHTMLParser()
parser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>''')
feed()方法可以多次调用，也就是不一定一次把整个HTML字符串都塞进去，可以一部分一部分塞进去。

特殊字符有两种，一种是英文表示的&nbsp;，一种是数字表示的&#1234;，这两种字符都可以通过Parser解析出来。
```

## 3. 常见的第三方模块

### `Pillow`

* 图像处理标准库

### `requests`

* 访问网络资源
* data = `erquests.get('url')`
* `post()    put()   delete()`

### `chardet`

* 检测编码
* 使用原因:
  * 虽然Python提供了Unicode表示的`str`和`bytes`两种数据类型，并且可以通过`encode()`和`decode()`方法转换，但是，在不知道编码的情况下，对`bytes`做`decode()`不好做。

```python
>>> chardet.detect(b'Hello, world!')
{'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
测出的编码是ascii，注意到还有个confidence字段，表示检测的概率是1.0（即100%）。

>>> data = '离离原上草，一岁一枯荣'.encode('utf-8')
>>> chardet.detect(data)
{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
```



### `psutil`

* 运维脚本常用模块
  * 在Python中获取系统信息的另一个好办法是使用`psutil`这个第三方模块。顾名思义，`psutil = process and system utilities`，它不仅可以通过一两行代码实现系统监控，还可以跨平台使用，支持`Linux／UNIX／OSX／Windows`等，是系统管理员和运维小伙伴不可或缺的必备模块。
* 获取`cpu `, 内存,  磁盘,  进程,  网络等的信息 信息

### `virtualenv`

* ​

### `图形界面`

* ​

### `heapq`

* 建立堆这种数据结构

```python
heapq = [] #创建一个空堆
heappush (heap, item) #插入一条新值
item = heappop(heap) # 弹出最小值
item = 

```



* * ​

### `sys`

* `sys.argv` 接受命令参数

### `heapq`

## `sys`

* 命令行参数  在输入命令是给的参数 
* `sys.argv`  接受所有的参数  保存在数组中

### `yield` 

```python
# 生成式   列表已存在,占用空间大
list1 = [x for x in range(10)]

#生成器    得到的是 generator  对象 引用 
list3 = (x for c in range(10))
for i in list3:   # 在需要用的时候再计算出值
    print(i)
   
# 生成器函数
def fibo(n):  #普通函数 
    a, b = (0, 1)
    for _ in range(n):
        a, b = b, a + b
    return a

def fibo(n):  #生成器函数   保留上次计算的值 不会重复计算 
    a, b = (0, 1)
    for _ in range(n):
        a, b = b, a + b
    	yield 

```



### `splitlines()`

- `str.splitlines([keepends])`  keepends 为是否保留换行符  \r\n, 默认为False  不包含换行符 , True 则保留换行符
- 返回一个包含各行元素的列表

### 字符串前的`b`

```Python
a = b'你好'
print(a)    # 只能是ASCII中的字符才能用b 编码  
SyntaxError: bytes can only contain ASCII literal characters.
  
# 在只有 ASCII码表中的字符的情况下可以直接用 b'str' 将字符串装换为 bytes类型,超出  ASCII表中的字符时应该使用 encode 编码   
a = b'hello' #等价于  'hello'.encode('utf-8')
print(a)
```

### `divmod()`

- 函数吧除数和玉树运算结合起来,返回一个包含商和余数 的元组
- `divmod(a, b)  `返回元组 `(a //b , a % b)`

### `math.hypot()`

- 返回欧几里得范数 `sqrt(x ** x , y ** y)`
- 即返回的是向量的模