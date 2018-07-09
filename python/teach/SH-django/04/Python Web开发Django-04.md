# Python Web开发Django-04

## 课程内容

### 路由规则

- 固定位置参数
- 命名参数

### 请求与响应

- 请求
- 响应


## 路由规则

给函数传递参数常用方式:func(arg1,arg2,arg3...),func(key=value,key2=value2,key3=value3...)
### 固定位置参数

url(r'path/(\d{4})/(\d{1,2})/(\d{1,2})',view_name)

view_name(request,arg1,arg2,arg3)

### 命名参数

url(r'path/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})',view_name)

view_name(request,month,day,year)


## 请求与响应

### 请求

request是HttpRequest对象,包含用户请求的所有信息

**属性**

- GET:字典类型,包含的是url中包含的请求参数
- POST:字典类型,如果与post方式上传一个表单数据,上传的表单数据保存在request.POST中
- FILES:字典类型,如果客户端通过表单上传了文件,那么文件信息保存在request.FILES中
- method:客户端使用的请求方法
- scheme:客户端请求使用的协议
- path:客户端请求的路径
- encoding:客户端数据使用的编码
- content_type:客户端上传数据所使用的数据格式,常见:application/json; multipart/form-data;
- COOKIES:字典格式,客户端请求所带的cookie
- META:包含请求头

**方法**

- read:读取请求体
- is_ajax:判断是否是ajax
- is_secure:判断是否是使用HTTPS协议


### 响应

每一个函数的返回值必须是一个HttpResponse对象

构造函数常用参数:
- content:响应体
- content_type:响应体数据类型,例如:application/json
- status:响应的状态码
- reason:状态码说明









