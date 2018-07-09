# AWK

条件,循环,与C语法相通

awk是一个强大的文本分析工具，相对于grep的查找，sed的编辑，awk在其对数据分析并生成报告时，显得尤为强大。简单来说awk就是把文件逐行的读入，以空格为默认分隔符将每行切片，切开的部分再进行各种分析处理。

`awk '{pattern + action}' {filenames}`或者`awk 'BEGIN{ commands } pattern{ commands } END{ commands }'`

尽管操作可能会很复杂，但语法总是这样，其中 pattern 表示 AWK 在数据中查找的内容，而action 是在找到匹配内容时所执行的一系列命令。花括号（{}）不需要在程序中始终出现，但它们用于根据特定的模式对一系列指令进行分组。 pattern就是要表示的正则表达式，用斜杠括起来。

awk语言的最基本功能是在文件或者字符串中基于指定规则浏览和抽取信息，awk抽取信息后，才能进行其他文本操作。完整的awk脚本通常用来格式化文本文件中的信息。

通常，awk是以文件的一行为处理单位的。awk每接收文件的一行，然后执行相应的命令，来处理文本。

awk工作流程是这样的：读入有'\n'换行符分割的一条记录，然后将记录按指定的域分隔符划分域，填充域，$0则表示所有域,$1表示第一个域,$n表示第n个域。默认域分隔符是"空白键" 或 "[tab]键",也可以使用`-F delimiter`来制定

`awk  -F ':'  'BEGIN {print "name,shell"}  {print $1","$7} END {print "blue,/bin/nosh"}'`

`BEGIN`表示在读取文件执行执行所做的操作,`END`表示执行结束后执行的操作

`awk -F: '/^root/' /etc/passwd`这里的`/^root/`时pattern,没有制定action,分隔符时`:`


## 内置变量

- ARGC:命令行参数个数
- ARGV:命令行参数排列
- ENVIRON:支持队列中系统环境变量的使用
- FILENAME:awk浏览的文件名
- FNR:浏览文件的记录数
- FS: 设置输入域分隔符，等价于命令行 -F选项
- NF: 浏览记录的域的个数
- NR: 已读的记录数
- OFS:输出域分隔符
- ORS:输出记录分隔符
- RS: 控制记录分隔符

```shell
awk  -F ':'  '{print "filename:" FILENAME ",linenumber:" NR ",columns:" NF ",linecontent:"$0}' /etc/passwd
filename:/etc/passwd,linenumber:1,columns:7,linecontent:root:x:0:0:root:/root:/bin/bash
filename:/etc/passwd,linenumber:2,columns:7,linecontent:daemon:x:1:1:daemon:/usr/sbin:/bin/sh
filename:/etc/passwd,linenumber:3,columns:7,linecontent:bin:x:2:2:bin:/bin:/bin/sh
filename:/etc/passwd,linenumber:4,columns:7,linecontent:sys:x:3:3:sys:/dev:/bin/sh
```
使用printf替代print,可以让代码更加简洁，易读

`awk  -F ':'  '{printf("filename:%10s,linenumber:%s,columns:%s,linecontent:%s\n",FILENAME,NR,NF,$0)}' /etc/passwd`

### 自定义变量

```shell
awk 'BEGIN {count=0;print "[start]user count is ", count} {count=count+1;print $0;} END{print "[end]user count is ", count}' /etc/passwd

[start]user count is  0
root:x:0:0:root:/root:/bin/bash
...
[end]user count is  40


awk 'BEGIN {size=0;} {size=size+$5;} END{print "[end]size is ", size/1024/1024,"M"}' 
```

### 正则运算符

`~ ~!	匹配正则表达式和不匹配正则表达式`,例如:`awk 'BEGIN{a="100testa";if(a ~ /^100*/){print "ok";}}'`

### 其它运算符

- $	字段引用 
- 空格	字符串连接符 
- ?:	C条件表达式 
- in	数组中是否存在某键值

## for循环两种格式

```
for(变量 in 数组) {语句}
```

## 其他语句
- break 当 break 语句用于 while 或 for 语句时，导致退出程序循环。 
- continue 当 continue 语句用于 while 或 for 语句时，使程序循环移动到下一个迭代。 
- next 能能够导致读入下一个输入行，并返回到脚本的顶部。这可以避免对当前输入行执行其他的操作过程。
- exit 语句使主输入循环退出并将控制转移到END,如果END存在的话。如果没有定义END规则，或在END中应用exit语句，则终止脚本的执行。

## 数组的定义
awk 中的数组不必提前声明，也不必声明大小。数组元素用0或空字符串来初始化，这根据上下文而定。

可以使用下标
```
Array[1]="sun" 
Array[2]="kai"
```

可以使用字符串坐下标
```
Array["first"]="www" 
Array["last"]="name" 
Array["birth"]="1987"
```

## 数组相关函数

- length返回字符串以及数组长度，
- split进行分割字符串为数组，也会返回分割得到数组长度。
- asort对数组进行排序，返回数组长度

## 算术函数

- atan2( y, x )	返回 y/x 的反正切。 
- cos( x )	返回 x 的余弦；x 是弧度。 
- sin( x )	返回 x 的正弦；x 是弧度。
- exp( x )	返回 x 幂函数。 
- log( x )	返回 x 的自然对数。 
- sqrt( x )	返回 x 平方根。 
- int( x )	返回 x 的截断至整数的值。 
- rand( )	返回任意数字 n，其中 0 <= n < 1。 
- srand( [expr] )	将 rand 函数的种子值设置为 Expr 参数的值，或如果省略 Expr 参数则使用某天的时间。返回先前的种子值。

## 字符串函数

- gsub( Ere, Repl, [ In ] )	除了正则表达式所有具体值被替代这点，它和 sub 函数完全一样地执行。 
- sub( Ere, Repl, [ In ] )	用 Repl 参数指定的字符串替换 In 参数指定的字符串中的由 Ere 参数指定的扩展正则表达式的第一个具体值。sub 函数返回替换的数量。出现在 Repl 参数指定的字符串中的 &（和符号）由 In 参数指定的与 Ere 参数的指定的扩展正则表达式匹配的字符串替换。如果未指定 In 参数，缺省值是整个记录（$0 记录变量）。  
- index( String1, String2 )	在由 String1 参数指定的字符串（其中有出现 String2 指定的参数）中，返回位置，从 1 开始编号。如果 String2 参数不在 String1 参数中出现，则返回 0（零）。 
- length [(String)]	返回 String 参数指定的字符串的长度（字符形式）。如果未给出 String 参数，则返回整个记录的长度（$0 记录变量）。 
- blength [(String)] 返回 String 参数指定的字符串的长度（以字节为单位）。如果未给出 String 参数，则返回整个记录的长度（$0 记录变量）。 
- substr( String, M, [ N ] )	返回具有 N 参数指定的字符数量子串。子串从 String 参数指定的字符串取得，其字符以 M 参数指定的位置开始。M 参数指定为将 String 参数中的第一个字符作为编号 1。如果未指定 N 参数，则子串的长度将是 M 参数指定的位置到 String 参数的末尾 的长度。 
- match( String, Ere )	在 String 参数指定的字符串（Ere 参数指定的扩展正则表达式出现在其中）中返回位置（字符形式），从 1 开始编号，或如果 Ere 参数不出现，则返回 0（零）。RSTART 特殊变量设置为返回值。RLENGTH 特殊变量设置为匹配的字符串的长度，或如果未找到任何匹配，则设置为 -1（负一）。 
- split( String, A, [Ere] )	将 String 参数指定的参数分割为数组元素 A[1], A[2], . . ., A[n]，并返回 n 变量的值。此分隔可以通过 Ere 参数指定的扩展正则表达式进行，或用当前字段分隔符（FS 特殊变量）来进行（如果没有给出 Ere 参数）。除非上下文指明特定的元素还应具有一个数字值，否则 A 数组中的元素用字符串值来创建。 
- tolower( String )	返回 String 参数指定的字符串，字符串中每个大写字符将更改为小写。大写和小写的映射由当前语言环境的 `LC_CTYPE `范畴定义。 toupper( String )	返回 String 参数指定的字符串，字符串中每个小写字符将更改为大写。大写和小写的映射由当前语言环境的` LC_CTYPE `范畴定义。 
- sprintf(Format, Expr, Expr, . . . )	根据 Format 参数指定的 printf 子例程格式字符串来格式化 Expr 参数指定的表达式并返回最后生成的字符串。

## 一般函数
- close( Expression )	用同一个带字符串值的 Expression 参数来关闭由 print 或 printf 语句打开的或调用 getline 函数打开的文件或管道。如果文件或管道成功关闭，则返回 0；其它情况下返回非零值。如果打算写一个文件，并稍后在同一个程序中读取文件，则 close 语句是必需的。 
- system(command )	执行 Command 参数指定的命令，并返回退出状态。等同于 system 子例程。 
- Expression | getline [ Variable ]	从来自 Expression 参数指定的命令的输出中通过管道传送的流中读取一个输入记录，并将该记录的值指定给 Variable 参数指定的变量。如果当前未打开将 Expression 参数的值作为其命令名称的流，则创建流。创建的流等同于调用 popen 子例程，此时 Command 参数取 Expression 参数的值且 Mode 参数设置为一个是 r 的值。只要流保留打开且 Expression 参数求得同一个字符串，则对 
- getline 函数的每次后续调用读取另一个记录。如果未指定 Variable 参数，则 $0 记录变量和 NF 特殊变量设置为从流读取的记录。 getline [ Variable ] < Expression	从 Expression 参数指定的文件读取输入的下一个记录，并将 Variable 参数指定的变量设置为该记录的值。只要流保留打开且 Expression 参数对同一个字符串求值，则对 getline 函数的每次后续调用读取另一个记录。如果未指定 Variable 参数，则 $0 记录变量和 NF 特殊变量设置为从流读取的记录。 
- getline [ Variable ]	将 Variable 参数指定的变量设置为从当前输入文件读取的下一个输入记录。如果未指定 Variable 参数，则 $0 记录变量设置为该记录的值，还将设置 NF、NR 和 FNR 特殊变量。


## 时间函数
- mktime( YYYY MM dd HH MM ss[ DST])	生成时间格式 
- strftime([format [, timestamp]])	格式化时间输出，将时间戳转为时间字符串 具体格式，见下表. 
- systime()	得到时间戳,返回从1970年1月1日开始到当前时间(不计闰年)的整秒数

- %a	星期几的缩写(Sun) 
- %A	星期几的完整写法(Sunday) 
- %b	月名的缩写(Oct) 
- %B	月名的完整写法(October) 
- %c	本地日期和时间 
- %d	十进制日期 
- %D	日期 08/20/99 
- %e	日期，如果只有一位会补上一个空格 
- %H	用十进制表示24小时格式的小时 
- %I	用十进制表示12小时格式的小时 
- %j	从1月1日起一年中的第几天 
- %m	十进制表示的月份 
- %M	十进制表示的分钟 
- %p	12小时表示法(AM/PM) 
- %S	十进制表示的秒 
- %U	十进制表示的一年中的第几个星期(星期天作为一个星期的开始) 
- %w	十进制表示的星期几(星期天是0) 
- %W	十进制表示的一年中的第几个星期(星期一作为一个星期的开始) 
- %x	重新设置本地日期(08/20/99) 
- %X	重新设置本地时间(12：00：00) 
- %y	两位数字表示的年(99) 
- %Y	当前月份 
- %Z	时区(PDT) 
- %%	百分号(%)


# 问题

## 单引号
`awk '{print "\047"}'`

```
head  all_title_df.csv|awk -F, '{last=$NF;second=$(NF-1);third=$(NF-2))}' #倒数位置
awk -F, -v i=$i '{count=$10;if(count==i) print count,$0}' > 120/$i; i=$[i+1]; done#使用环境参数
```