---

---

# 课堂笔记

## 匿名函数

```python
可以传递一个或者多个参数的 运算 将表达式传给一个变量 避免函数名称的冲突
a  = lambda x : x * 2
print(a(2))  # 可以得到  4
b = lambda x, y : x + y
print(b(1, 3)) # 4
```



### reduce()

```python
reduce   把一个函数作用在一个序列上, 这个函数必须接受两个参数, reduce 把结果和序列的写一个元素做累积计算
# 运用的是递归的思想  不同之处在于 它是将第一次调用函数的结果作为了第二次调用函数的第一个参数, 
reduce(f, [x1, x2, x3, x4, x5])  = f(f(f( f(x1, x2), x3),x4), x5)
```

###map()

```python
map() 得到的是一个 object 需要进行其他的实体化操作才能得需要的值
# 返回的是一个迭代器
>>>def square(x) :            # 计算平方数
...     return x ** 2
... 
#  传入的是函数名 不带()
>>> map(square, [1,2,3,4,5])   # 计算列表各个元素的平方
[1, 4, 9, 16, 25]

# 传入的时候一个匿名函数  
>>> map(lambda x: x ** 2, [1, 2, 3, 4, 5])  # 使用 lambda 匿名函数
[1, 4, 9, 16, 25]
 
# 提供了两个列表，对相同位置的列表数据进行相加, map 会自动查找需要是参数
>>> map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
[3, 7, 11, 15, 19]
```



## Easy_note

<< Java 与模式>>

```python
集合:	
    
nolocal:
    上一层函数中的变量引用申明
闭包:   
    延长了参数的生命周期  时期参数值变化	
    	def make_counter():
            count = 0
            def counter():
                nonlocal count
                count += 1
                return count
            return counter

        mc = make_counter()
        print(mc())   #1
        print(mc())   #2
        print(mc())   #3
        

config:   (中文释义:配置,布局,显示配置信息)

assert:
    只有满足其后面的条件程序才能向下执行
   		应用:
            通常情况传递参数不会有误，但编写大量的参数检查影响编程效率，而且不需要检查参数的合法性。
            排除非预期的结果。

_ str _

randrange(num):
    在0 - num 范围内随机去值   相当于 randint(range(num))

     
enumerate():   
            将一个可以遍历的数据对象(列表,元组 , 字符串 ) 组合成一个索引序列 , 同时给出数据和下标  默认下标为0 开始
            可设置start=num  规定其开始的下标
            在写 for 循环是增加一个参数 i 
    
            >>>seq = ['one', 'two', 'three']
            >>>for i, element in enumerate(seq):
            ...    print(i, seq[i])
            ... 
            0 one
            1 two
            2 three
            >>>
            >>>seasons = ['Spring', 'Summer', 'Fall', 'Winter']
            >>>list(enumerate(seasons))
            [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
            >>>list(enumerate(seasons, start=1))       # 小标从 1 开始
            [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]

```

**-全局变量**: 
    在局部如果不声明全局变量，并且不修改全局变量。则可以正常使用全局变量
    在局部如果不声明全局变量，并且不修改全局变量。则可以正常使用全局变量：

####nonlocal

```python
nonlocal:
    用来在函数或其他作用域中使用外层(非全局)变量
    def scope_test():
    def do_local():
        spam = "local spam" #此函数定义了另外的一个spam字符串变量，并且生命周期只在此函数内。此处的spam和外层的spam是两个变量，如果写出spam = spam + “local spam” 会报错
    def do_nonlocal():
        nonlocal  spam        #使用外层的spam变量
        spam = "nonlocal spam"
    def do_global():
        global spam
        spam = "global spam"     # 输出为nonlocal中的spam???
    spam = "test spam"
    do_local()
    print("After local assignmane:", spam)   # test spam
    do_nonlocal()
    print("After nonlocal assignment:",spam)   #nonlocal spam
    do_global()
    print("After global assignment:",spam)   # nonlocal spam

scope_test()
print("In global scope:",spam)

########################################2222
def make_counter(): 
    count = 0 
    def counter(): 
        nonlocal count 
        count += 1 
        return count 
    return counter 

def make_counter_test(): 
  mc = make_counter() 
  print(mc())
  print(mc())
  print(mc())

make_counter_test()

output:
1
2
3
    
```

## 1. str 字符串操作

```python
常见的字符串函数
zip 
    l = ['a', 'b', 'c', 'd', 'e', 'f']
    b = zip(l[:-1], l[1:])
    print(dict(b))  # 可以映射成字典,元组,列表
    {'a': 'b', 'b': 'c', 'c': 'd', 'd': 'e', 'e': 'f'}
str1.split()：
	过指定分隔符对字符串进行切片，如果参数num 有指定值，则仅分隔 num 个子字符串

str1.splitlines():
	按照行('\r', '\r\n', \n')分隔，返回一个包含各行作为元素的列表，如果参数 keepends 为 False，不包含换行符，如果为 True，则保留换行符。
    
str1.join(): 
    用于将序列中的元素以指定的字符连接生成一个新的字符串。
    
max():
    返回给定参数的最大值，参数可以为序列
    
min():
    返回字符串中最小的字母。
    
str1.replace(old, new[, max]):
    把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次。
    
str1.maketrans():
    返回字符串转换后生成的新字符串。
    
str47.translate(table[, delete]):
	intable = 'adsda
	outtable = '12345
	trantab = str.marketrans(intable, outtable)
	st1 = '*********'
	result = st1.translate(trantab[,delate])
	result 是翻译后的结果 delate  可 正则删除
    返回翻译后的字符串,若给出了 delete 参数，则将原来的bytes中的属于delete的字符删除，剩下的字符要按照table中给出的映射来进行映射 。
    
str1.startswith(str, beg=0,end=len(string)):
    方法用于检查字符串是否是以指定子字符串开头，如果是则返回 True，否则返回 False。如果参数 beg 和 end 指定值，则在指定范围内检查。
    
str1.endswith(suffix[, start[, end]]):
    方法用于判断字符串是否以指定后缀结尾，如果以指定后缀结尾返回True，否则返回False。可选参数"start"与"end"为检索字符串的开始与结束位置
    s
str1.encode():
    指定的编码格式编码字符串
    
bytes.decode():
    以指定的编码格式解码 bytes 对象。默认编码为 'utf-8'。
    
str1.isalpha():
    方法检测字符串是否只由字母组成。
    
str1.isalnum():
    检测字符串是否由字母和数字组成。
    
str1.isupper():
    检测字符串中所有的字母是否都为大写。
    
str1.islower():
    检测字符串是否由小写字母组成。
    
str1.istitle():
    检测字符串中所有的单词拼写首字母是否为大写，且其他字母为小写。
    
str1.isdigit():
    检测字符串是否只由数字组成。
    
str1.isnumeric():
    检测字符串是否只由数字组成。这种方法是只针对unicode对象
    
str1.isdecimal():
    检查字符串是否只包含十进制字符。这种方法只存在于unicode对象
    
str1.isspace():
    检测字符串是否只由空白字符组成
    
len():
    返回对象（字符、列表、元组等）长度或项目个数。
    
lower():
    转换字符串中所有大写字符为小写。
    
upper():
    将字符串中的小写字母转为大写字母。
    
swapcase():
    用于对字符串的大小写字母进行转换。
    
capitalize():
    将字符串的第一个字母变成大写,其他字母变小写
    
title():
    返回"标题化"的字符串,就是说所有单词都是以大写开始
    
center(width[, fillchar]):   ?????
    返回一个指定的宽度 width 居中的字符串，fillchar 为填充的字符，默认为空格。
    
ljust(width[, fillchar]):
    返回一个原字符串左对齐,并使用空格填充至指定长度的新字符串。如果指定的长度小于原字符串的长度则返回原字符串。
    
rjust(width[, fillchar]):
    回一个原字符串右对齐,并使用空格填充至长度 width 的新字符串。如果指定的长度小于字符串的长度则返回原字符串。
    
zfill(width):
    返回指定长度的字符串，原字符串右对齐，前面填充0。
    
count():
    统计字符串里某个字符出现的次数。可选参数为在字符串搜索的开始与结束位置
    
find():
    方法检测字符串中是否包含子字符串 str ，如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，如果指定范围内如果包含指定索引值，返回的是索引值在字符串中的起始位置。如果不包含索引值，返回-1。
    
rfind():
    返回字符串最后一次出现的位置，如果没有匹配项则返回-1。
    
index():
    方法检测字符串中是否包含子字符串 str ，如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，该方法与 python find()方法一样，只不过如果str不在 string中会报一个异常。
    
rindex(str, beg=0 end=len(string)):
    返回子字符串 str 在字符串中最后出现的位置，如果没有匹配的字符串会报异常，你可以指定可选参数[beg:end]设置查找的区间。
strip():
    用于移除字符串头尾指定的字符（默认为空格）
    
lstrip():
    方法用于截掉字符串左边的空格或指定字符。
rstrip():
    删除 string 字符串末尾的指定字符（默认为空格）.

```

## 2.  OS模块  文件操作  

```
1.获取当前操作系统         os.name
2.查看当前操作系统的详细信息    os.uname()
3.获取当前操作系统的环境变量     ** os.environ    返回为一个dict
4.获取指定的环境变量    os.environ.get('path')    **
5.获取当前目录     os.curdir
6.获取当前工作目录       os.getcwd()
7.在当前目录下创建新的目录    os.mkdir('path')
8.删除目录       os.rmdir()
9.删除文件       os.remove()
10.文件重命名         os.rename(old, new)
11.获取文件属性      os.stat('path')
12.路径拼接        os.path.join()
13.拆分文件扩展名        os.path.split()       os.path.splitext()                ************
14.判断目录是否存在      os.path.exists()
15.判断是否是目录                os.path.isdir()
16.判断是否是文件    	  os.path.isfile()
17.获取文件的大小	      os.path.getsize()
18.获取当前文件目录所在的目录   os.path.dirname()
19.获取当前文件的文件名         os.path.basename() 

```

### 文件打开 open()

```python
模式	描述
r	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
rb	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。
r+	打开一个文件用于读写。文件指针将会放在文件的开头。
rb+	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。
w	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
wb	以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
w+	打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
wb+	以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
a	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
ab	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
ab+	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。
```

### file() 对象方法

```python
file.read([size]) size未指定则返回整个文件,如果文件大小>2倍内存则有问题.f.read()读到文件尾时返回""(空字串)

file.readline() 返回一行

file.readlines([size]) 返回包含size行的列表,size 未指定则返回全部行

for line in f: print line #通过迭代器访问

f.write("hello\n") #如果要写入字符串以外的数据,先将他转换为字符串.

f.tell() 返回一个整数,表示当前文件指针的位置(就是到文件头的比特数).

f.seek(偏移量,[起始位置]) 用来移动文件指针.

偏移量:单位:比特,可正可负
起始位置:0-文件头,默认值;1-当前位置;2-文件尾
f.close() 关闭文件
```



## 3.time  datetime  calendar

```
time.time()  时间戳,从1970-1-1 0时开始计算时间  秒
time.gmtime()  时间戳转换为UTC时间
time.localtime()  获取本地时间
time.mktime()    将时间转化为时间戳函数
time.asctime()     将时间转化为用户可读的字符串格式
time.ctime()    将时间戳转化为用户可读的时间
time.strftime()  将时间字符串格式化输出给用户看
time.strptime()   将时间转化为元组时间的格式

datetime.datetime.now()
datetime.datetime()
.strftime()
datetime.datetime.strptime(date, '%Y-%m-%d')

calendar.month()
calendar.calendar()
calendar.monthrange()
calendar.monthcalendar()

```

### 格式化时间字符串

```python
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
```

## 4.面向对象

```python 
@property   # 属性包装器
@   .setter       # 修改属性
@classmethod    # 类方法
@staticmethod     # 抽象方法
MethodType         # 动态添加

抽象方法  from abc import abstractmethod, ABCMeta
		metaclass=ABCmeta   # 默认的类参数
    	@abstractmethod    # 定义抽象方法
 super().__init__()

from enum import Enum       # 枚举
class Color(Enum):
    red = 1

```





###运算符重载

```
在类中，对内置对象（例如，整数和列表）所能做的事，几乎都有相应的特殊名称的重载方法。下表列出其中一些最常用的重载方法。

  方法          	重载        	调用                              
  init        	构造函数      	对象建立：X = Class(args)            
  del         	析构函数      	X对象收回                           
  add         	运算符+      	如果没有iadd,X+Y,X+=Y               
  or          	运算符\|(位OR)	如果没有ior,X\|Y,X\|=Y              
  repr,str    	打印、转换     	print（X）、repr(X),str(X)         
  call        	函数调用      	X(*args,**kargs)                
  getattr     	点号运算      	X.undefined                     
  setattr     	属性赋值语句    	X.any = value                   
  delattr     	属性删除      	del X.any                       
  getattribute	属性获取      	X.any                           
  getitem     	索引运算      	X[key],X[i:j],没iter时的for循环和其他迭代器
  setitem     	索引赋值语句    	X[key] = value,X[i:j] = sequence
  delitem     	索引和分片删除   	del X[key],del X[i:j]           
  len         	长度        	len(X),如果没有bool,真值测试            
  bool        	布尔测试      	bool(X),真测试                     
  lt,gt,      	特定的比较     	X < Y,X > Y                     
  le,ge,      	          	X<=Y,X >= Y                     
  eq,ne       	          	X == Y,X != Y                   
  radd        	右侧加法      	Other+X                         
  iadd        	实地（增强的）加法 	X += Y （or else add）            
  iter,next   	迭代环境      	I = iter(X),next(I)             
  contains    	成员关系测试    	item in X （任何可迭代的）              
  index       	整数值       	hex(X),bin(X),oct(X),O[X],O[X:] 
  enter,exit  	环境管理器     	with obj as var:                
  get,set     	描述符属性     	X.attr,X.attr = value,del X.attr
  new         	创建        	在init之前创建对象                     

```

## 5.正则表达式

```python
finditer()  迭代器    用 next() 方法进行迭代器操作
sub()    返回被替换后的字符串
subn()   返回一个元组, 第一个为被替换是字符串, 第二个是替换的次数

分组;
	除了简单的判断是否匹配外, 还能提取子串
    用() 表示提取出的分组
	str2 = '01053247654'
    m = re.match((r'(\d{3})(\d{8})'), str2)
    m = re.match((r'(?P<name1>\d{3})-(?P<name2>\d{8})'), str2)

    group(0)  原始字符串
    group(1)  
    group(2)
    m = m.groups()
    print(m)
    
    
compile(pattern ,flags=0)    pattern 正则表达式
    
    
    
```



### 正则常用字符

```python
\w匹配字母数字及下划线

\W匹配非字母数字及下划线

\s匹配任意空白字符，等价于 [\t\n\r\f].

\S匹配任意非空字符

\d匹配任意数字，等价于 [0-9]

\D匹配任意非数字

\A匹配字符串开始

\Z匹配字符串结束，如果是存在换行，只匹配到换行前的结束字符串

\z匹配字符串结束

\G匹配最后匹配完成的位置

\n匹配一个换行符

\t匹配一个制表符

^匹配字符串的开头

$匹配字符串的末尾。

.匹配任意字符，除了换行符，当re.DOTALL标记被指定时，则可以匹配包括换行符的任意字符。

[...]用来表示一组字符,单独列出：[amk] 匹配 'a'，'m'或'k'

[^...]不在[]中的字符：abc 匹配除了a,b,c之外的字符。

*匹配0个或多个的表达式。

+匹配1个或多个的表达式。

?匹配0个或1个由前面的正则表达式定义的片段，非贪婪方式

{n}精确匹配n个前面表达式。

{n, m}匹配 n 到 m 次由前面的正则表达式定义的片段，贪婪方式

a|b匹配a或b

( )匹配括号内的表达式，也表示一个组

```

###正则匹配模式

```
re.match()    开头开始匹配  一个
re.search()    整个查找 一个
re.findall()     全局查找,匹配所有
re.sub('查找要替换的 表达式', '替换的字符', str)
re.compile()     compile()还可以传入修饰符，例如re.S等修饰符，这样在search()、findall()等方法中就不需要额外传了。所以compile()方法可以说是给正则表达式做了一层封装，以便于我们更好地复用。
```

### 常用的表达式

```python
一、校验数字的表达式
数字：^[0-9]*$
n位的数字：^\d{n}$
至少n位的数字：^\d{n,}$
m-n位的数字：^\d{m,n}$
零和非零开头的数字：^(0|[1-9][0-9]*)$
非零开头的最多带两位小数的数字：^([1-9][0-9]*)+(\.[0-9]{1,2})?$
带1-2位小数的正数或负数：^(\-)?\d+(\.\d{1,2})$
正数、负数、和小数：^(\-|\+)?\d+(\.\d+)?$
有两位小数的正实数：^[0-9]+(\.[0-9]{2})?$
有1~3位小数的正实数：^[0-9]+(\.[0-9]{1,3})?$
非零的正整数：^[1-9]\d*$ 或 ^([1-9][0-9]*){1,3}$ 或 ^\+?[1-9][0-9]*$
非零的负整数：^\-[1-9][]0-9"*$ 或 ^-[1-9]\d*$
非负整数：^\d+$ 或 ^[1-9]\d*|0$
非正整数：^-[1-9]\d*|0$ 或 ^((-\d+)|(0+))$
非负浮点数：^\d+(\.\d+)?$ 或 ^[1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0$
非正浮点数：^((-\d+(\.\d+)?)|(0+(\.0+)?))$ 或 ^(-([1-9]\d*\.\d*|0\.\d*[1-9]\d*))|0?\.0+|0$
正浮点数：^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$ 或 ^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$
负浮点数：^-([1-9]\d*\.\d*|0\.\d*[1-9]\d*)$ 或 ^(-(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*)))$
浮点数：^(-?\d+)(\.\d+)?$ 或 ^-?([1-9]\d*\.\d*|0\.\d*[1-9]\d*|0?\.0+|0)$
校验字符的表达式
汉字：^[\u4e00-\u9fa5]{0,}$
英文和数字：^[A-Za-z0-9]+$ 或 ^[A-Za-z0-9]{4,40}$
长度为3-20的所有字符：^.{3,20}$
由26个英文字母组成的字符串：^[A-Za-z]+$
由26个大写英文字母组成的字符串：^[A-Z]+$
由26个小写英文字母组成的字符串：^[a-z]+$
由数字和26个英文字母组成的字符串：^[A-Za-z0-9]+$
由数字、26个英文字母或者下划线组成的字符串：^\w+$ 或 ^\w{3,20}$
中文、英文、数字包括下划线：^[\u4E00-\u9FA5A-Za-z0-9_]+$
中文、英文、数字但不包括下划线等符号：^[\u4E00-\u9FA5A-Za-z0-9]+$ 或 ^[\u4E00-\u9FA5A-Za-z0-9]{2,20}$
可以输入含有^%&',;=?$\"等字符：[^%&',;=?$\x22]+
禁止输入含有~的字符：[^~\x22]+


三、特殊需求表达式
Email地址：^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$
域名：[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/.?
InternetURL：[a-zA-z]+://[^\s]* 或 ^http://([\w-]+\.)+[\w-]+(/[\w-./?%&=]*)?$
手机号码：^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$
电话号码("XXX-XXXXXXX"、"XXXX-XXXXXXXX"、"XXX-XXXXXXX"、"XXX-XXXXXXXX"、"XXXXXXX"和"XXXXXXXX)：^(\(\d{3,4}-)|\d{3.4}-)?\d{7,8}$
国内电话号码(0511-4405222、021-87888822)：\d{3}-\d{8}|\d{4}-\d{7}
电话号码正则表达式（支持手机号码，3-4位区号，7-8位直播号码，1－4位分机号）: ((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)
身份证号(15位、18位数字)，最后一位是校验位，可能为数字或字符X：(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)
帐号是否合法(字母开头，允许5-16字节，允许字母数字下划线)：^[a-zA-Z][a-zA-Z0-9_]{4,15}$
密码(以字母开头，长度在6~18之间，只能包含字母、数字和下划线)：^[a-zA-Z]\w{5,17}$
强密码(必须包含大小写字母和数字的组合，不能使用特殊字符，长度在8-10之间)：^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$
日期格式：^\d{4}-\d{1,2}-\d{1,2}
一年的12个月(01～09和1～12)：^(0?[1-9]|1[0-2])$
一个月的31天(01～09和1～31)：^((0?[1-9])|((1|2)[0-9])|30|31)$
钱的输入格式：
有四种钱的表示形式我们可以接受:"10000.00" 和 "10,000.00", 和没有 "分" 的 "10000" 和 "10,000"：^[1-9][0-9]*$
这表示任意一个不以0开头的数字,但是,这也意味着一个字符"0"不通过,所以我们采用下面的形式：^(0|[1-9][0-9]*)$
一个0或者一个不以0开头的数字.我们还可以允许开头有一个负号：^(0|-?[1-9][0-9]*)$
这表示一个0或者一个可能为负的开头不为0的数字.让用户以0开头好了.把负号的也去掉,因为钱总不能是负的吧。下面我们要加的是说明可能的小数部分：^[0-9]+(.[0-9]+)?$
必须说明的是,小数点后面至少应该有1位数,所以"10."是不通过的,但是 "10" 和 "10.2" 是通过的：^[0-9]+(.[0-9]{2})?$
这样我们规定小数点后面必须有两位,如果你认为太苛刻了,可以这样：^[0-9]+(.[0-9]{1,2})?$
这样就允许用户只写一位小数.下面我们该考虑数字中的逗号了,我们可以这样：^[0-9]{1,3}(,[0-9]{3})*(.[0-9]{1,2})?$
1到3个数字,后面跟着任意个 逗号+3个数字,逗号成为可选,而不是必须：^([0-9]+|[0-9]{1,3}(,[0-9]{3})*)(.[0-9]{1,2})?$
备注：这就是最终结果了,别忘了"+"可以用"*"替代如果你觉得空字符串也可以接受的话(奇怪,为什么?)最后,别忘了在用函数时去掉去掉那个反斜杠,一般的错误都在这里
xml文件：^([a-zA-Z]+-?)+[a-zA-Z0-9]+\\.[x|X][m|M][l|L]$
中文字符的正则表达式：[\u4e00-\u9fa5]
双字节字符：[^\x00-\xff] (包括汉字在内，可以用来计算字符串的长度(一个双字节字符长度计2，ASCII字符计1))
空白行的正则表达式：\n\s*\r (可以用来删除空白行)
HTML标记的正则表达式：<(\S*?)[^>]*>.*?|<.*? /> ( 首尾空白字符的正则表达式：^\s*|\s*$或(^\s*)|(\s*$) (可以用来删除行首行尾的空白字符(包括空格、制表符、换页符等等)，非常有用的表达式)
腾讯QQ号：[1-9][0-9]{4,} (腾讯QQ号从10000开始)
中国邮政编码：[1-9]\d{5}(?!\d) (中国邮政编码为6位数字)
IP地址：((?:(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d)\\.){3}(?:25[0-5]|2[0-4]\\d|[01]?\\d?\\d))
```



## 6. 常用  快捷键

```python
cyrl + P 查看参数提醒

debug
pycharm 中的红圈 是断点, 到断点程序会停止  用 debug 模式调试程序


```

## 7. cmd   ping  操作命令

```word
cmd    ipconfig  查看网络地址
ping  + 网址   查看网络信息   检查网络可达性
pip install   安装pycharm 包
netsatat -na   查看网络状态
pip install pycodestyle   安装python格式检查器

```



## ---发邮件与发短信

```
互亿无线： http://user.ihuyi.com
注册163邮箱： http://mail.163.com
```

### 发短信

C81937851

16a0b151f0af1f617db89fcb11667e0c

```python
# 接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
# 账户注册：请通过该地址开通账户http://sms.ihuyi.com/register.html
# 注意事项：
# （1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
# （2）请使用APIID（查看APIID请登录用户中心->验证码短信->产品总览->APIID）及 APIkey来调用接口；
# （3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；

# !/usr/local/bin/python
# -*- coding:utf-8 -*-
import http.client
import urllib

host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

# 用户名是登录用户中心->验证码短信->产品总览->APIID
account = "C81937851"
# 密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
password = "16a0b151f0af1f617db89fcb11667e0c"


def send_sms(text, mobile):
    params = urllib.parse.urlencode(
        {'account': account, 'password': password, 'content': text, 'mobile': mobile, 'format': 'json'})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


if __name__ == '__main__':
    mobile = "15884550995"
    text = "您的验证码是：888888。请不要把验证码泄露给其他人。"

    print(send_sms(text, mobile))
```

### 发邮件

```python
#首先导入一个发邮件的库
import smtplib
# 接受我们所需要的文本库
from email.mime.text import MIMEText
from email.header import Header


# smtp服务器的地址
SMTPServer = 'smtp.163.com'

# 发邮件的地址
Sender = 'liuhaiyan_11260814@163.com'


# 发送邮件的授权密码
Password = 'q1234567890'

# 发邮件的内容
Message = 'liuhaiyan'

# 将内容转成邮件格式
Msg = MIMEText(Message)


# 邮件标题
Msg['Subject'] = '一封来自美女的邮件'

# 发送者
Msg['From'] = Sender


# 开始创建smtp服务器
mailServer = smtplib.SMTP(SMTPServer, 25)


# 接着登录邮箱
mailServer.login(Sender, Password)

#发送邮件
mailServer.sendmail(Sender, ['liuhaiyan_11260814@163.com', 'zyz13219083090@163.com'], Msg.as_string())

# 退出邮箱
mailServer.quit()
```





## 8. 网络介绍

```python
多台独立自主的计算机互联的总称叫计算机网络
实现信息互联与资源共享 

网络接口 -->  网络  -->  传输  --> 应用 

协议  protocol  通信双方需要遵循的规范和标准

Inernet  因特网   基于TCP/IP Model 的网络 
互联网  可以用任何协议
 
network    IP   ICMP 寻址 路由
传输协议   TCP  UDP 是在IP 之上构建的传输协议 , 它能提供传输数据服务



TCP   可靠传输协议    
传输控制协议  Transfer Control Protocol
1, 可靠通信(数据不会穿丢也不会传错
2. 流量控制  自动调节发送数据的速度
3. 拥塞控制  网络拥堵时会降低发送速率
        
可靠通讯的实现:
            如何保证数据不会传输错误
             握手机制 +    在数据中添加冗余校验对发送的数据                            进行校验
流量控制:
        滑动窗口机制   逐步增加发送的数据大小
        
拥塞控制:
        减小滑动窗口  减小发送速率
        
     
        
UDP  User Datagram Protocol 用户数据宝协议
        数据可能会丢失某部分内容 只要不影响使用  列如视屏  不会影响用户的使用
     
        
        
应用层   QQ 微信       OICQ(QQ)
        www.baidu.com 
        
    HTTP  Hyper Text Transfer Protocol
    HTTPS
        
        
URL 统一资源定位服务    端口 0 - 65535  2**16    
       
       
```

![4-18-00](C:\Users\Administrator\Desktop\screenshots\04-18-002.png)



## 9. 天行数据

```python
APIKEY:30cb00f0e0f6c2f605ba1ebca41c3282

    微信调用 :https://api.tianapi.com/weixin/key=30cb00f0e0f6c2f605ba1ebca41c3282


```

## 10.   扒图片

```python
import os
import requests, json


def get_file(path):
    """
    在url中查找图片

    :param path:
    :return:   查找结果
    """
    resp = requests.get(path)
    url_dict = json.loads(resp.text, encoding='utf-8')
    i = 0
    for new_dict in url_dict['newslist']:
        url = new_dict['picUrl']
        resp_new = requests.get(url)
        print(resp_new.content)
        i += 1
        with open ('%d.jpg' % i, 'wb') as f:
            f.write(resp_new.content)
            print(i)
    print('下载完成')


def rm_picture(path):
    """
    删除jpg格式文件

    :param path: 删除的文件夹
    """
    list_file = os.listdir(path)
    for file in list_file:
        if file[file.rindex('.') + 1:] == 'jpg':
            os.remove(file)
    print('图片删除完毕')


path_file = '../day18'
path_url = 'http://api.tianapi.com/meinv/?key=30cb00f0e0f6c2f605ba1ebca41c3282&num=1'
def main():
    # get_file(path_url)
    rm_picture(path_file)


if __name__ == '__main__':
    main()
```

 #### API  应用程序编程接口



```python
200   success
5**   服务器爆炸
 
    交换的是纯文本  所有系统都能接受
def main():
    # 网络数据接口   网络 API
    # 通过网络API  拿到两种数据接口  XML / JSON  其中一种
    #
    resp = requests.get('	http://api.tianapi.com/meinv/?key=30cb00f0e0f6c2f605ba1ebca41c3282&num=2')
    print(resp.text)


if __name__ == '__main__':
    main()


```

### XML    可扩展标签语言   

### JSON   对象编辑语言  

JavaScript Object Notation

```python

JSON   发送消息 
{
    'from':'person'
    'to':'person1'
    'content':'内容'
    
}


```



## 11. p2 和 p3 区别 与转换

```python


URL 不能写中文  谷歌浏览器 自动转化为百分号编码



Linux 系统下有  2to3 命令
                2to3 -W 文件名    实现2 - 3 的转换
    
    
tcp  udp

```



## 12.网络编程  服务器  客户端 

```
折半法    每次从中间开始考虑   搜索范围减小一一半


```

### 套接字编程   socket()

```python
套接字socket    其实是c语言的函数 (基于FreeBSD) ,提供了网络访问和使用网络的方法
server    服务器
client    客户端
browser   浏览器
C/S       客户端服务器
B/S       浏览器服务器
P2P       点对点模式    peer-

```

### 服务器与客户端

```python
********     服务器        #### 套接字编程  socket()
from socket import socket


def servey():
    ser_temp = socket()
    ser_temp.bind(('10.7.152.105', 7779))
    ser_temp.listen()
    while True:
        client, addr = ser_temp.accept()
        while True:     #  必须有这个循环才能一直接受一个客户的消息, 没有循环只能接收一次
            get_msg = client.recv(1024).decode('utf-8')
            print(get_msg)
            sed_msg = input('服务器:').encode('utf-8')
            client.send(sed_msg)


 ***********   客户端  ***********************         
from socket import socket


def client():
    client = socket()
    client.connect(('10.7.152.105', 7779))
    while True:
        msg = input('客户端:').encode('utf-8')
        client.send(msg)
        get_msg = client.recv(1024).decode('utf-8')
        print(get_msg)
```





###   serve_robot

```python
#服务器
from random import randint
from socket import socket
from time import sleep


class Robot(object):
    def __init__(self):
        self.answer = randint(1, 100)
        self._hint = ''
        self.count = 0

    @property
    def hint(self):
        return self._hint

    def judge(self, yours):
        self.count += 1
        if yours > self.answer:
            self._hint = '请输入小一点'
        elif yours < self.answer:
            self._hint = '请输入大一点'
        else:
            self._hint = '猜对了,但没有奖励....'
            if self.count > 7:
                self._hint += '\n智商真捉急!!!'
            return True
        return  False


def main():
    robot = Robot()
    server = socket()
    server.bind(('10.7.152.105', 9669))
    server.listen(512)
    print('服务器开启...')
    while True:
        client, addr = server.accept()
        print(addr)
        while True:
            get_msg = int(client.recv(1024).decode('utf-8'))
            if 0 < get_msg < 100:
                robot.judge(get_msg)
                out_msg = robot.hint
                client.send(out_msg.encode('utf-8'))
            else:
                out_msg = '输入有误,重新输入'
                client.send(out_msg.encode('utf-8'))

    print('服务器关闭.....')
    server.close()


if __name__ == '__main__':
    main()
    
    
    \****************************************\
    # 客户端

from socket import socket


def main():
    client = socket()
    client.connect(('10.7.152.105', 9669))
    while True:
        numstr = input('输入数字:')
        client.send(numstr.encode('utf-8'))
        in_msg = client.recv(1024).decode('utf-8')
        print(in_msg)

    print('客户端断开连接')
    client.close()


if __name__ == '__main__':
    main()
```

### BASE 64 编码

```python
将二进制数据变为有64种符号表示的文本
011011001100001111010011
将二进制编码每6位分开
```

### 处理方法  示例

```python
用一个字典的 键值对 形式保存要发送的数据
将字典处理成 JSON 格式进行传输

JSON 只能是纯文本   用 BSAE64 处理二进制数据 
    dumps()处理二进制数据
  
\***********************       服务器
from socket import socket, SOCK_STREAM, AF_INET
from base64 import b64encode
from json import dumps


def main():
    # 1.创建套接字对象并指定使用哪种传输服务
    server = socket()
    # 2.绑定IP地址和端口(区分不同的服务)
    server.bind(('10.7.152.69', 5566))
    # 3.开启监听 - 监听客户端连接到服务器
    server.listen(512)
    print('服务器启动开始监听...')
    with open('memory.png', 'rb') as f:
        # 将二进制数据处理成base64再解码成字符串
        data = b64encode(f.read()).decode('utf-8')
    while True:
        client, addr = server.accept()
        # 用一个字典(键值对)来保存要发送的各种数据
        # 待会可以将字典处理成JSON格式在网络上传递
        my_dict = dict({})
        my_dict['filename'] = 'memory.png'
        # JSON是纯文本不能携带二进制数据
        # 所以图片的二进制数据要处理成base64编码
        my_dict['filedata'] = data
        # 通过dumps函数将字典处理成JSON字符串
        json_str = dumps(my_dict)
        # 发送JSON字符串
        client.send(json_str.encode('utf-8'))
        client.close()


if __name__ == '__main__':
    main()
**********************************************
##   客户端  #############
from socket import socket
from json import loads
from base64 import b64decode


def main():
    client = socket()
    client.connect(('10.7.152.69', 5566))
    # 定义一个保存二进制数据的对象
    in_data = bytes()
    # 由于不知道服务器发送的数据有多大每次接收1024字节
    data = client.recv(1024)
    while data:
        # 将收到的数据拼接起来
        in_data += data
        data = client.recv(1024)
    # 将收到的二进制数据解码成JSON字符串并转换成字典
    # loads函数的作用就是将JSON字符串转成字典对象
    my_dict = loads(in_data.decode('utf-8'))
    filename = my_dict['filename']
    filedata = my_dict['filedata'].encode('utf-8')
    with open('c:/images/' + filename, 'wb') as f:
        # 将base64格式的数据解码成二进制数据并写入文件
        f.write(b64decode(filedata))
    print('图片已保存.')


if __name__ == '__main__':
    main()


```



### homework

```python

```

### 栈 堆  静态区

```python
stack 栈         对象的引用  对象引用类
heap  堆       最大的区域    对象    
				栈中  xiaoyu = Xiaoyu() 堆
static area 静态区

```

![](C:\Users\Administrator\Desktop\screenshots\04-20-006.png)





## 13. 线程  进程

```python
进程: 操作系统分配内存的基本单元 以进程来隔离内存  
      一个进程 有一个或多个线程
线程:  操作系统分配 CPU 的基本单位   
       线程都是在cpu一个核心上

多线程 : 改善用户体验  提高效率
    
better : 单线程操作   异步I/O操作其余的工作  
```

### 前端工具  Sublime  + Emmet((代码提示)

```
HBuilder  / webStorm
jetbrans 公司   考特林 编程语言  Kotlin
```

### 博客



```
dict(zip([k for k in d.values], [for v in d.keys]))
```



***

- ​