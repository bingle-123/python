# Python Web开发Django-03

## 课程内容

### ORM补充

- 关联数据的读取
    - 主表读取从表
    - 从表读取主表

### 模板引擎

- 模板引擎原理
- 实现一个简单的模板引擎
- 如何使用django自带的模板引擎
- django模板引擎调用过程

### 模板引擎语法

- 模板构成
- 注释
- 变量打印
- 条件判断
- 循环
- 乘除法
- 转义
- 过滤标签
- 静态资源 
- 继承与block
- 包含

## ORM补充

### 一对一

主--->从   
`mobj.字段名` 例如:`student.desktop`读取的是DeskTop对象

从--->主  
`sojb-->主类名小写` 例如: `desktop.student` 读取的是Student对象

### 多对一

主-->从  
`mobj.字段名` 例如:`student.classroom`读取的是一个ClassRoom对象

从-->主  
`sobj-->主类名小写__set.过滤函数` 例如:`classroom1.student_set.all()`

### 多对多

主-->从  
`mobj.字段名.过滤函数` 例如:`author.book.all()`读取的是一个数据集合对象

从-->主  
`sobj-->主类名小写__set.过滤函数` 例如:`book.author_set.all()`

## 模板引擎

### 模板引擎原理

模板包含两个部分:静态数据+动态数据

构建特殊的文件,文件内容包含特殊的字符,使用处理函数将特殊字符替换成其他数据

### 使用函数实现字符串替换

```python
s='''用户名:name;年龄:age'''
def render(name,age):
    result = s.replace('name',str(name)).replace('age',str(age))
    return result
```

### 如何使用django自带的模板

django自带的模板引擎执行流程:加载模板,导入参数,模板渲染

**模板引擎配置**

**函数中调用模板引擎**

## 模板语法

网页模板包含两个部分:网页原始内容+模板语法

### 注释

网页原始注释: `<!-- 网页注释 -->`

单行注释: `{# 注释内容 #}`

多行注释: `{% comment %} 注释内容 {% endcomment %} `

### 变量打印

`{{变量名}}`

### 条件判断

```
{% if xxx %}
{% elif xxx %}
{% else %}
{% endif %}

{% ifequal a b %}
{% endifequal%}

{% ifnotequal a b %}
{% endifnotequal%}

```

### 循环

```
{% for item in items %}
{% endfor %}

{% for item in items %}
{% empty %} 
{% endfor %}

```

### 乘除法

django模板引擎不能够直接使用变量的相乘以及相除

{% widthratio 数值变量 分母 分子 %} 

### 转义

{% autoescape off|on %}

{% endautoescape %}

### 过滤标签

- safe:不对变量数据进行转义
- join:把元素连接起来,相当于 `''.join(var)`
- length:获取变量的长度 相当于 `len(var)`

### 静态资源

配置django静态文件夹路径  
`STATICFILES_DIRS`=[os.path.join(BASE_DIR,'static_path')]

模板中使用`{% load static %}` `{% static 资源位置 %}`

### 继承
`{% extends 父模板名称 %}`  

`{% block block_name %} {% endblock %}`

### 包含

`{% include 模板名称 %}`



