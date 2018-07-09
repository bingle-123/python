# Getting Started
## Install 

`pip install cython`

## Building Cython code

cython代码必须被编译,分为两步:
1. 一个`.pyx`结尾的文件,cython把它编译为`.c`文件
2. `.c` 文件被gcc编译为`.so`文件,这样python可以直接`import`

有多重方法构建Cython代码:
- 使用distutils `setup.py`,推荐的方式
- 使用`pyximport` 像导入`.py`文件一样导入`.pyx`文件(他使用distutils编译并且是在后台执行)
- 使用`cython`命令行工具来手动从`.pyx`文件创建`.c`文件.然后手动编译`.c`文件到共享对象库(shared object library),这种方式通常用来debug
- 使用jupyter notebook或者Sage notebook,他们都允许行内Cython代码

### 使用distutils构建cython模块

```python
#hello.pyx
def say_hello_to(name):
    print("Hello %s!"%name)
```

```python
#setup.py
from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'Hello world app',
  ext_modules = cythonize("hello.pyx"),
)
```

`python setup.py build_ext --inplace`

`from hello import say_hello_to`

### 在jupyter中使用

```
%load_ext Cython

%%cython --annotate

cdef int a = 0
for i in range(10):
    a += i
print(a)
```

## 使用静态类型来加速代码

所有的C类型,cython都支持:integer, float,  structs, unions and pointer types...;

使用静态类型会导致代码可读性变差,如果python类型向C类型转换溢出时,会抛出python的OverflowError

```python
def f(x):
    return x**2-x

def integrate_f(a, b, N):
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += f(a+i*dx)
    return s * dx
```
这里的代码用Cython编译后速度提高接近35% 

但是如果使用静态类型,速度会提高更多,但是一定要选择恰当的类型

## 函数类型

python的函数调用损耗较大

```python
cdef double f(double x) except? -2:
    return x**2-x
```

`except? -2:`通常是需要的,否则如果函数内部调用其他函数时发生异常,或者函数自己跑出异常时,Cython不会传递这些异常.

`except? -2:`表示:如果函数返回了`-2`那么会检查发生错误;`?`表示`-2`可能是函数返回的有效值

`except * `是安全的但是低效

副作用是:函数在python空间不可见,而且运行时也不可更改`f()`

使用`cpdef`代替`cdef`,一个Python wrapper会自动创建,这样函数在cython和python中都可用;事实上`cpdef`不止提供了Python wrapper,它还使得该函数可一个python 方法覆盖.

可以提高150倍

## 什么地方添加类型

初次接触cython,可能导出使用静态类型.静态类型会导致可读性,扩展性,降低;

循环代码,容易性能瓶颈的点;使用profile和annotation来诊断,profile应该是第一步,他可以指出,时间耗费在哪里

cython annotation可以指出为什么代码耗时;`cython -a`

# 基础教程

Cython is Python with C data types;Almost any piece of Python code is also valid Cython code;

 
如果代码不需要任何的C库或者特殊的构建步骤,那么可以直接使用`pyximport`模块,他不需要每次都执行一遍`setup.py`

Cython编译python代码时人会有很多失败情况,那么可以使用`pyximport.install(pyimport = True)`当失败时就会加载python的源代码

# 调用C函数

使用`cimport`

```python
from libc.math cimport sin

cdef double f(double x):
    return sin(x*x)
```

## 动态链接

math库,在unix或者linux系统中默认是没有被链接的,所以Cython编译时需要指定链接库`m`

在setup中使用`Extension()`的`libraries`参数来指定

```python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules=[
    Extension("demo",
              sources=["demo.pyx"],
              libraries=["m"] # Unix-like specific
    )
]

setup(
  name = "Demos",
  ext_modules = cythonize(ext_modules)
)
```

### 外部声明

```python
cdef extern from "math.h":
    double sin(double x)
```

### 参数命名

C和Cython都可以支持签名声明,不需要提供参数名称

```python
cdef extern from "string.h":
    char* strstr(const char*, const char*)


cdef extern from "string.h":
    char* strstr(const char *haystack, const char *needle)

cdef char* data = "hfvcakdfagbcffvschvxcdfgccbcfhvgcsnfxjh"

pos = strstr(needle='akd', haystack=data)
print(pos)
```






