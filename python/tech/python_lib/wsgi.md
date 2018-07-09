# WSGI

WSGI 的官方定义是，the Python Web Server Gateway Interface。从名字就可以看出来，这东西是一个Gateway，也就是网关。网关的作用就是在协议之间进行转换。

WSGI 是作为 Web 服务器与 Web 应用程序或应用框架之间的一种低级别的接口，以提升可移植 Web 应用开发的共同点。WSGI 是基于现存的 CGI 标准而设计的。

也就是说，WSGI就像是一座桥梁，一边连着web服务器，另一边连着用户的应用。但是呢，这个桥的功能很弱，有时候还需要别的桥来帮忙才能进行处理。

## WSGI的作用

WSGI有两方：“服务器”或“网关”一方，以及“应用程序”或“应用框架”一方。服务方调用应用方，提供环境信息，以及一个回调函数（提供给应用程序用来将消息头传递给服务器方），并接收Web内容作为返回值。

所谓的 WSGI中间件同时实现了API的两方，因此可以在WSGI服务和WSGI应用之间起调解作用：从WSGI服务器的角度来说，中间件扮演应用程序，而从应用程序的角度来说，中间件扮演服务器。

## 其他

wsgi将 web 组件分为三类： web服务器,web中间件,web应用程序;wsgi基本处理模式为 ： WSGI Server -> (WSGI Middleware)* -> WSGI Application 。


## wsgi server 基本工作流程
- 服务器创建socket，监听端口，等待客户端连接。
- 当有请求来时，服务器解析客户端信息放到环境变量environ中，并调用绑定的handler来处理请求。
- handler解析这个http请求，将请求信息例如method，path等放到environ中。
- wsgi handler再将一些服务器端信息也放到environ中，最后服务器信息，客户端信息，本次请求信息全部都保存到了环境变量environ中。
- wsgi handler 调用注册的wsgi app，并将environ和回调函数传给wsgi app
- wsgi app 将reponse header/status/body 回传给wsgi handler
- 最终handler还是通过socket将response信息塞回给客户端。

web组件被分成三类：client, server, and middleware.WSGI apps(服从该规范的应用)能够被连接起来(be stacked)处理一个request，这也就引发了中间件这个概念，中间件同时实现c端和s端的接口，c看它是上游s，s看它是下游的c。WSGI的s端所做的工作仅仅是接收请求，传给application（做处理），然后将结果response给middleware或client.除此以外的工作都交给中间件或者application来做。


WSGI里的组件分为『Server』，『Middleware』和『Application』三种，其中的『Middleware』是『设计模式』里的Decorator（装饰器）。


A WSGI server (meaning WSGI compliant) only receives the request from the client, pass it to the application and then send the response returned by the application to the client. It does nothing else,All the gory details must be supplied by the application or middleware.


# WSGI python内置库实现web服务器

```python
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return '<h1>Hello, web!</h1>'
#environ包含所有的请求信息
#start_response,用于向客户端返回信息
```