## MySQL中的运算符

- = : 等于
- <>或!= : 不等于
- <=> : NULL安全的等于
- < : 小于
- <= : 小于等于
- \> : 大于conbgf

- \>= : 大于等于

- between : 存在于指定的范围

- in : 存在于指定集合

- is null : 为null

- is not null : 不是null

- like : 通配符匹配

- regexp或rlike : 正则表达式匹配

- NOT 或者 ! : 逻辑非

- AND 或者 && : 逻辑与

- OR 或者 || : 逻辑或

- XOR : 逻辑异或


## 数据库

> 查看已有数据库`show databases`<br>
> 创建数据库`create database db_name`<br>
> 使用数据库`use db_name`<br>
> 查看数据库下有哪些表`show tables`<br>
> 删除数据库`drop database dbname`

## 表

> 创建表<br>
> `create table table_name （column_name data_type constrains, ..., constrains`<br>
> 查看表定义`descibe|desc table_name`<br>
> 删除表`drop table table_name`<br>
> 修改字段<br>
> `alter table table_name modify [column] column_definition [first|after column]`例如：`alter table t1 modify name varchar(32)`<br>
> 增加字段<br>
> `alter table table_name add [column] column_definition [first|after column_name]`例如`alter table t1 add column new_name varchar(32)`<br>
> 删除字段<br>
> `alter table table_name drop [column] column_name`例如`alter table t1 drop column tmp_age`<br>
> 修改字段名<br>
> `alter table change [column] old_name column_definition [first|after column_name]`例如：`alter table change column name name_change varchar(64)`<br>
> 修改表名 `alter table table_name rename new_table_name`

### DML

主要insert、update、delete、select

## 插入记录

```
insert into table_name [(field1,field2,field3,fieldn)]
values (value1,value2,value3,valuen),
(value1,value2,value3,valuen),
```

## 更新记录

```
update table_name set field1=value1,field2=value2 [where condition]
更新两个表
update table1 table_alias,table2 table2_alias set a.sal=a.sal*b.deptno,b.deptname=a.ename where a.deptno=b.deptno
```

## 删除记录

`delete from table_name [where condition]`

## 查询记录

排序`select * from table_name order by field1[desc],fild2[desc],...`

显示一部分数据`select [limit start,row_count]` start表示起始位置，默认为0，只需给出要显示的行数。

## 聚合操作

```
select [field1,field2,fieldn] fun_name
from table_name
[where condition]
[group by field1,field2,fieldn]
[with rollup]
[having condition]
group by按照指定属性分组后再进行聚合函数操作
with rollup 表明是够对分类聚合后的结果在进行汇总
having对分类后的结果再次进行条件过滤
```

## 链接

```
自然连接
select t1.field1,t2.field1 from t1,t2 where t1.field1=t2.field1
外链接
select field1,field2 from t1 left join t2 on t1.field1=t2.field1
```

## 子查询

```
select * fom t1 where t1.field1 in (select field2 from t2 where field2>100)
如果只有一条记录 可以使用=
```

## 记录联合

```
将两个表的数据查询出来后合并到一起
常用union 和 union all
union all会把两个几个并集后去除重复的元组
select field1 form table1
union|union all
select field1 from table2
```
