# 简单工厂模式

特点： 根据条件产生不同功能的类

程序实例： 四则运算计算器，根据用户的输入产生相应的运算类，用这个运算类处理具体的运算

```python
class Operation:
    def get_result(self):
        pass

class OperationAdd(Operation):
    def get_result(self):
        return self.op1+self.op2

class OperationSub(Operation):
    def get_result(self):
        return self.op1-self.op2

class OperationMul(Operation):
    def get_result(self):
        return self.op1*self.op2

class OperationDiv(Operation):
    def get_result(self):
        try:
            return self.op1/self.op2
        except:
            print 'divided by zero'
            return 0

class OperationUndef(Operation):
    def get_result(self):
        print 'undefined operation'
        return 0

class OperationFactory:
    operation={}
    operation['+']=OperationAdd();
    operation['-']=OperationSub();
    operation['*']=OperationMul();
    operation['/']=OperationDiv();
    def create_operation(self,ch)
        if ch in self.operation:
            op=self.operation[ch]
        else:
            op=OperationUndef
        return op
of=OperationFactory()
cal=of.create_operation('*')
cal.op1=10
cal.op2=20
print cal.get_result()

# 对象事先生产
#根据操作符选择对应对象
```

# 策略模式

特点： 定义算法家族并且分别进行封装，他们之间可以相互替换而不影响客户端

程序实例：商场收银软件，需要根据不同的销售策略方式进行收费

```python
class CashSuper():
    def accept_cash(self, money):
        return 0

class CashNormal(CashSuper):
    def accept_cash(self, money):
        return money

class  CashRebate(CashSuper):
    discount=0
    def __init__(self, discount):
        self.discount=discount
    def accept_cash(self, money):
        return money*self.discount

class CashReturn(CashSuper):
    total=0
    ret=0
    def __init__(self, total, ret):
        self.total=total
        self.ret=ret
    def accept_cash(self, money):
        if(money>=self.total):
            return money-self.ret
        return money

class CashContext:
    def __init__(self, csuper):
        self.cs=csuper

    def get_result(self, money):
        return self.accept_cash(money)

money = 100
strategy = {}
strategy[1] = CashContext(CashNormal())
strategy[2] = CashContext(CashRebate(0.8))
strategy[3] = CashContext(CashReturn(300,100))
ctype = input("type:[1]for normal,[2]for 80% discount [3]for 300 -100.")
if ctype in strategy:
    cc = strategy[ctype]
else:
    print "Undefine type.Use normal mode." cc = strategy[1]
print "you will pay:%d" %(cc.GetResult(money))

# 每一个策略都有相同的函数
```

# 装饰模式

模式特点： 动态地给对象增加额外的职责

程序实例：展示一个一件一件穿衣服的过程

```python
class Person:
    def __init__(self, tname):
        self.name = tname
    def show(self):
        print 'dressed %s'%self.name

class Finery(Person):
    component=None
    def __init__(self):
        pass

    def decorate(self, component):
        self.component = component

    def show(self):
        if(self.component!=None):
            self.component.show()

class Tshirt(Finery):
    def __init__(self):
        pass

    def show(self):
        print "big t-shirt"
        self.component.show()

class BigTrouser(Finery):
    def __init__(self):
        pass
    def show(self):
        print 'big trouser'
        self.component.show()

p=Person('somebody')
bt=BigTrouser()
ts=Tshirt()
bt.decorate(p)
ts.decorate(bt)
ts.show()

# 每个类都有同一个方法
```

# 代理模式

特点：为其他对象提供一种代理以控制对象的访问

```python
class Interface:
    def request(self):
        return 0

class RealSubject(Interface):
    def request(self):
        print 'real request'

class Proxy(Interface):
    def request(self):
        self.real=RealSubject()
        self.real.request()
p=Proxy()
p.request()
```

# 工厂方法模式

特点：定义一个用于创建对象的接口，让子类决定实例化哪一个类，这使得一个类的实例化延迟到其子类

```python
class Feng:
    def sweep(self):
        print "feng sweep"

class Student(Feng):
    def sweep(self):
        print 'student sweep'

class Volenter(Feng):
    def sweep(self):
        print 'volenter sweep'

class FengFactory:
    def create_feng(self):
        tmp=Feng()
        return tmp

class StudentFactory(FengFactory):
    def create_feng(self):
        tmp=Student()
        return tmp

class VolenterFactory(FengFactory):
    def create_feng(self):
        tmp=Volenter()
        return tmp

sf=StudentFactory()
s=sf.create_feng()
s.sweep()

sdf=VolenterFactory()
sd=sdf.create_feng()
sd.sweep()
```

# 原型模式

特点：用原型实例指定创建对象的种类，并且通过拷贝这些原型创建新的对象

程序实例：从简历原型，生成新的简历

代码特点：简历类Resume提供的clone方法其实并不是真正的clone，只是为已存在的对象增加一次引用。python中copy模块的copy方法和deepcopy方法已经实现了原型模式

```python
import copy
class WorkExp
    place=''
    year=0

class Resume:
    name=''
    age=0
    def __init__(self, name):
        self.name=name

    def set_age(self, age):
        self.age=age

    def set_work_exp(self, place, year):
        self.place=place
        self.year=year

    def display(self):
        print self.age
        print self.place
        print self.year

    def clone(self):
        return self#这里并不是克隆，而是返回自身
```

# 模板方法模式

特点： 定义一个操作中的算法骨架，将一些步骤延迟至子类中

程序实例：考试时使用同一份考卷，不同学生上交自己填写的考卷

```python
class TestPaper:
    def TestQuestion1(self):
        print "Test1:A. B. C. D."
        print "(%s)" %self.Answer1()

    def TestQuestion2(self):
        print "Test1:A. B. C. D."
        print "(%s)" %self.Answer2()
    def Answer1(self):
        return ""
    def Answer2(self):
        return ""

class TestPaperA(TestPaper):
    def Answer1(self):
        return "B"
    def Answer2(self):
        return "C";

class TestPaperB(TestPaper):
    def Answer1(self):
        return "D"
    def Answer2(self):
        return "D";

s1 = TestPaperA()
s2 = TestPaperB()
print "student 1" s1.TestQuestion1()
s1.TestQuestion2()
print "student 2" s2.TestQuestion1()
s2.TestQuestion2()
```

# 外观模式

特点：为一组调用提供一直的接口

程序实例：接口将几种调用组合成两组，用户通过接口调用其中的一组

```python
class SubSystemOne:
    def MethodOne(self):
        print "SubSysOne"

class SubSystemTwo:
    def MethodTwo(self):
        print "SubSysTwo"

class SubSystemThree:
    def MethodThree(self):
        print "SubSysThree"

class SubSystemFour:
    def MethodFour(self):
        print "SubSysFour"

class Facade:
    def __init__(self):
        self.one = SubSystemOne()
        self.two = SubSystemTwo()
        self.three = SubSystemThree()
        self.four = SubSystemFour()

    def MethodA(self):
        print "MethodA"
        self.one.MethodOne()
        self.two.MethodTwo()
        self.four.MethodFour()

    def MethodB(self):
        print "MethodB" self.two.MethodTwo()
        self.three.MethodThree()

facade = Facade()
facade.MethodA()
facade.MethodB()
```

# 建造者模式

特点：将一个复杂的对象的构建与他的表示分离，使得同样的构建过程可以创建不同的表示

程序实例： 画出一个四肢健全的小人

```python

class Person:
    def CreateHead(self):
        pass
    def CreateHand(self):
        pass
    def CreateBody(self):
        pass
    def CreateFoot(self):
        pass

class ThinPerson(Person):
    def CreateHead(self):
        print "thin head"
    def CreateHand(self):
        print "thin hand"
    def CreateBody(self):
        print "thin body"
    def CreateFoot(self):
        print "thin foot"

class ThickPerson(Person):
    def CreateHead(self):
        print "thick head"
    def CreateHand(self):
        print "thick hand"
    def CreateBody(self):
        print "thick body"
    def CreateFoot(self):
        print "thick foot"

class Director:
    def __init__(self,temp):
        self.p = temp
    def Create(self):
        self.p.CreateHead()
        self.p.CreateBody()
        self.p.CreateHand()
        self.p.CreateFoot()

p = ThickPerson()
d = Director(p)
d.Create()
```

# 观察者模式

模式特点：定义了一种一对多的关系，让多个观察对象同时监听一个主题对象，当主题对象状态发生变化时会通知所有观察者。

程序实例：公司里有两种上班时趁老板不在时偷懒的员工：看NBA的和看股票行情，并
且事先让老板秘书当老板出现时通知他们继续做手头上的工作。

```python
class Observer:
    def __init__(self,strname,strsub):
        self.name = strname
        self.sub = strsub
    def Update(self):
        pass

class StockObserver(Observer):
    def Update(self):
        print "%s:%s,stop watching Stock and go on work!" %(self.name,self.sub.action)

class NBAObserver(Observer):
    def Update(self):
        print "%s:%s,stop watching NBA and go on work!" %(self.name,self.sub.action)

class SecretaryBase:
    def __init__(self):
        self.observers = []
    def Attach(self,new_observer):
        pass
    def Notify(self):
        pass

class Secretary(SecretaryBase):
    def Attach(self,new_observer):
        self.observers.append(new_observer)
    def Notify(self):
        for p in self.observers:
            p.Update()

p = Secretary()
s1 = StockObserver("xh",p)
s2 = NBAObserver("wyt",p)
p.Attach(s1);
p.Attach(s2);
p.action = "WARNING:BOSS";
p.Notify()


```
