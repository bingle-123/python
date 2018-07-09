# Python Decorator 和函数式编程 

Decorators 是Python中最重要的特性之一. 它除了使Python更好用外的, 它还能帮助我们以一种更有趣的方法考虑问题--函数式编程的方法

我会尝试着从零开始解释Decorator是怎么工作的. 首先, 我们会介绍一些帮助你理解Decorator的概念. 然后, 我们会深入的去解释一些示例代码以及他们的工作原理. 最后, 我们会讨论一些更加高级的Decorator的用法, 诸如给他们传可选参数, 把他们组成一个执行链。 

首先, 让我们来用我所能想到的最简单的方法来定义Python中的方法(Function). 然后基于这个简单的定义，再用相同方法来定义Decorators.

方法(Function)是一段用以执行某一特定任务的可重用的代码.

那什么是Decorator呢？

Decorator是一个改变其他方法的方法.

现在，让我们通过几个先决条件来解释decorators的含义。

# 函数（Functions）是第一个对象

在Python中， 一切都是对象。这意味着即使一个函数被其他对象所包装，我们仍然可以通过这个对象名来进行调用。 举个列子：

```python
def traveling_function():
    print "Here I am!"

function_dict = {
    "func": traveling_function
}

trav_func = function_dict['func']
trav_func()
# >> Here I am!
```

`traveling_function`尽管在`function_dictdictionary`中被指定为func这个‘key’的‘value’， 但是我们仍然可以正常的使用。


# 在高阶函数中使用第一类函数 

我们可以以类似其它对象的方式传递对象。它可以是字典的值、列表的项或是另一个对象的属性。那么，我们不能将函数以参数的方式传递给另一个函数么？可以！函数作为参数传递给高阶函数。

```python
def self_absorbed_function():
    return "I'm an amazing function!"

def printer(func):
    print "The function passed to me says: " + func()

# Call `printer` and give it `self_absorbed_function` as an argument
printer(self_absorbed_function)
# >> The function passed to me says: I'm an amazing function!
```

上面就是将函数作为参数传递另一个函数，并进行处理的示例。用这种方式，我们可以创造很多有趣的函数，例如 decorator。

# Decorator 基础

从心而论，decorator 只是将函数作为参数的函数。通常，它的作用是返回封装好的经过修饰的函数。下面这个简单的身份识别 decorator 可以让我们了解 decorator 是如何工作的。
```python
def identity_decorator(func):
    def wrapper():
        func()
    return wrapper


def a_function():
    print "I'm a normal function."

# `decorated_function` is the function that `identity_decorator` returns, which
# is the nested function, `wrapper`
decorated_function = identity_decorator(a_function)

# This calls the function that `identity_decorator` returned
decorated_function()
# >> I'm a normal function
```

`在这里，identity_decoratordoes` 并没有修改其封装的函数。它仅仅是返回了这个函数，调用了作为参数传递给 `identity_decorator` 的函数。这个 decorator 毫无意义！

有趣的是在 identity_decorator 中，虽然函数没有传递给 wrapper ，它依然那可以被调用，这是因为闭包原理。

# 闭包

闭包是个花哨的术语，意思是当一个函数被声明，在其被声明的词法环境中，它都可以被引用。

上例中，当 wrapper 被定义时，它就访问了本地环境中的函数变量。一旦 `identity_decorator` 返回，你就只能通过 `decorated_function` 访问函数。在 `decorated_function` 的闭包环境之外，函数并非以变量形式存在的。

# 简单的 decorator

现在, 让我们来创建一个简单的,有点实际功能的Decorator. 这个Decorator所做的就是记录他所包装的方法被调用的次数。

```python
def logging_decorator(func):
    def wrapper():
        wrapper.count += 1
        print("The function I modify has been called {0} times(s).".format(wrapper.count))
        func()
    wrapper.count = 0
    return wrapper


def a_function():
    print("I'm a normal function.")

modified_function = logging_decorator(a_function)

modified_function()
# >> The function I modify has been called 1 time(s).
# >> I'm a normal function.

modified_function()
# >> The function I modify has been called 2 time(s).
# >> I'm a normal function.
```

# Decorator语法

在上一个例子中，我们看到一个Decorator可以接受一个方法作为参数，然后在该方法上再包装上其他方法。一旦你熟悉了装饰器(Decorator), Python还为你提供了一个特定的语法使得它看上去更直观，更简单。
```python
# In the previous example, we used our decorator function by passing the
# function we wanted to modify to it, and assigning the result to a variable

def some_function():
    print "I'm happiest when decorated."

# Here we will make the assigned variable the same name as the wrapped function
some_function = logging_decorator(some_function)
# We can achieve the exact same thing with this syntax:

@logging_decorator
def some_function():
    print "I'm happiest when decorated."

```
Decorator语法的简要工作原理:

当Python的解释器看到这个被装饰的方法时，先编译这个方法(`some_function`), 然后先给它赋一个名字 'some_function'.

这个方法(`some_function`)再被传入装饰方法(decorator function)`logging_decorator`中

装饰方法(decorator function)`logging_decorator`返回的新方法替代原来的`some_function`方法, 与`some_function`这个名字绑定.

记住这些步骤，再来仔细看一下`identity_decorator`方法和它注释.
```python
def identity_decorator(func):
    # Everything here happens when the decorator LOADS and is passed
    # the function as described in step 2 above
    def wrapper():
        # Things here happen each time the final wrapped function gets CALLED
        func()
    return wrapper
```

希望这里的注释能起到一定的引导作用. 只有在装饰器所返回的方法中的指令才会在每次调用的时候被执行. 在被返回函数外的指令只会被执行一次-- 在第二步 当装饰器第一次接受一个方法的时候。

在我们研究更有趣的装饰器之前， 我还有一件事情需要特别解释一下。

# *args和**kwargs

你也许以前会觉得这些东西让人困惑和烦恼。让我来一一为你讲解一下吧。

通过使用`*args`语法，一个python函数在它的参数列表中可以接受多个位置参数。 `*args` 将所有的非关键词参数组合到一个元组（tuple)里，这个元组可以在函数中访问得到。 反过来，当`*args`用在调用函数的参数列表时，它会将一个元组的参数展开成一系列的位置参数。
```python
# （译注：形式参数示例）
def function_with_many_arguments(*args):
    print args

# 此函数中的`args`将成为传递的所有参数的元组
# 可以在函数中像使用元组一样使用
function_with_many_arguments('hello', 123, True)
# >> ('hello', 123, True)
# （译注：实参示例）
def function_with_3_parameters(num, boolean, string):
    print "num is " + str(num)
    print "boolean is " + str(boolean)
    print "string is " + string

arg_list = [1, False, 'decorators']

# 通过使用'*'号 arg_list将会被展开为三个位置参数 
function_with_3_parameters(*arg_list)
# >> num is 1
# >> boolean is False
# >> string is decorators
```
重申：在形式参数列表中，`*arg`将放到一个名为args的元组中，在一个实参列表中，`*arg`将扩展成一系统位置参数然后应用到函数中。

正如你在实参示例所看到那样，'*'符号可以和'args'之外的的名字使用。它只是一个在收缩和扩展通用列表时的约定形式。

`**kwargs`跟他的兄弟`*args`相似，但是它是跟关键词参数相关而不是位置。如果`**kwargs`用在一个形式参数列表中，它将所有接收到的关键词参数收集进一个字典中。如果它用在一个函数的实参列表中。它将把一个字典扩展成一系统的关键词参数。
```python
def function_with_many_keyword_args(**kwargs):
    print kwargs

function_with_many_keyword_args(a='apples', b='bananas', c='cantalopes')
# >> {'a': 'apples', 'b': 'bananas', 'c': 'cantalopes'}  def multiply_name(count=0, name=''):
    print name * count

arg_dict = {'count': 3, 'name': 'Brian'}

multiply_name(**arg_dict)
# >> BrianBrianBrian 
```
现在你明白了为什么`*arg`和`**kwargs`有魔力了吧，让我们继续学习你会觉得很有用的装饰器吧。

# 代码记忆（Memoization)

代码记忆是一种避免潜在的重复计算开销的方法。你通过缓存一个函数每次运行的结果来达到此目的。 这样，下一次函数以同样的参数运行时，它将从缓存中返回结果，并不需要花费额外的时间来计算结果。
```python
from functools import wraps
def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def an_expensive_function(arg1, arg2, arg3)
```
你可能已经注意到代码示例中的一个奇怪的@wrapsdecorator.在我们稍后要讲解代码记忆之前，我将简要介绍下这个奇怪的@wrapsdecorator。

使用装饰器的一个副作用就是，装饰之后函数丢失了它本来的__name__,__doc__及__module__属性。 包装函数用作装饰器来包装装饰器返回的函数，如果被包装的函数没有被装饰，则将恢复他们所有的三个属性值。 例如：一个_expensive_function的名字（可以通过_expensive_function.__name__来查看）将被包装，即使我们没有使用装饰器。
我认为，代码记忆是一个很好的使用装饰器的示例。通过创建一个通用的装饰器，他为很多函数想要的功能服务， 我们可以将装饰器添加到任何想要利用这些功能的函数上。这避免了在不同的地方写同样的功能。 不重复自己（DRY)让我们的代码更易于维护，易于阅读和理解。 只要看到一个单词就可以马上知道函数有代码记忆。

我应该指出的是，代码记忆只适用于纯函数。因为这种函数保证了给定特定的同样的参数就会得出同样的结果。 如果一个函数它的结果取决于一个没有作为参数传递的全局变量，或者I/O，或者其它可能影响到结果值的东西， 代码记忆将产生令人困惑的结果！同样，纯函数没有任何副作用。因此，如果你的让一个计数器增加，或者在另一个对象中调用方法，或者任何不在函数得到的返回值上面的东西，如果结果是从缓存中返回的话，也不会什么副作用。

# 类装饰器

上面我们说到装饰器是修饰函数的函数。凡事总有个但是。我们还可以用它来修饰类或方法。虽然一般不会这么用它。但有些情况下用来替代元类也未尝不可呀。

```python
foo = ['important', 'foo', 'stuff']


def add_foo(klass):
    klass.foo = foo
    return klass


@add_foo
class Person(object):
    pass

brian = Person()

print brian.foo
# >> ['important', 'foo', 'stuff']

```
现在任何从 Person 实例出来的对象都会包含 foo 属性，注意到我们的装饰器函数没，它没有返回一个函数，而是一个类。所以赶紧更新一下刚才我们对装饰器的定义吧：装饰器是一个可以修饰函数，类或方法的函数。

# 作为一个类的装饰器

事实证明，我在之前隐瞒了其它的什么东西。 装饰器不仅仅可以装饰一个类，它可以作为一个类来使用。**一个装饰器的唯一需求是他的返回值可以被调用。 这意味着当你调用一个对象时它必须实现_call_这个魔幻般的在幕后调用的方法**。函数设置了这个隐式方法。让我们重新建立 identity_decorators 作为一个类，然后来看它是怎么运作的。这个例子到底发生了什么呢：
```python
class IdentityDecorator(object):
    def __init__(self, func):
        self.func = func

    def __call__(self):
        self.func()


@IdentityDecorator
def a_function():
    print "I'm a normal function."

a_function()
# >> I'm a normal function
```
- 当IdentityDecorator装饰器装饰了`a_function`,它表现仅仅是一个装饰器也是一个函数。这个片段相当于这个例子的装饰语法： `a_function = IdentityDecorator(a_function)`. 这个类装饰器被调用并实例化，然后把它作为参数传递给它所装饰的函数。

- 当IdentityDecorator实例化，它的初始化函 `_init_`与当做参数传递进来的装饰函数一起调用。 这种情况下，它所做的一切就是分派给这个函数一个属性，随后可以被其它方法访问。

- 最后,当`a_function`（真实的返回的IdentityDecorator对象包装了`a_function`）被调用，这个对象的 call 方法被引用进来，由于这仅仅是一个有标识的装饰器，它可以简单的调用它所装饰的函数。 

让我们再一次更新我们的装饰器！

装饰模式可以做为修改函数、方法或者类来被调用。 

# 带参数的装饰器

时你需要根据不同的情况改变装饰器的行为，这可以通过传递参数来完成。
```python
from functools import wraps

def argumentative_decorator(gift):
    def func_wrapper(func):
        @wraps(func)
        def returned_wrapper(*args, **kwargs):
            print "I don't like this " + gift + " you gave me!"
            return func(gift, *args, **kwargs)
        return returned_wrapper
    return func_wrapper


@argumentative_decorator("sweater")
def grateful_function(gift):
    print "I love the " + gift + "! Thank you!"

grateful_function()
# >> I don't like this sweater you gave me!
# >> I love the sweater! Thank you!
```

让我们看看如果我们不用装饰器语法，装饰器函数是怎么运作的：

```python
# If we tried to invoke without an argument:
grateful_function = argumentative_function(grateful_function)

# But when given an argument, the pattern changes to:
grateful_function = argumentative_decorator("sweater")(grateful_function)
```

主要的要关注的是当给定一些参数，装饰器会首先被引用并带有这些参数——就像平时包装过的函数并不在此列。 然后这个函数调用返回值， 装饰器已经包装的这个函数已经传递给初始化后的带参数的装饰器的返回函数。（这种情况下， 返回值是(`argumentative_decorator("swearter")`).

一步步来看：

- 解释器到达装饰过的函数, 编译grateful_function, 并把它绑定给'grateful_fucntion'这个名字.

- argumentativ_decorator被调用, 并传递参数“sweater”, 返回func_wrapper. 

- func_wrapper被调用, 并传入grateful_function作为参数, func_wrapper返回returned_wrapper.

- 最后， returned wrapper 被替代为原始的函数 grateful_function, 然后被绑定到grateful function这个名字下.

我认为当不使用装饰器参数的时候, 这一系列的事件有点难以追踪。请花点时间通盘考虑下，希望这对你会有点启发.

# 带可选参数的装饰器

有许多方法使用带可选参数的装饰器。这取决于你是要用一个位置参数还是关键字参数，或者两个都用。在使用上可能有一点点不同。下面就是其中的一种方法:
```python
from functools import wraps

GLOBAL_NAME = "Brian"


def print_name(function=None, name=GLOBAL_NAME):
    def actual_decorator(function):
        @wraps(function)
        def returned_func(*args, **kwargs):
            print "My name is " + name
            return function(*args, **kwargs)
        return returned_func

    if not function:  # User passed in a name argument
        def waiting_for_func(function):
            return actual_decorator(function)
        return waiting_for_func

    else:
        return actual_decorator(function)


@print_name
def a_function():
    print "I like that name!"


@print_name(name='Matt')
def another_function():
    print "Hey, that's new!"

a_function()
# >> My name is Brian
# >> I like that name!

another_function()
# >> My name is Matt
# >> Hey, that's new!

```
如果我们需要传name 到 `print_name`方法里面，他将会和之前的`argumentative_decoratorin`效果相同。也就是说，第一个`print_name`将会把name作为它的参数。函数在第一次请求时返回的值将会传递到函数里。

如果没有向`print_name`传name的参数，将会报缺少修饰的错。它将会像单参数函数一样发送请求。

`print_name `有这两种可能。他要检查收到的参数是不是一个被包装的函数。如果不是的话，返回`waiting_for_func` 函数来请求被包装的函数。如果收到的是一个函数参数，它将会跳过中间的步骤，立刻请求`actual_decorator`。

# 链式装饰器

今天让我们来探索下装饰器的最后一个特性吧：链式。你可以在任意给定的函数中放置多个装饰器。 它使用一种类似用多继承来构造类的方式来构造函数。但是最好不要过于追求这种方式。
```python
@print_name('Sam')
@logging_decorator
def some_function():
    print "I'm the wrapped function!"

some_function()
# >> My name is Sam
# >> The function I modify has been called 1 time(s).
# >> I'm the wrapped function!
```
当你将装饰器链接在一起时，他们在放置在栈中顺序是从下往上。 被包装的函数，`some_fuction`，编译之后，传递给在它之上的第一个装饰器（loging_decorator). 然后第一个装饰器的返回值传递给下一个。它将以这样的式传递给链中的每一个装饰器。

因为我们这里用到的装饰器都是打印一个值然后返回传递给它们的函数。这意味着在链中的最后一个装饰器，`print_name`，当被包装（装饰）的函数调用时，将打印整个输出的第一行。

# 总结

我认为decorator最大的好处之一是它能让你从高些的层次进行抽象。如果你开始读一个方法的定义，发现他有个 amemoize decorator，你会马上意识到你是在看memoized方法。如果memoization的代码是在方法内部，则可能要花些额外的心思去解析，且有可能误解。 使用decorator，也能实现代码重用，从而节省时间，简化调试，使得反射更容易。

使用decorator也是个很好的学习函数式编程概念的方式，如高级函数、闭包。



