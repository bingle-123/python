# Python Web开发Django-01

## 课程内容

#### 一、基础知识

- C/S与B/S
- django框架
- MVC
- django的MTV

#### 二、项目构建
- 环境
- 搭建项目
- 启动服务器
- django请求流程

#### 三、项目目录结构

#### 四、自定义路由与请求处理函数

#### 作业

## 一、基础知识

### C/S与B/S

- C: Client 客户端
- B: Browser 浏览器 
- S: Server 服务器

浏览器是最常见的客户端，几乎所有平台上（安卓，Ios，Windows，MacOS，Linux，树莓派等嵌入设备）都有浏览器。

> 单机到客户端与服务器,发展历史

### HTTP

超文本传输协议（HTTP，HyperText Transfer Protocol) 是互联网上应用最为广泛的一种网络协议。互联网从传输简单问文字，网页只包含文字，到包含多媒体。  
目前使用的版本是HTTP 1.1

#### URL

统一资源定位符，用于定位网络上某个资源，通过URL可以访问到对应的网络资源。

常见格式：scheme://domain/path
- scheme：协议，例如：http、https、ftp
- domain：服务器地址，格式:`域名或者IP:端口号`。例如：127.0.0.1:8000；www.baidu.com
- path：资源路径，指明要访问的资源在服务器上的位置。例如：/images/logo.png

> 类似于电话号码，通过电话号码找到某个人，电话号码具有一定的格式

### 服务器处理请求的流程

请求-->路由-->业务处理函数-->数据库-->网页-->返回给客户端

### django框架

地址:`https://www.djangoproject.com/`

- 从2005初步完成，是开源框架
- 重量级的python Web开发框架，内置了大量的模块工具
- 使用的是MVC的设计思想

### MVC

> 分工合作：盖房子，砌墙工，和水泥，砖头供应  
> web开发中类似于盖房子，但是分为数据模型，视图，控制器  

全名是Model View Controller。是一种软件设计思想，用于将业务逻辑、数据、界面显示分离。

- model 模型：用于管理业务数据，例如：数据库的增删改查
- view 视图：用于显示业务数据
- controller 控制器：用于从视图中获取数据，以及向model中发送数据，控制数据在视图中的展示

### MVT

django使用的是MVC思想。使用MTV方式来实现MVC思想：

- M:model 数据层，用户处理数据库操作
- T:template 视图模板，用于显示数据
- V:view 控制器，用处理用户请求，返回响应数据。


## 二、项目构建

### 环境

ubuntu 16.04+python3 或者 MacOS 10+

### 安装虚拟环境

```shell
# 更新软件
sudo apt-get update

# 安装python3
sudo apt-get install python3

# 安装python3 pip
sudo apt-get install python3-pip

# 切换到home目录下
cd ~
mkdir DjangoProjects
cd DjangoProjects

# python虚拟换件管理工具
sudo pip3 install virtualenv

# 创建虚拟环境
virtualenv -p python3 .djenv

# 启动虚拟环境
source ~/DjangoProjects/.djenv/bin/activate

# 退出虚拟环境
deactivate
# 配置启动虚拟环境命令别名
vim ~/.bashrc
# 尾部添加
# alias djenv=‘source ~/home/u/DjangoProjects/.djenv/bin/activate’
```

```shell
# 启动虚拟环境
djenv
# 安装django库
pip install django==1.11

# 安装pylint-django
pip install pylint-django

# 查看已经安装的包
pip freeze

# 新建项目
django-admin startproject Django01
# 启动服务器
cd Django01
./manage.py runserver
# 打开浏览器访问 127.0.0.1:8000
```


## 四、项目目录结构

```
Django01/
    manage.py
    Django01/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```
Django01项目文件夹
- `manage.py`：所有的django项目中默认都会创建这个文件，它是django项目的命令行管理工具。
- `Django01/Django01`是一个python包，
- `Django01/Django01/__init__.py` 是一个空文件，用户指明这个文件夹是python包
- `Django01/Django01/settings.py` 项目的相关配置信息
- `Django01/Django01/urls.py` 路由配置文件
- `Django01/Django01/wsgi.py` 项目部署时用到的文件

### settings配置信息
- DEBUG：开发环境下始终为True，只有在项目部署到生产环境时改为False
- ALLOWED_HOSTS：允许被访问的主机
- INSTALLED_APPS：需要安装的应用，django中自带了了一些应用已经，创建应用后，要把应用的名称加入到这里
- ROOT_URLCONF：根路由文件
- TEMPLATES：模板引擎配置信息
- DATABASES：数据库配置信息

### Django请求流程

请求-->路由-->处理函数-->数据库操作-->渲染模板-->返回响应数据

> 类似于一家门厂。客户：想要买门。接单客服:接待客户。库房：找到对应的门。客服安排发货。

- 请求由客户端发起
- 路由负责对客户端发起的请求进行解析,找到对应的处理函数

### 新建应用

`./manage.py startapp MyApp`

```
MyApp/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```
- admin.py：django自带的后台管理工具的相关配置
- apps.py：这个应该相关配置信息
- migrations/ ：数据库迁移文件目录
- **models.py**：存放数据模型
- tests.py：测试文件
- **views.py**：视图处理函数文件

## 五、创建请求处理函数并绑定路由

### 在views新建视图处理函数

视图处理函数格式
```python
def hello_world(request):
    # 处理过程
    return HttpResponse('')
```
第一个参数必须是request，并且每一个处理函数必须返回一个HttpResponse对象

### 绑定路由

```python
from MyApp.views import hello_wolrd

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello_world$', hello_world),
]
```
路由格式:`url(正则匹配，处理函数名)`

### 浏览器中访问

`127.0.0.1:8000/hello_world`

### 子路由

> 园区-->楼-->几层
> 
> 或者一家公司，前台-->分机号-->人

```python
from django.conf.urls import include
from MyApp.views import hello_wolrd
from MyApp import urls as myapp_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hello_world/', include(myapp_urls)),
]
```

## 作业

新建一个后台管理的应用，用于管理产品，订单，用户，客服。通过后台首页进入到对应的管理页面。

使用子路由来实现。

页面：

- 后台首页
- 产品管理
- 订单管理
- 用户管理
- 客服管理




















