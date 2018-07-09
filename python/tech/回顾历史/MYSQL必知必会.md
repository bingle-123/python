# MYSQL必知必会

# 使用MYSQL

## 查看数据库和表

show 主要用来查看信息.调用`help show`查看show的命令详情
```mysql
show databases ;查看数据库
show tables [from db_name];查看数据库下的表有哪些
show columns from table_name;查看数据表的列定义
show create [databases db_name][table table_name];显示创建数据库或数据库时的语句
show grants ;显示授权信息
```

# 检索数据

`select`

`[distinct]` 去除结果集中重复的行

`limit [start,] lines` 限制取出的行, start 表示从结果集中第几行开始的 lines 行数 **mysql 行号 start 是从0开始**

## 限定表名称

`select table_name.column_name from db_name.table_name`

# 排序检索数据

`order by [column_1,column_2] [desc]`

# 过滤数据

`where`

条件操作符`= , > , < , <> , != , >= , <= , between and`

空置 `is null`和`is not null`

# 数据过滤

组合where子句

`and , or`

## In **In比Or更快**

## NOT

# 通配符匹配

`like`

- `%` 表示任意字符任意次数
- `_` 匹配任意单个字符

# 正则表达式

转义使用`\\.`两个斜线

`regexp`和`rlike`一个意思

`1000|2000` 匹配1000或者2000

`[abc]` `[a-z]` `[0-9]` abc中任意一个字符

`.` 任意字符

`\\f`换页

`\\n`换行

`\\r`回车

`\\t`制表

`\\v`纵向制表

`[:alnum:] 任意字母和数字(同[a-zA-Z0-9])`

`[:alpha:] 任意字符(同[a-zA-Z])`

`[:blank:] 空格和制表(同[\\t])`

`[:cntrl:] ASCII控制字符(ASCII 0到31和127)`

`[:digit:] 任意数字(同[0-9])`

`[:graph:] 与[:print:]相同，但不包括空格`

`[:lower:] 任意小写字母(同[a-z])`

`[:print:] 任意可打印字符`

`[:punct:] 既不在[:alnum:]又不在[:cntrl:]中的任意字符`

`[:space:] 包括空格在内的任意空白字符(同[\\f\\n\\r\\t\\v])`

`[:upper:] 任意大写字母(同[A-Z])`

`[:xdigit:] 任意十六进制数字(同[a-fA-F0-9])`


- `*`0个或多个
- `+` 一个或多个`{1,}`
- `{n}` n个
- `{n,}` 不少于n个
- `{n,m}` n到m个
- `^` 文本开始 如果`[^0-9]`表示排除集合内数据
- `$` 文本结尾

# 创建计算字段

拼接字段`concat(column_1,'_to_',column_2)`

别名 `select column as alias_name`

执行计算 `select quantity*price as total` 可以使用`= - * /`

# 使用数据处理函数

常用文本处理函数

- `Left()` 返回串左边的字符 
- `Length()` 返回串的长度 
- `Locate()` 找出串的一个子串 
- `Lower()` 将串转换为小写 
- `LTrim()` 去掉串左边的空格 
- `Right()` 返回串右边的字符
- `RTrim()` 去掉串右边的空格 
- `Soundex()` 返回串的SOUNDEX值 
- `SubString()` 返回子串的字符 
- `Upper()` 将串转换为大写

日期

- `AddDate()`     增加一个日期(天、周等)
- `AddTime()`     增加一个时间(时、分等)
- `CurDate()`     返回当前日期
- `CurTime()`     返回当前时间
- `Date()`     返回日期时间的日期部分
- `DateDiff()`     计算两个日期之差
- `Date_Add()`     高度灵活的日期运算函数
- `Date_Format()`     返回一个格式化的日期或时间串
- `Day()`     返回一个日期的天数部分
- `DayOfWeek()`     对于一个日期，返回对应的星期几
- `Hour()`     返回一个时间的小时部分
- `Minute()`     返回一个时间的分钟部分
- `Month()`     返回一个日期的月份部分
- `Now()`     返回当前日期和时间
- `Second()`     返回一个时间的秒部分
- `Time()`     返回一个日期时间的时间部分
- `Year()`     返回一个日期的年份部分

数值
- `Abs()` 返回一个数的绝对值 
- `Cos()` 返回一个角度的余弦 
- `Exp()` 返回一个数的指数值 
- `Mod()` 返回除操作的余数 
- `Pi()` 返回圆周率
- `Rand()` 返回一个随机数 
- `Sin()` 返回一个角度的正弦 
- `Sqrt()` 返回一个数的平方根 
- `Tan()` 返回一个角度的正切

# 汇总数据

聚集函数

- `AVG()` 返回某列的平均值 
- `COUNT()` 返回某列的行数 count会忽略null
- `MAX()` 返回某列的最大值 
- `MIN()` 返回某列的最小值 
- `SUM()` 返回某列值之和

聚集不同的值

`select avg(distinct price)`

组合聚集函数

`select count(*) as total,avg(price),avg(quantity)`

# 分组数据

`group by`会在聚集函数之前执行  `select pro_id,price from prod group by pro_id,price`

`having`对聚集后的结果再次过滤

`group by`使用`order by`明确规定按照哪一列排序比较规范

# 子查询

## **作为计算字段使用子查询**

```sql
select  cust_name,
        cust_state,
        (
            select count(*) from orders where order.cust_id=customers.cust_id
        ) as orders 
from customers
group by cust_name
;-- -输出---
;cust_name | cust_state | orders
;name1 | MI | 2
```
**orders是一个计算字段,它是由圆括号的子查询建立的,对每个检索出的客户进行一次计算**

# 联结表

联结就是在笛卡尔积上做了限制条件,最常用的是等值联结,也叫内部联结

```
select vend_name,prod_name,prod_price 
from venders inner join products ;这里可以直接写成 from venders,products 
where venders.vender_id = products.vender_id;
```
联结多个表
```
select vend_name,prod_name,prod_price,quantity
from venders,products,orderitems
where venders.vender_id = products.vender_id 
and orderitems.prod_id=products.prod_id
and orderitems.order_num=2005
```

# 创建高级联结

`from table1 as t1,table2 as t2` 给表定义别名

## 使用不同类型的联结

联结除了内部联结(等值联结),还有外部联结,自然联结,自联结

自联结其实是对同一张表进行操作,对同一张表进行子查询通常可以转化为自联结

```
select p1.prod_name,p2.prod_id 
from products as p1,products as p2
where p1.vend_id=p2.vend_id
and p2.prod_id='dtntr'

; 相同于

select prod_name,prod_id 
from products
where vend_id in (select vender_id from products where prod_id='dtntr')
```

自然联结的返回表,列是去重的,通常内部联结都是自然联结，很可能我们永远都不会用到不是自然联结的内部联结。

## 外部联结(OUTER JOIN)

外部联结必须加上left或者right.left表示外部联结左边表(右边表没有数据则为null)

```
select customers.cust_id,orders.order_num
from customers left outer join orders
on customers.cust_id=orders.cust_id
+---------+-----------+
| cust_id | order_num |
+---------+-----------+
| 10001   | 20005     |
| 10001   | 20009     |
| 10002   | <null>    |
| 10003   | 20006     |
| 10004   | 20007     |
| 10005   | 20008     |
+---------+-----------+
```

## 使用带聚集函数的联结

```
select customers.cust_name,customers.cust_id,
        count(orders.order_num) as num_ord
from customers,orders
where customers.cust_id=orders.cust_id
group by cust_id
+----------------+---------+---------+
| cust_name      | cust_id | num_ord |
+----------------+---------+---------+
| Coyote Inc.    | 10001   | 2       |
| Wascals        | 10003   | 1       |
| Yosemite Place | 10004   | 1       |
| E Fudd         | 10005   | 1       |
+----------------+---------+---------+
```

```
select customers.cust_name,customers.cust_id,
        count(orders.order_num) as num_ord
from customers left outer join orders
on customers.cust_id=orders.cust_id
group by cust_id
+----------------+---------+---------+
| cust_name      | cust_id | num_ord |
+----------------+---------+---------+
| Coyote Inc.    | 10001   | 2       |
| Mouse House    | 10002   | 0       |
| Wascals        | 10003   | 1       |
| Yosemite Place | 10004   | 1       |
| E Fudd         | 10005   | 1       |
+----------------+---------+---------+
```

# 组合查询

UNION,union会把两个结果集中重复的行去除掉,使用 `UNION ALL`来避免

UNION语句只允许一条ORDER BY,并且只能跟在最后一个select语句后面

# 全文本搜索

Mysql支持多种数据库引擎,常见的MyISAM支持全文搜索,但是InnoDB不支持

**为了进行全文搜索,被搜索的列必须尽力索引,而且要随着数据的改变不断地重新索引**,建立索引后select可与match(),against()一起使用执行实际的搜索

## 启用全文本搜索支持
必须使用FULLTEXT声明
```
CREATE TABLE productnotes
(
  note_id    int           NOT NULL AUTO_INCREMENT,
  prod_id    char(10)      NOT NULL,
  note_date datetime       NOT NULL,
  note_text  text          NULL ,
  PRIMARY KEY(note_id),
  FULLTEXT(note_text)
) ENGINE=MyISAM;
<!-- show create table productnotes -->
CREATE TABLE `productnotes` (                            
  `note_id` int(11) NOT NULL AUTO_INCREMENT,             
  `prod_id` char(10) NOT NULL,                           
  `note_date` datetime NOT NULL,                         
  `note_text` text,                                      
  PRIMARY KEY (`note_id`),                               
  FULLTEXT KEY `note_text` (`note_text`)                 
) ENGINE=MyISAM AUTO_INCREMENT=115 DEFAULT CHARSET=latin1
```

## 进行全文本搜索

match指定被搜索的列,against指定使用的搜索表达式
```
select note_text
from productnotes
where Match(note_text) against('rabbit')

+----------------------------------------------------------------------------------------------+
| note_text                                                                                    |
+----------------------------------------------------------------------------------------------+
| Customer complaint: rabbit has been able to detect trap, food apparently less effective now. |
| Quantity varies, sold by the sack load.                                                      |
| All guaranteed to be bright and orange, and suitable for use as rabbit bait.                 |
+----------------------------------------------------------------------------------------------+
```
全文本搜索的一个重要部分就是对结果排序。具有较高等级的行先返回.

```
select note_text,Match(note_text) against('rabbit') as rank
from productnotes
order by rank desc
```
不包含rabbit的行rank为0,都包含,那么rabbit靠前的行rank要高

## 扩展查询

```
select note_text
from productnotes
where Match(note_text) against('rabbit' with query expansion)
```

## 布尔文本搜索

MySQL支持全文本搜索的另外一种形式，称为布尔方式,以布尔方式，可以提供关于如下内容的细节:

- 要匹配的词;
- 要排斥的词(如果某行包含这个词，则不返回该行，即使它包含其他指定的词也是如此);
- 排列提示(指定某些词比其他词更重要，更重要的词等级更高); 
- 表达式分组;
- 另外一些内容。

```
select note_text
from productnotes
where Match(note_text) against('rabbit' in bool mode)
```

全文布尔操作符

- `+`  包含，词必须存在 例如('+rabbit +rope')
- `-`  排除，词必须不出现 例如against('rabbit -`rope*`' in bool mode)排除`rope*`的词
- `>`  包含，而且增加等级值
- `<` 包含，且减少等级值 
- `()` 把词组成子表达式(允许这些子表达式作为一个组被包含、排除、排列等)
- `~` 取消一个词的排序值
- `*`  词尾的通配符
- `""` 定义一个短语(与单个词的列表不一样，它匹配整个短语以便包含或排除这个短语)

# 插入数据

insert into table_name(column,..) values (),(),...;

insert into table_name(column,...) select ...;

# 创建操纵表

# 试图

视图简化复杂的联结,每次检索视图,实际还是执行了一次查询,性能可能有问题

# 存储过程

把复杂的操作组织起来,简单,安全,高性能

优点:
- 开发人员调用统一接口,保证了完整性,防止出错
- 提高性能,比执行多条sql要快

一般只有数据库管理员才有创建存储过程的权限

## 使用存储过程

`CALL func_name(params)`

```sql
delimiter //
create procedure productpricing()
begin
    select avg(prod_price) as priceaverage
    from products;
end //
delimiter ;
drop procedure productpricing;
```

## 使用参数

参数`In|Out|InOut var_name type` In表示传递给存储过程,Out表示从存储过程传出,InOut传入传出
```
create procedure productpricing(
    OUT pl Decimal(8,2),
    OUT ph Decimal(8,2),
    OUT pa Decimal(8,2)
)
begin
    select min(prod_price)
    INTO pl
    from products;
    select max(prod_price)
    INTO ph
    from products;
    select avg(prod_price)
    INTO pa
    from products;
end;
;这里接收三个参数pl,ph,pa
```
调用`call productpricing(@pricelow,@pricehigh,@priceaverage);select @pricelow` **变量必须使用@**

```sql
create procedure ordertotal(
    IN onumber INT,
    OUT ototal Decimal(8,2)
)
begin 
    select sum(item_price*quantity) 
    from orderitems
    where order_num=onumber
    INTO ototal;
end;
```

# 使用游标

MYSQL游标只能用于存储过程

使用游标前必须声明,然后打开,然后关闭
```
create procedure processorder()
begin
    declare o INT;
    declare done boolean default 0;
    declare ordernumbers CURSOR
    FOR
    select order_num from orders;
    
    declare continue handler for sqlstate '02000' set done=1;

    open ordernumbers;

        repeat
            fetch ordernumbers into o;
        until done end repeat;

    close ordernumbers;
end;
```
上面直到done为真是退出循环,done只有在sqlstate为02000时变成真,02000是一个未找到条件

# 触发器

mysql触发器只响应insert update delete;只有表支持触发器,视图不支持

## 编写触发器

- 名称
- 关联的表
- 响应的动作
- 何时执行(之前或之后)

```
create trigger newproduct after insert on products
for each row select 'product added';
```

**每张表最多6个触发器,delete,insert,update,之前|之后**

**如果before执行失败,那么sql语句不会执行;如果before或sql失败after也不执行**

## INSERT触发器

- insert触发器代码内,可以引用一个名为new的虚拟表访问被插入的行
- before insert可以修改new的值,来改变被插入的值
- 对auto_increment,new在insert执行之前包含0,在insert执行之后包含自动生成的值

## DELETE触发器

- delete 触发器内,可以引用old表,访问被删除的行
- old的数据是只读的

可以把old数据保存到另外的表中
```
create trigger deleteorder before delete on orders
for each row 
begin
    insert into archive_orders(order_num,order_date,cust_id)
    values(old.order_num,order_date,cust_id);
end;
```

## UPDATE 触发器

- update触发器内,可以用old访问以前的数据,new访问更新的值
- before update内可以修改new的值
- old值全部只读

# 事务处理

InnoDB支持事务

## 控制事务

默认mysql是commit的,但是在事务内部必须手动commit,rollback会退到指定的位置

start transaction
savepoint p1
roolback to p1
commit

commit之后事务将会关闭,mysql回到自动commit状态


























    






