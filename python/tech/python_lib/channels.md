# Channels

channels 使得 Django 能够用来处理除了 http 之外的其他协议,*(传统的 http 协议request/response)*,例如: Websocket 和 HTTP2.

##  第一章

Channels 的五个依赖包

- Channels:Django 的注入层
- Daphne: HTTP 和 Websocket 接口服务器 
- asgiref: 基础 ASGI 库,保存在内存中
- asgi_redis: Redis 信道 
- asgi_rabbitmq:RabbitMQ 信道
- asgi_ipc: POSIX IPC 信道

## 第二章

### Channels 是什么

Channels 在 Django 中添加新的一层,支持两个重要特性:

- WebSocket处理器, 以类似于 view 的方式
- 后台任务,在同一个服务器下,作为 Django 的一部分

### 实现方式

Channels 将 Django 分成两个类型的进程

- 处理 HTTP 和 WebSockets
- 执行 views,websocket处理器以及后台任务(consumers)

他们通过 ASGI 协议通信, ASGI 类似于 WSGI, 运行在网络之上,并且支持更多的协议

Channels 不会将asyncio, gevent或者其他异步代码引入到 django 代码中.所有的业务逻辑以同步方式运行在 worker 进行或者线程中.

### 是否需要更改 Django 的运行方式

所有的东西都是可选的,如果你愿意,可以把 Django 的 WSGI 方式改为以下方式:

- 一个 ASGI 服务器,例如 Daphne
- Django worker 服务器,使用`mangge.py runworker`
- 可以将 ASGI 请求进行路由的东西,例如 Redis

即使运行的是 Channels, 他也会默认把所有的 HTTP 请求路由到 Django View系统

### Channels 带来了什么

额外的特性包括:

- 使得支持上千的 HTTP 长连接变得简单
- 向Wedsocket 提供支持完整的 session 和 auth 支持
- 为 Websocket 提供用户自动登录支持,他通过基础的网站 cookie
- 内置了有事件触发的复杂触发事件(聊天,实时博客等等)
- 对于 URL 提供了低层次 HTTP 控制
- 对于其他协议或者事件资源提供可扩展性(例如 WebRTC,原始 UDP,SMS)

### 是否可扩展

可以运行任何数量`协议服务器`(例如, HTTP 和 WebScoket) 和 `worker服务器`(运行 Django的代码)

ASGI 允许在这两个组件之间多个不同的信道层.他被设计用来支持快速简便的切分,就像使用分布式集群运行他们自己的协议和 worker 服务器

### 为什么不适用消息队列

Channels 被设计用来实现低延迟(目标是几毫秒),并且在保证传输的下高吞吐量.这个特性有些消息队列不支持.

一些特性例如, `guaranteed ordering of messages`,are opt-in as they incur a performance hit, 但使得他更像消息队列.

### Channels 概念

Django 的传统 view 处理请求和响应,当请求到来时, Django 被启动对请求服务,生成响应发送回去,然后 Django 离开并等待下一个链接.

对于由单个浏览器交互完全可以,但是现代 Web 包含 WebSocket 和 HTTP2 协议,服务器需要在传统的循环之外与web客户端交互

他将 Django 变成了`事件驱动`,而不是只是对请求响应. Django 对 channel 上的一个大的事件集合做出响应.这里仍然没有`保持状态` .当调用任何一个事件处理器,或者 comsumer 时,他们是被独立调用的,就像调用 view 一样.

### 什么是 channel

系统的核心是 channel,不出意外的是 channel 是一个数据结构.chnnel 是一个有序的,先进先出队列.`with message expiry and at-most-once delivery to only one listener at a time`.

可以理解为一个任务队列,消息由生产者放入到channel 中,然后只发送给坚挺当前 channel 的所有消费者中的一个.

**at-most-once**意思是要么一个消费者受到消息,要么任何人得不到消息(例如: channel 执行崩溃了)另一个意思是`at-least-once`,当一个 comsumer 得到消息后,但是处理时 crash 了,那么就会发送给布置一个 channel.

还有两个其他的限制:消息必须是可序列化的,并且由大小限制.

channel具有容纳能力,没有 consumer 时许多生产者也可以向 channel 中写消息,当有消费者在其后到来时,开始服务.

Django 的 channels 和 Go 中的 channels 类似,不同的是, Django 中的 channels 是网络透明的.网络中 consumer 和 producer 可以在任何地方访问 Channels, 即使是不同的进程,不同机器.

在网络中,我们通过 name 来唯一定义 Channels, 你可以从任何链接到同一个 channel backend 的地方向任何被命名的channels 发送消息.如果不同的机器都向 `http.request` channel 写数据,那么他们写入的是同一个 channel.

### 如何使用 channels

写一个函数来 consume 一个 channel.

```python
def my_consumer(message):
    pass
```
然后将 channel 绑定到一 channel 路由上.

这意味着,这个 channel 上的每一条消息, Djando 都会调用那个 consumer, 并把消息对象传递给他(消息有一个content 属性, content 是一个字典对象,channel 属性,表示消息从哪来)

Channels 使得 Django 以 worker 模式运行,他会监听所有的绑定了 consumer的 channel. 当一个消息到来时,他会启动对应的consumer.所以 Django 不再只是运行一个绑定到 WSGI 服务器的进程,而是运行在三个分离的层级中:

1. 接口服务器:在 Django 和外面的世界之间通信.他包括一个 WSGI 适配器,和 WebSocket 服务器一样

2. channel backend:他是一个链接,把可插入的 python 代码,一个负责发送消息的数据库(例如redis, 共享内存),链接起来. 

3. workers,他们监听所有相关的 channel, 并且 当消息准备好时启动 consumer 代码

view 接收一个 request 并且返回一个 response.consumer 接收一条消息,并且能够向许多 channel 消息

为request 创建一个 channel (`http.request`).为每一个客户创建一个 response channel(例如`http.response.o4F2h2FD`),response channel 是来自 request 消息的reply_channel 属性.view 几乎是另一个 consumer 例子

```python
# 监听 http.request 
def my_consumer(message):
    # 将 request 从 message 格式转为 Request 对象
    django_request = AsgiRequest(message)
    django_response=view(django_request)
    for chunk in AsgiHandler.encode_response(django_response):
        message.reply_channel.send(chunk)
```

事实上,这就是 Channels 的工作方式.接口服务器将从外面进来的连接(HTTP,Websocket)发送到 channel 中的消息中,然后你写出 workers 来处理这些消息.通常你不需要处理 HTTP, 系统通过内置了 consumers 将他绑定到 view/template 系统中,但是你可以重写他来添加一些功能

但是,关键的部分是你可以运行代码（因此可以在通道上发送）来响应任何事件,包括自己创建的代码.可以在模型保存,其他传入消息或视图和表单内的代码路径中触发.这种方法可用于`push-style`代码,你可以使用WebSockets或HTTP长时间轮询来实时通知客户变更（聊天中的消息,或者另一个用户编辑某个内容时,在管理中的实时更新）

### channel 类型


这个模型实际上有两个主要用途.第一个也是比较明显的一个是向consumer派遣工作 - 一个消息被添加到一个channel中,然后任何一个worker可以接收并运行消费者.

然而,第二种渠道用于回复.值得注意的是,这些只有一个东西在他们上面 - 接口服务器.每个回复通道被单独命名,并且必须被路由回到客户端被终止的接口服务器.

这并不是巨大的差异 - 它们仍然依照channel的核心定义来表现 - 但是当我们想扩大规模时,会出现一些问题.我们可以高兴地在channel服务器和worker群集之间随机均衡正常channel - 毕竟任何worker都可以处理消息 - 但是响应channel必须将他们的消息发送到正在监听的channel服务器

因此,channel会将其视为两种不同的类型,并通过让channel名称包含字符来`!`表示回复频道- 例如http.response!f5G3fE21f.正常channel不包含它,但是它们只能包含字符`a-z A-Z 0-9 _ -`,并且只能包含200个字符.

Channels 被看成两种不同的 channel 类型. reply channel 包含一个`!`,例如`http.response!f5G3fE21f`,普通 channel 不包含`!`,但是必须只包含,并且必须小于200个字符.

### Groups

因为 channels 只发送到一个监听者,他们不能进行广播.Groups 可以向组内所有 client 发送消息.

例如:你可以将一些客户的 reply channel,保存在 redis 中,然后分别发送消息:

```python
redis_conn=redis.Redis('localhost',6379)
@receiver(post_save,sender=BlogUpdate)
def send_update(sender, instance, **kwargs):
    # Loop through all reply channels and send the update
    for reply_channel in redis_conn.smembers("readers"): 
        Channel(reply_channel).send({
                    "text": json.dumps({
                        "id": instance.id,
                        "content": instance.content
            })
        })
# Connected to websocket.connect
def ws_connect(message):
    # Add to reader set
    redis_conn.sadd("readers", message.reply_channel.name()

# Connected to websocket.disconnect
def ws_disconnect(message):
    # Remove from reader group on clean disconnect 
    Group("liveblog").discard(message.reply_channel)
```

虽然这样会起作用,但是存在一个小问题 - 当断开连接时,我们不会将用户从读者设置中移除.我们可以添加一个监听websocket.disconnect的消费者,但是我们还需要有使用`到期时间`,以防在接口服务器被迫退出或断电之前发送断开信号 - 否则代码将永远不会看到任何断开连接通知,回复通道是完全无效的,并且发送到那里的消息将一直在那里,直到它们过期.

由于channel的基本设计是无状态的.channel服务器是没有"关闭"channel的概念,即使接口服务器消失 - 毕竟,channel意味着保持消息直到消费者到来

我们并不特别关心断开连接的客户端没有获得发送到该组的消息 - 毕竟它已断开连接

#### 使用 Groups 可以轻松的做到,添加,发送,移除

```python
@receiver(post_save, sender=BlogUpdate)
def send_update(sender, instance, **kwargs):
    Group("liveblog").send({
        "text": json.dumps({
            "id": instance.id,
            "content": instance.content
        })
})
# Connected to websocket.connect
def ws_connect(message):
    # Add to reader group 
    Group("liveblog").add(message.reply_channel) 
    # Accept the connection request 
    message.reply_channel.send({"accept": True})

# Connected to websocket.disconnect
def ws_disconnect(message):
    # Remove from reader group on clean disconnect 
    Group("liveblog").discard(message.reply_channel)
```

Groups不仅具有 send 方法,他们还自动管理组内成员的`过期时间`.当 channel 中开始有消息因为没被消费而过期时,我们会将他从所在的所有的组中移除.当然,你仍然可以在 disconnect 时,从 groups 中移除一些东西.`过期`代码是为了在无法获取 disconnect 消息情况.

Groups 通常只在 reply channel 中可用(channel 名称中包含`!`),但是你也可以把他们当做普通 channel 来使用

### 下一步

Channel 不保证传递.如果你需要确保任务完成,使用一些包含重做和持久性设计的系统(例如: Celery).或者使用管理器来检查是否完成,并且重新发送消息

### 安装

```
pip install channels

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
...
    'channels',
)
```

### 开始

#### 第一个 consumers

如果你第一次启动 Django, 他会被设置在默认的 channel 层中:所有的 HTTP 请求(在`http.request` channel)被路由到 Django 的 view 层,他和 WSGI 没有什么不同

我们来写一个处理 HTTP 请求的处理器

```python
from django.http import HttpResponse  
from channels.handler import AsgiHandler
def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path']) 
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
            message.reply_channel.send(chunk)
```

重要:因为消息必须可以按照 JSON 来格式化,所有 request 和 response 必须是 `key-value` 格式. ASGIRequest 将 ASGI 转为 Django 请求对象, AsgiHandler 将 HttpResponse 转为 ASGI 消息.

下面一个要做的是,告诉 Django, 这个 consumer 需要被绑定到`http.request`channel 上,而不是默认的 Django view 系统.在 settings 文件中设定我们的默认 channel 层以及他的路由设置

```python
# In settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "myproject.routing.channel_routing",
    },
}
# In routing.py
from channels.routing import route channel_routing = [
    route("http.request", "myapp.consumers.http_consumer"),
]
```

这有有点像 Django 的数据库设置,他们是被命名的 channel 层,上面定义了一个`default`名称的 channel 层,他使用内存层.每一个层都可能会有一些额外的配置选项

启动`manage.py runserver`可以看到`Hello world ,...`,因为上面所有的请求消息都发送给了`http_consumer`,

我们来写 Websocket 消息的 consumer

```python
# In consumers.py
def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types # both have a "text" key for their textual data. 
    message.reply_channel.send({
            "text": message.content['text'],
        })

# In routing.py
from channels.routing import route from myapp.consumers import ws_message
channel_routing = [
    route("websocket.receive", ws_message),
]
```
上面绑定了`websocket.receive`,每当有 Websocket 消息进来时就会调用`ws_message`,然后他使用`message.reply_channel.send`返回响应消息

### Groups

把我们的 echo 服务器变成一个真正的聊天服务器.这里我们使用 Groups

我们会在`websocket.connect`和`websocket.disconnect`时添加,移除用户 channel

```python
# In consumers.py
from channels import Group
# Connected to websocket.connect
def ws_add(message):
    # Accept the incoming connection 
    message.reply_channel.send({"accept": True}) # Add them to the chat group 
    Group("chat").add(message.reply_channel)

# Connected to websocket.disconnect
def ws_disconnect(message): 
    Group("chat").discard(message.reply_channel)
```
> 如果你重写了 connect,你需要通过发送`accept: True`来明确的指明接收 Websocket 链接,你也可以在他们打开之前发送`close: True` 来拒绝链接  
> 当 channel 中有消息过期时 group 中的 channel 会过期,(每一个 channel 层都有过期时间,同在时30秒到几分钟内,并且他们是可配置的),但是 disconnect 处理会在任何时候都可以被调用  

>NOTE: channel 中总可能会有一些消息丢失,channel 被设计接收失败,所有有消息丢失时,系统不会崩溃  
> 我们推荐你讲应用设计为这种方式,而不是100%保证消息被发送,然后捕捉异常,并重新执行业务逻辑.

现在,我们来修改一下 Webscoket 代码

```python
# In consumers.py
from channels import Group

# Connected to websocket.connect
def ws_add(message):
    # Accept the connection 
    message.reply_channel.send({"accept": True}) 
    # Add to the chat group 
    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message): 
    Group("chat").send({ "text": "[user] %s" % message.content['text'], })

# Connected to websocket.disconnect
def ws_disconnect(message): 
    Group("chat").discard(message.reply_channel

# In routing.py
from channels.routing import route
from myapp.consumers import ws_add, ws_message, ws_disconnect
channel_routing = [
    route("websocket.connect", ws_add),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
```

上面的路由配置中,我们移除了 `http.request`,这样 Django 会自动讲 http 请求路由到 view 系统中

### 使用 Channels 来启动

因为 Channels 把 Django 分为多进程模式,你不再需要把所有东西运行在一个 WSGI 服务器中.相反,你启动一个或多个`接口服务器`,和一个或多个`worker 服务器`,并使用之前配置的channel层连接.

有许多类型的`接口服务器`,并且每一个都会服务不同类型的请求,例如:有的可能同时服务于 Websocket 和 HTTP, 有的可能服务于 SMS 消息网关

这些与Django将运行实际逻辑的"worker服务器"是分开的,因此channel层可以跨网络传输channel的内容.在生产场景中,你通常需要把`worker 服务器`的集群与`接口服务器`的集群分离,尽管你可以在一台机器上使用不同的进程来同时运行他们.

默认情况下, Django 没有配置 channel 层,执行 WSGI 请求时不需要他.但是当你尝试添加 consumers, 就需要了

在上面的例子中,我们使用内存中通道层实现作为默认channel层.这只是将所有的channel数据存储在内存中,所以实际上并不是交叉进程;它仅在runserver内部运行,因为它在同一进程内的不同线程中运行接口和worker服务器.当你发布生产版本时,需要使用例如 Redis bakend asgi_redis,他们可以跨进程运行.

第二件事,一旦我们在设置了网络的 channel backend时,就确保了运行的接口服务器能够进行Websocket服务.解决这个问题,使用`daphne`,他是接口服务器,可以同时处理 HTTP 和 Websocket, 然后当你运行`runserver`时,自动绑定他们进来.尽管有一些选项可能有点不同,但是你应该不会发觉到任何不同.

> runserver 现在在一个线程中运行Daphne,另一个线程中运行worker(with autorelaod) 这是最小版本的发布,所有都在一个进程中

使用 asgi_redis

```python
sudo apt-get install redis-server
pip install asgi_redis
# In settings.py
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
        "ROUTING": "myproject.routing.channel_routing",
    },
}
```

使用 runserver 来启动,他会和之前一样.你也可以尝试跨进程,使用两个命令:
- `manage.py runserver --noworker`
- `manage.py runworker`

这会禁用掉在worker线程,并且在独立的进程中处理他.你可以受用`runworker -v 2`来打印日志

如果 Django 在 DEBUG=True 下运行,那么 runworker 还会服务静态文件,DEBUG=False 静态文件服务会被关闭

### 数据持久化

echo 消息是一个简单的例子,但是他忽略的实际的系统需求,例如链接的状态保持.考虑一下基础的聊天网站,一个用户在链接初始化请求一个聊天室,作为URL路径的一部分,(`wss://host/rooms/room-name`)

`reply_channel`是对打开着的Websocket是唯一指针,因为不同的客户之间是不同的,所以我们要跟踪消息来自谁.记住, Channel 是网络透明的并且可运行在多个 worker上,所以你不能把数据保存在本地的全局变量或其他本地变量中

相反,解决方案是在其他地方存储`reply_channel` 的key信息,有点熟悉吧这就是Django的session框架为HTTP请求而使用的cookie作为key.所以如果我们可以使用reply_channel作为key来获得session, 将会很有用.

Channels 提供了`channel_session`装饰器,从而`message.channel_session`可以获得 session

我们来建立一个聊天服务器,客户通过 Websocket 的 path 提供房间名称,通过 query 字符串来提供客户名

```python
# In consumers.py
from channels import Group
from channels.sessions import channel_session from urllib.parse import parse_qs

# Connected to websocket.connect
@channel_session
def ws_connect(message, room_name):
    # Accept connection 
    message.reply_channel.send({"accept": True}) 
    # Parse the query string
    params = parse_qs(message.content["query_string"]) 
    if "username" in params:
        # Set the username in the session
        message.channel_session["username"] = params["username"] 
        # Add the user to the room_name group
        Group("chat-%s" % room_name).add(message.reply_channel)
    else:
        # Close the connection. 
        message.reply_channel.send({"close": True})

# Connected to websocket.receive
@channel_session
def ws_message(message, room_name): 
    Group("chat-%s" % room_name).send({
        "text": message["text"],
        "username": message.channel_session["username"]
    })
# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message, room_name):
    Group("chat-%s" % room_name).discard(message.reply_channel)

# in routing.py
from channels.routing import route
from myapp.consumers import ws_connect, ws_message, ws_disconnect
channel_routing = [
    route("websocket.connect", ws_connect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.receive", ws_message, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", ws_disconnect, path=r"^/(?P<room_name>[a-zA-Z0-9_,!]+)/$"),
]
```

### 鉴权

现在,当然,WebSocket解决方案的范围有限,没有能力与你的网站的其余部分一起使用,通常我们希望知道正在和哪一个用户通信,假设我们需要一个私有聊天 channel

这还能避免去问客户他们想要看到什么,如果我看到你打开了链接到我的`updates`上的Websocket,然后我只你是哪一个用户,我可以把你添加到相关的 groups 中

因为 Websocket 使用了基础的 HTTP 协议,他们有许多相似之处,包括 path,GET 请求参数, cookie. 我们想使用这些来钩住熟悉的Django会话和认证系统;毕竟,除非我们可以确定websocket属于谁,并做安全的事情,否则WebSockets不是很好.

此外,我们不希望接口服务器存储数据或尝试运行身份验证;它们的责任是简单,精简,快速的过程,而不需要很多状态,因此我们需要在我们的consumer功能中进行认证.


幸运的是,由于channel具有WebSockets和其他消息（ASGI）的底层规范,因此它可进行身份验证和获取基础Django session(Django身份验证所依赖的).

渠道可以使用来自Cookie的Django会话（如果在与主要网站相同的域下使用Websocket服务器,使用类似Daphne的方式）,或者,如果你想继续通过WSGI服务器运行HTTP请求并将将WebSockets卸载掉放到到另一个域名下的第二个服务器进程,使用`session_key`GET参数.

使用`http_session`装饰器来获取用的的 Django session,`message.http_session`会和       `request.session` 一样,还可以使用`http_session_user`装饰器来获得`message.user`.

现在,需要注意的是,你只能在 Websocket 的`connect`时获取详细的 HTTP 信息,这样我们可以节省带宽.

这意味着你必须在链接处理函数中处理获取用户信息,然后保存到 session 中, Channels 的`channel_session_user`和`http_session_user`结果一样,但是他从 channel session 中而不是 HTTP session加载用户.`transfer_user`方法将一个用户从一个 session 复制到另一个session.更好的是,它将所有这些组合到一个`channel_session_user_from_http`装饰器中.

现在来允许一个用户只能与跟他第一个名字相同的人聊天

```python
# In consumers.py
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http

# Connected to websocket.connect
@channel_session_user_from_http
def ws_add(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Add them to the right group
    Group("chat-%s" % message.user.username[0]).add(message.reply_channel)

# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    Group("chat-%s" % message.user.username[0]).send({
            "text": message['text'],
        })

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    Group("chat-%s" % message.user.username[0]).discard(message.reply_channel)
```

如果在只是使用` runserver`(或者 Daphne),你可以直接连接.如果你在其他域名下运行 Websocket, 你需要提供 Django 的 session ID 作为 URL 的一部分`socket = new WebSocket("ws://127.0.0.1:9000/?session_key=abcdefg");`

### 安全性

与 Ajax 不同, Websocket 请求不收 Same-Origin 协议限制.这意味着你不需要额外的步骤就能在不同主机之间通信

这是比较方便的,但是其他网站也能连接到你的 Websocket 应用上,当你使用`http_session_user`或者`channel_session_user_from_http`时,这个连接会被授权.

Websocket 明确要求浏览器在 HTTP 头 Origin 中发送 Websocket 请求的 origin. 但是 header 得验证留给了服务器.

你可以使用 `channels.security.websockets.allowed_hosts_only`装饰器来限制,连接只能来自`ALLOWED_HOSTS`

```python
# In consumers.py
from channels import Channel, Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http from channels.security.websockets import allowed_hosts_only.

# Connected to websocket.connect
@allowed_hosts_only @channel_session_user_from_http def ws_add(message):
    # Accept connection
    ...
```
来自其他主机的请求或者请求没有给出合法的 origin 头会被拒绝连接

`allowed_hosts_only`是`AllowedHostsOnlyOriginValidator`类装饰器的别名,他继承自`BaseOriginValidator`.如果你有其他的验证需求,可以创建子类来重写`validate_origin(self, message, origin)`,他必须返回 True 或者 False.

### 路由

`routing.py`文件和 Django 的 `urls.py`类似,可以根据 path 来路由到不同的 consumer 上,或者任何消息的字符串属性(例如 你可以依赖于`http.request` 消息method 键,进行路由)

route 使用正则表达式.因为path 不是特例,所有 Channels 不知道那是一个 URL, 你需要设置匹配规则第一个字符为`/`,并且末尾不包含`/`来使得匹配符可以链接

```python
http_routing = [
    route("http.request", poll_consumer, path=r"^/poll/$", method=r"^POST$"),
]
chat_routing = [
    route("websocket.connect", chat_connect, path=r"^/(?P<room_name>[a-zA-Z0-9_]+)/$"),
    route("websocket.disconnect", chat_disconnect),
]
routing = [
    # You can use a string import path as the first argument as well. 
    include(chat_routing, path=r"^/chat"),
    include(http_routing),
]
```

### Models

事实上我们想要把消息保存到数据库中,并且我们可能想要把消息从其他地方注入到聊天室,而不是客户的连接.

幸运的是,我们可以使用 Django 的 ORM 来处理消息的持久性,并且方便的把 send 融入到modelde保存流程中,而不是接收消息时.这样任何一个消息保存时都会广播到适当的客户端,不论消息从哪里被保存

我们将为新的消息定义自己的 channel,并且把 model 保存和聊天广播移动当中.`meaning the sending process/consumer can move on immediately and not spend time waiting for the database save and the (slow on some backends) Group.send() call.`

假设我们有个 ChatMessage表包含 message 和 room 字段

```python
# In consumers.py
from channels import Channel
from channels.sessions import channel_session from .models import ChatMessage

# Connected to chat-messages
def msg_consumer(message): # Save to model
    room = message.content['room']
    ChatMessage.objects.create(
        room=room,
        message=message.content['message'],
    )
    # Broadcast to listening sockets
    Group("chat-%s" % room).send({
    "text": message.content['message'],
    })

# Connected to websocket.connect
@channel_session
def ws_connect(message):
    # Work out room name from path (ignore slashes) 
    room = message.content['path'].strip("/")
    # Save room in session and add us to the group 
    message.channel_session['room'] = room 
    Group("chat-%s" % room).add(message.reply_channel) 
    # Accept the connection request 
    message.reply_channel.send({"accept": True})

# Connected to websocket.receive
@channel_session
def ws_message(message):
    # Stick the message onto the processing queue 
    Channel("chat-messages").send({
            "room": message.channel_session['room'],
            "message": message['text'],
        })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)

# in routing.py
from channels.routing import route
from myapp.consumers import ws_connect, ws_message, ws_disconnect, msg_consumer
channel_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
    route("chat-messages", msg_consumer),
]
```
你可以在任何地方向`chat-messages`channel 发送消息,在 View 中,其他 model的 post_save 信号中,在 cron 中等等.如果你想写一个机器人,我们可以把它放在`chat-messages` consumer 中,这样每个消息都会通过它.

### 强制排序

因为 Channels 是一个可以拥有很多 worker 的分布式系统,默认它只是以 worker 从队列中取出的顺序来处理消息.Websocket 接口服务器完全可以在几乎同时的请款下发出两个消息,第二个 worker 可以取出并且执行第二条消息,即使,第一个 worker 还没有处理完第一条消息

如果你保存 一个 consumer 的数据到 session中,然后从其他 consumer 中取出数据.但是 connect consumer 还不存在,他的 session 还没有被保存.同样的,如果有人尝试在 login view 完成之前请求 view.

Channels 中包含一个`enforce_ordering`装饰器.所有Websocket 消息都包含一个 order 属性,这个装饰器用来确保消息以正确的顺序被消费.另外 connect 消息会在直到他响应之前一直阻塞 socket 打开.所以你可以保证 connect 会在 receives 之前运行,即使没有使用`enforce_ordering`装饰器.

`enforce_ordering`使用`channel_session`来跟踪有多少消息被处理了,并且如果一个 worker 尝试在`out-of-order`消息之上运行 consumer 的话,他会导致`ConsumeLater`异常,他会把消息放回到源 channel 上,并且通知 worker 处理其他的消息.

使用`enforce_ordering`会耗费大量资源,所有他是可选的装饰器

### 部署

使用 Channels 来部署应用相对于 Django 的 WSGI 应用需要额外的一些步骤,但是你有一些选项,例如:如何部署以及你希望有多少流量通过 channel 来路由.

首先,记住对于 Django 来说这些完全是可选的.如果你保持默认的设置(没有CHANNEL_LAYERS),他会和运行 WSGI 应用一样

当你想要在生产中使用 Channels 时,你需要做三件事:
- 设置 channel backend
- 启动 worker 服务器
- 启动 接口服务器

你可用两种方式来实现:你可以通过两种方法之一来设置; 通过HTTP / WebSocket接口服务器路由所有流量,完全不需要运行WSGI服务器; 或者只是将WebSockets和长时间轮询的HTTP连接路由到接口服务器,并保留由标准WSGI服务器提供的其他页面.

通过接口服务器路由所有流量,你可以将WebSockets和长轮询共存在同一个URL树中,无需配置;如果你将流量分开,你需要在两台服务器之前配置一个Web服务器或第7层负载均衡器,以便根据路径或域将请求路由到正确的位置. 这两种方法都在下面.

#### 设置 channel backend

通常,通道后端将连接到用作通信层的一个或多个中央服务器 - 例如,Redis后端连接到Redis服务器. 所有这些都进入CHANNEL_LAYERS设置; 以下是远程Redis服务器的示例:

```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis-server-name", 6379)],
        },
        "ROUTING": "my_project.routing.channel_routing",
    },
}
```
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_rabbitmq.RabbitmqChannelLayer",
        "ROUTING": "my_project.routing.channel_routing",
        "CONFIG": {"url": "amqp://guest:guest@rabbitmq:5672/%2F", },
    }, 
}
```

#### 启动 worker 服务器

因为运行 consumer 的work和与`HTTP,Websocket,其他客户链接`通信的work是解耦的, 所有你需要一个 `worker 服务器集群`来做所有的处理.

每一个服务器是单线程的,所以建议你每台机器上每个核心上运行一或2个.在同一个机器上运行多个 worker 是安全的,因为他们不会打开任何一个端口(他们所做的只是与 channel backend 通信)

启动一个 worker 服务器:`manage.py runworker`

确保你运行在一个 init 系统中或者类似于supervisord的软件当中,他们能够在 worker 消失时重启它. wroker 服务器没有重启机制,尽管它会把内部的 consumer执行信息 写到 stderr 中.

需要监听 worker 的工作状态,如果他们过载的话,请求会花费很长时间来返回(直到过期时间或者容量达到极限时 HTTP 链接开始丢弃掉)

在更复杂的项目中,你可能不想让同一个 worker 服务于所有的 channel, 尤其是有的任务需要运行很长时间

可以设置 worker 只服务于特定名字的 channel 或者或略掉特定名称的 channel,使用`--only-channels`和`--exclude-channels`.例如:`python manage.py runworker --only-channels=http.* --only-channels=websocket.*`;`python manage.py runworker --exclude-channels=thumbnail`

#### 启动接口服务器

最后一个难题就是"接口服务器",这些进程将接收到请求并将其加载到channel系统中.

如果要支持WebSockets,长轮询的HTTP请求和其他channel功能,则需要运行原生ASGI接口服务器,因为WSGI规范不支持同时运行这些类型的请求.我们推荐一个接口服务器,我们建议你使用Daphne;它支持WebSockets,长时间轮询的HTTP请求,HTTP/2,并且执行得很好.

你可以继续运行你的Django代码作为一个WSGI应用程序,如果你喜欢,可以在uwsgi或gunicorn后面运行;但他们不支持WebSockets,因此你需要运行单独的接口服务器来终止这些连接,并在接口和WSGI服务器之前配置路由以适当地路由请求.

如果你使用Daphne来获取所有流量,它将在HTTP和WebSocket之间进行自动协商,因此你无需将WebSockets放在单独的域或path上（他们可以与你的普通视图代码共享cookies,如果你通过域名而不是path分离,则可能不可行）.

要运行Daphne,它只需要一个channel backe后端,就像WSGI服务器需要一个application一样. 首先,确保你的项目有一个asgi.py文件,它看起来像这样（它应该存在于wsgi.py旁边）：

```python
import os
from channels.asgi import get_channel_layer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_project.settings")
channel_layer = get_channel_layer()
```

`daphne my_project.asgi:channel_layer`

像runworker一样,你应该把它放在一个init系统或者像supervisord这样的东西,以确保它在意外的退出时被重新运行.

 如果你只运行daphne,没有任何worker,你的所有页面请求都会永远挂起; 那是因为daphne没有任何worker服务器来处理请求时,而是等待一个worker出现（而runserver也使用Daphne,它会在同一个进程中启动工作线程）. 在这种情况下,最终会超时,并在2分钟后给你503错误; 你可以使用`--http-timeout`命令行参数配置等待的时间.

#### 发布新的代码版本

将客户端连接处理与worer处理分离的好处之一是它意味着你可以运行新代码而不会丢弃客户端连接;这对于WebSockets尤其有用.

当你有新代码时,只需重新启动你的worker（默认情况下,如果你发送SIGTERM,他们将彻底退出并完成运行任何进程中的消费者）,并且任何以进入队列的消息或新连接将转到新的worker.只要新代码与session兼容,你甚至可以进行分阶段部署,以确保新代码的worker不会出现高错误率.

除非你升级了接口服务器本身或更改了CHANNEL_LAYER设置,否则不需要重新启动WSGI或WebSocket接口服务器.没有一个代码被他们使用,所有可以自定义请求的中间件和代码都在consumer中运行.

你甚至可以为接口服务器和woker使用不同的Python版本;channel层使用的通信协议 ASGI 被设计为可跨所有Python版本移植.

#### 只运行 ASGI

如果你只是运行daphne来服务所有的流量,那么上面的配置就足够了,你可以把它暴露在互联网上,它会提供任何类型的请求; 对于一个小型网站,只有一个daphne的实例和四到五个worker就够了.

然而,较大的网站将需要以更大的规模部署东西,而且如何扩展它们与WSGI是不同的;

#### 与WSGI一起运行ASGI

ASGI及其标准接口服务器Daphne都是相对较新的,因此你可能不希望通过它传输所有流量（或者你可能正在使用现有WSGI服务器的专门功能）.

如果是这样,那没关系你可以一起运行Daphne和WSGI服务器,Daphne只会服务于你需要的请求（通常是WebSocket和长时间轮询的HTTP请求,因为这些不适用于WSGI模型）.

要做到这一点,只需设置你的Daphne来服务上面讨论到的,然后配置你的负载均衡器或前端HTTP服务器进程,以将请求分派到正确的服务器 - 基于path,domain,或者 Upgrade 请求头.

基于path或domain意味着你需要仔细设计WebSocket URL,以便你可以随时了解如何在负载平衡器级别进行路由;理想的情况是能够查找`Upgrade：WebSocket`头,并通过它区分连接,但并不是所有的软件都支持这一点,并且它根本不能路由HTTP长连接.

你还可以反转此模型,并且默认情况下,所有连接都将转到Daphne,如果你有特定的URL或domain要使用WSGI服务器,则有选择地将其返回到WSGI服务器.

#### 在PaaS上运行

要在Platform-as-a-Service（PaaS）上通过 channel启动Django,你需要确保你的PaaS允许你以不同的scaling级别运行多个进程; 一组将作为一个纯Python应用程序运行Daphne（不是WSGI应用程序）,另一个组件将启动runworker.

PaaS还将提供自己的Redis服务或第三种进程类型,让你自己运行Redis来使用跨网络channel backend; 接口和worker进程都必须能够看到Redis.

如果你只被允许运行一个进程类型,接口服务器和worker服务器使用独立线程运行在一个进程中,并使用内存型 channel backend. 但是,不建议将其用于生产用途,因为你无法通过单个节点进行扩展.

#### 扩展

包含channel部署的扩展与扩展WSGI部署的扩展有所不同.

根本的区别在于,组内机器要求所有服务于同一站点的服务器能够看到彼此;如果你将站点切分并将其运行在几个大型集群中,那么消息只能发送到连接到同一集群的WebSockets.对于一些网站设计,这将是很好的.

对于大多数项目,你需要运行单个通道层,以实现正确的组投递.不同的后端扩展方式不同,但是Redis backend可以使用多个Redis服务器,并使用基于一致散列`consistent hashing`的分片技术来分离负载.

channel层知道如何扩展`channel’s delivery`的关键是如果它是否包含`！`字符,它表示`single-reader channel`.`single-reader channel`只能被一个进程连接,因此在Redis的情况下,它们存储在单个可预测的分片上.其他channel被假设有许多worker尝试读取它们,因此这些消息可以在所有分片上均匀分配.

Django channel还是比较新的,所以我们可能还不知道关于如何扩展的全部故事;我们运行大型负载测试来尝试改进和提高大型项目扩展,但不能代替实际情况.如果你正在扩展channels, 我们则鼓励你向Django团队发送反馈意见,并与我们一起研究channel backend的设计和性能,或者你可以自由自主创建; ASGI规范是全面的,并附有一致性测试套件,它应有助于对现有backend修改或开发新的backend.

### 通用消费者


### 引用

#### 消费者

配置channel路由时,绑定到channel的对象应该是一个可调用的,只需一个位置参数(这里称为消息,它是一个消息对象). 消费者是符合此定义的任何可调用的对象.

消费者没有任何返回,即使有返回也会被忽略. 他们可以通过跑出`channels.ConsumeLater`异常来将当前消息重新插入到他的channel的后面,但请注意,在消息被删除(以避免死锁)之前,你只能执行有限次数（默认为10）.

#### 消息

消息对象是消费者接收的唯一参数. 他们封装了基本的ASGI消息,他是一个dict,带有额外的信息. 它们具有以下属性：
- content：实际的消息内容,是一个dict.
- channel：一个Channel对象,表示消息的从哪一个channel上接收的. 如果一个消费者处理多个channel 时,则很有用.
- reply_channel：表示此消息的唯一回复通道的Channel对象,如果没有,则返回None.
- channel_layer：一个ChannelLayer对象,接收到的消息底层channel层. 这可以在具有多个channel层的项目中有用,以识别消费者生成的消息的位置（可以将其传递给Channel或Group的构造函数）

#### Channel

channel对象是ASGI channel的简单抽象,默认情况下是unicode字符串. 构造函数如下所示：

`channels.Channel(name, alias=DEFAULT_CHANNEL_LAYER, channel_layer=None)`

通常,您只需要调用`Channel("my.channel.name")`,但如果您处于设置了多个channel层的项目中,则可以传入 channel层别名或channel层对象,它将发送到该对象. 它们具有以下属性：

- name：表示通道名称的unicode字符串.
- channel_layer：一个ChannelLayer对象,表示发送消息的基础通道层.
- send(content)：通过channel发送content字典内容. content应符合相关的ASGI规范或协议定义.

#### Group

组以面向对象的方式表示基础的ASGI组概念,构造函数如下:

`channels.Group(name, alias=DEFAULT_CHANNEL_LAYER, channel_layer=None)`

它们具有以下属性：

- name：表示组名的unicode字符串.
- channel_layer：一个ChannelLayer对象
- send(content)：发送给组内所有成员的content字典内容.
- add（channel）：将给定的channel（Channel对象或unicode字符串名称）添加到组中. 如果channel已经在群组中, 则什么都不做.
- discard（通道）：从组中删除给定channel（Channel对象或unicode字符串名称）,如果在组中,则删除,否则什么都不做

#### Channel Layer

对底层ASGI channel层的封装,提供将channel映射到消费者的路由系统,使用别名来区分具有多个层.

可以直接通过别名获得他们

```python
from channels import channel_layers 
layer = channel_layers["default"]
```

具有以下属性

- alias: 别名
- router: channel 到消费者的映射.包含以下属性:
    – channels: 这个路由可以处理的 channel 集合, as unicode strings
    – match(message): 接收消息参数,并且要么反回一个消费者和从路由模式提取的要传递的参数名参数的元组,要么返回 None, 表示没有可用的路由


#### AsgiRequest

这是`django.http.HttpRequest`的子类,它提供了ASGI请求的解码,还有一些额外的ASGI特定的方法. 构造函数是：`channels.handler.AsgiRequest(message)`

消息必须是ASGI http.request 格式消息. 附加属性有：

- reply_channel,针对当前请求的`http.response.?`响应channel的Channel对象 
- message,传递给构造函数的原始ASGI消息.

#### AsgiHandler

这是`channels.handler`中的一个class,旨在通过ASGI消息来处理HTTP请求的工作流. 您可能不需要直接与之进行交互,但有两种有用的方法可以调用它：

- AsgiHandler(message) 将通过Django视图层处理消息,并产生一个或多个响应消息,以发送回客户端, encoded from the Django HttpResponse.
- encode_response(response) 类方法,接收Django HttpResponse, will yield one or more ASGI messages that are the encoded response

#### Decorators

Channels 提供了装饰器来提供数据持久性以及安全性

- `channel_session`: 向消费者提供一个类似 session 的对象称为`channel_session`, 他会作为消息的属性,该属性将在具有相同传入"reply_channel"值的消费者之间自动持久化.使用它可以在连接的整个生命周期内保留数据.
- `http_session`:包装一个HTTP或WebSocket连接消费者（或提供`cookies`或`get`属性的消息的任何消费者），以提供一个`http_session`属性，其行为类似于`request.session`;也就是说，它被保存在cookie中的每个用户会话密钥中，或作为`session_key`GET参数传递。它不会自动为没有session的用户cookie创建和设置会话cookie - 这就是session中间件所做的事情，对于更低级别的代码来说，这是一个更简单的只读版本.不允许设置新的 session,session 只能在 view 中设置,他只是 session 的访问器.
- `channel_and_http_session`:同时启用`channel_session`和`http_session`,在websocket.connect消息的`channel_session`中存储http session key。 然后，它会在后续消息中从同一个key对`http_session`进行hydrate。
- `allowed_hosts_only`:封装WebSocket连接消费者，并确保请求源自允许的主机。读取Origin标头，只将从ALLOWED_HOSTS中列出的主机发出的请求传递给消费者。来自其他主机或丢失或无效的Origin标头的请求将被拒绝