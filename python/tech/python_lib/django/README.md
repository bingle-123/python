# Django源码解析

django runserver 启动流程

- 执行 `./manage.py runserver` --> 调用`django.core.management`中`execute_from_command_line(sys.argv)`
    > django-admin 也是调用此方法
- 新建 `utility = ManagementUtility(argv)`
- 调用 `utility.execute()`
    - 取出 subcommand :即传递的命令参数
    - 添加默认参数
    - 检查 settings 中是否存在 INSTALLED_APPS
        > settings 使用 LazySettings 
        - 否:使用` conf.global_settings `作为默认设置
        > 默认 django 使用 `conf.__init__中`

django manage.py 命令参数在`django.core.management.commands`下.

如果需要自定义命令可以在该文件夹下,**命令名称与文件名相同**

# **init**.py

# apps

# contrib

# dispatch

# middleware

# templatetags

# utils

# **main**.py

# bin

# core

# forms

# shortcuts.py

# test

# views

# **pycache**

# conf

# db

# http

## cookie.py

调用python的http库种的cookie

## multipartparser.py

用于解析http请求类型为multipart的请求体,请求体的每一个部分都是使用bound来分割的.浏览器上传的文件也是以multipart类型上传的,所以解析客户端上传的文件也是在这里进行的.

## request.py

但请求进来时,request对象会去检查 当前请求的host是否在settings里面allowed_hosts


## response.py

# template

# urls
