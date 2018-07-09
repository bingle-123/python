# Python Web开发Django-02

## 课程内容

### 一、ORM是什么

- 数据表
- 面向对象
- 对应关系

### 二、在django中如何构建映射关系

- 构建对应的model
- 配置数据库
- 迁移数据

### 三、常用字段

- 普通字段
- 关联字段

### 四、ORM的使用

- 简单操作
- 复杂操作
    - 关联数据
    - 数据查询
    - 数据更新
    - 数据删除

### 作业


## 一、ORM是什么

ORM 对象关系映射，用于实现面向对象编程语言里不同类型系统的数据之间的转换。

数据操作请求-->ORM-->数据库(mysql,oracle,mssql,sqlite3...)

> 不同数据库语法有差别,支持的功能不同

### 数据库表

- 表名
- 字段
- 数据记录

### 面向对象

- 类名
- 属性
- 对象

### 结合起来

`类名<--->表名`

`类属性<---->表字段`

`对象<---->数据记录`

> django中通过操作类和对象来实现对数据库表以及记录的操作

## 二、在django中如何构建映射关系

构建类与数据表的对应关系：构建model类-->生成迁移文件-->执行迁移

### 构建model

在MyApp下`model.py`中新增类，继承自`django.db.models.Model`

```python
class Student(models.Model):
    pass 
```
这里的Student对应的是一张数据库表。

为Student类添加属性，对应数据表的字段

```python
class ClassRoom(models.Model):
    name= models.CharField(max_length=32)
```

数据表字段由字段名、字段类型、字段属性组成

`name`-->`字段名`、`model.CharField`-->`字段类型`、`max_length=32`-->`字段属性`

### 配置数据库

#### 安装mysql数据库

安装mysql数据库：`sudo apt-get install mysql-server`

创将数据库用户`grant all on *.* to 'django'@'%' identified by 'djangopwd';`

创建数据库 `create database django01 character set=utf8;`

#### 安装连接mysql库

- sudo apt-get install python3-dev libmysqlclient-dev
- pip install mysqlclient


#### 在settings.py中修改默认的数据库

django默认的数据库是sqlite

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django01',#数据库名
        'USER': 'django',#数据库用户名
        'PASSWORD': 'djangopwd',#数据库用户密码
        'HOST': 'localhost',#数据库地址
        "PORT": '3306'#数据库端口号
    }
}
```

### 迁移数据

```shell
# 生成迁移文件，生成的迁移文件在MyApp/migrations/下
./manage.py makemigrations MyApp
# 执行迁移
./manage.py migrate
```

## 三、字段

### 普通字段

- AutoField：自增长字段
- CharField：字符串
- IntegerField：整数
- BooleanField：布尔
- TextField：大文本
- DateField：日期
- DateTimeField：日期时间
- FloatField：浮点

### 关联字段
- ForeignKey 多对一
- ManyToManyField 多对多
- OneToOneField 一对一 是特殊的多对一关系

### 通用字段属性
- null：默认是False，数据库中该字段是否可以为null
- db_index：默认False，表示该字段是否构建索引
- primary_key：默认False，是否主键
- unique：默认False，该字段的值是否不能有重复
- default：字段的默认值
- blank：默认为False，通常使用在char或text类型上，表示是否可以存储`''`，它与null不同，null是数据库级别限制，blank是业务上的限制
- help_text：帮助说明信息
- choices: 接受一个遍历对象,对象中每一个元素是一个2位元素的元组；该字段的值只能从给出的列表中选一个，元组中第一个元素是保存到数据库中，第二个元素只是一个别名，例如：
```python
gender_choices = ( 
    ('male', '男'), 
    ('female', '女'), 
)
```
- db_cloumn:数据表字段名，默认情况下是属性名

### 关联字段属性

ForeignKey与OneToOneField：
- on_delete：
    - models.CASCADE：级联删除，当主键删除时，所有关联的数据全部删除
    - models.PROTECT：保护，当删除主键时，假如还有关联数据，那么抛出异常
    - models.SET_NULL：主键删除时，将该字段设置为null
    - models.SET_DEFAULT：设置为默认值，但是必须在定义字段是给出默认值
    - models.SET()：使用函数的返回值作为字段值
    - models.DO_NOTHING：什么都不做

## 使用ORM管理数据

每一个类都有一个默认的属性：objects，他是一个管理器

django中执行数据库操作需要通过，类的属性objects执行

### 简单操作

#### 创建数据

两种方式创建一条数据

```python
obj=ClassRoom()
obj.attr=value
obj.save()
```
创建一个类对象，对象属性赋值，执行保存

#### 数据更新

```python
obj.attr=value
obj.save()
```

更新对象属性，执行保存

#### 查询数据

ClassRoom.objects.get()

#### 删除数据

obj.delete

### 复杂操作

#### 关联关系数据创建

**一对一**

**多对一**

**多对多**

#### 数据查询

**字段特殊查询**

- `age__lt=10`: ==== `where age < 10`
- `age__lte=10`: ==== `where age <= 10`
- `age__gt=10`: ==== `where age > 10`
- `age__gte=10`: ==== `where >= 10`
- `name__contains='tom'`: ==== `where name like '%tom%'`
- `name__icontains='tom'`: ==== `where name ilike '%tom%'`
- `name__startswith='tom'`: ==== `where name like 'tom%'`
- `name__istartswith='tom'`: ==== `where name ilike 'tom%'`
- `name__endswith='tom'`: ==== `where name like '%tom'`
- `name__iendswith='tom'`: ==== `where name ilike '%tom'`
- `age__in=[20,25,28]`:  ====`where age in (20,25,28)`
- `street__isnull=True`: ==== `where steert is null`

**字段关联查询**

- `classroom__name='1801'`: ==== `WHERE blog.name='1801'`
- `classroom__name__contains='1801'`: ==== `WHERE blog.name like '%1801%'`

> 定义属性字段时,不可以使用包含`__`的名字

**Q**

命名参数查询对应到数据查询时,使用的是 `and`逻辑。如果要使用`or`和`not`，那么需要借助于`Q`

**Q实现or**

ClassRoom.objects.filter(name='1801',Q(bodys__gt=20)|Q(girls__lt=5))

**Q实现not**

ClassRoom.objects.filter(~Q(girls__lt=5))

**F**

F可以实现一条数据内部字段的比较，比如：

ClassRoom.objects.filter(girls__gt=F('boys'))

**聚合查询**
- 平均值 Avg
- 最大值 Max
- 最小值 Min
- 数量 Count
Student.objects.aggregate(Avg('age'))

#### 更新多条数据

ClassRoom.objects.filter(...).update(...)

#### 删除多条数据

ClassRoom.objects.filter(...).delete()


## 作业

构建表

学校,教师,教室,学生,课程

图书馆,图书,作者,借阅记录






