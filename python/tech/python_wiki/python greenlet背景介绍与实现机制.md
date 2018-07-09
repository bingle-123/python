# python greenlet背景介绍与实现机制

并发处理的技术背景

并行化处理目前很受重视， 因为在很多时候，并行计算能大大的提高系统吞吐量，尤其在现在多核多处理器的时代， 所以像lisp这种古老的语言又被人们重新拿了起来， 函数式编程也越来越流行。 介绍一个python的并行处理的一个库： greenlet。 python 有一个非常有名的库叫做 stackless ，用来做并发处理， 主要是弄了个叫做tasklet的微线程的东西， 而greenlet 跟stackless的最大区别是， 他很轻量级？不够， 最大的区别是greenlet需要你自己来处理线程切换， 就是说，你需要自己指定现在执行哪个greenlet再执行哪个greenlet。

# greenlet的实现机制

以前使用python开发web程序,一直使用的是fastcgi模式.然后每个进程中启动多个线程来进行请求处理.这里有一个问题就是需要保证每个请求响应时间都要特别短,不然只要多请求几次慢的就会让服务器拒绝服务,因为没有线程能够响应请求了.平时我们的服务上线都会进行性能测试的,所以正常情况没有太大问题.但是不可能所有场景都测试到.一旦出现就会让用户等好久没有响应.部分不可用导致全部不可用.后来转换到了coroutine,python 下的greenlet.所以对它的实现机制做了一个简单的了解.
每个greenlet都只是heap中的一个python object(PyGreenlet).所以对于一个进程你创建百万甚至千万个greenlet都没有问题.
```cpp
typedef struct _greenlet {
	PyObject_HEAD
	char* `stack_start`;
	char* `stack_stop`;
	char* `stack_copy`;
	intptr_t `stack_saved`;
	struct _greenlet* stack_prev;
	struct _greenlet* parent;
	PyObject* run_info;
	struct _frame* top_frame;
	int recursion_depth;
	PyObject* weakreflist;
	PyObject* exc_type;
	PyObject* exc_value;
	PyObject* exc_traceback;
	PyObject* dict;
} PyGreenlet;
```
每一个greenlet其实就是一个函数,以及保存这个函数执行时的上下文.对于函数来说上下文也就是其stack..同一个进程的所有的greenlets共用一个共同的操作系统分配的用户栈.所以同一时刻只能有栈数据不冲突的greenlet使用这个全局的栈.greenlet是通过`stack_stop`,`stack_start`来保存其stack的栈底和栈顶的,如果出现将要执行的greenlet的`stack_stop`和目前栈中的greenlet重叠的情况,就要把这些重叠的greenlet的栈中数据临时保存到heap中.保存的位置通过`stack_copy`和`stack_saved`来记录,以便恢复的时候从heap中拷贝回栈中`stack_stop`和`stack_start`的位置.不然就会出现其栈数据会被破坏的情况.所以应用程序创建的这些greenlet就是通过不断的拷贝数据到heap中或者从heap中拷贝到栈中来实现并发的.对于io型的应用程序使用coroutine真的非常舒服.
```
A PyGreenlet is a range of C stack addresses that must be
saved and restored in such a way that the full range of the
stack contains valid data when we switch to it.

Stack layout for a greenlet:

               |     ^^^       |
               |  older data   |
               |               |
  stack_stop . |_______________|
        .      |               |
        .      | greenlet data |
        .      |   in stack    |
        .    * |_______________| . .  _____________  stack_copy + stack_saved
        .      |               |     |             |
        .      |     data      |     |greenlet data|
        .      |   unrelated   |     |    saved    |
        .      |      to       |     |   in heap   |
 stack_start . |     this      | . . |_____________| stack_copy
               |   greenlet    |
               |               |
               |  newer data   |
               |     vvv       |
```
下面是一段简单的greenlet代码.
```python
from greenlet import greenlet

def test1():
    print 12
    gr2.switch()
    print 34

def test2():
    print 56
    gr1.switch()
    print 78

gr1 = greenlet(test1)
gr2 = greenlet(test2)
gr1.switch()
```
目前所讨论的协程，一般是编程语言提供支持的。协程不同于线程的地方在于协程不是操作系统进行切换，而是由程序员编码进行切换的，也就是说切换是由程序员控制的，这样就没有了线程所谓的安全问题。
所有的协程都共享整个进程的上下文，这样协程间的交换也非常方便。

相对于第二种方案（I/O多路复用），使得使用协程写的程序将更加的直观，而不是将一个完整的流程拆分成多个管理的事件处理。

协程的缺点可能是无法利用多核优势，不过，这个可以通过协程+进程的方式来解决。
