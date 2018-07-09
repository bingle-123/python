# Mastering RabbitMQ

这本书适合了解RabbitMQ

## 开始

### 使用场景：

- 确保消息被传递和接受
- 将消息路由到正确的目的地
- 保存消息的状态
- 支持多种传输协议（AMQP, MQTT, STOMP, HTTP)
- 支持集群
- 高可用，可扩展，可伸缩。
- 支持插件
- 支持多种语言客户端

### 安装与启动

sudo apt-get install rabbitmq-server && sudo rabbitmq-server

## 配置 RabbitMQ

有三中配置方法：

- 环境变量
- 配置文件：传递服务组件的设置
- 运行时参数：管理集群配置，他会在运行时候就生效

### 环境变量

环境变量存储在文件中rabbitmq-env.conf中CONFIG_FILE=/etc/rabbitmq/testfile 常用环境变量：

- RABBITMQ_BASE：RabbitMQ基础文件夹，存放database和log
- RABBITMQ_CONFIG_FILE：rabbitmq有默认配置文件，可以用这个配置修改默认配置文件
- RABBITMQ_LOGS：rabbitmq有不同等级的日志，他有默认的目录，这个变量可以修改默认日志目录
- RABBITMQ_NODE_IP_ADDRESS：默认rabbitmq绑定到所有接口，用它改变绑定地址
- RABBITMQ_NODE_PORT：默认rabbitmq默认绑定到5672端口，用它改变端口
- RABBITMQ_PLUGINS_DIR：rabbitmq有很多插件可用，这里配置插件目录
- RABBITMQ_CONSOLE_LOG：new|reuse，默认rabbitmq console输出是不保存的，使用new保存到新的日志文件，reuse使用老的日志文件
- RABBITMQ_LOG_BASE：保存日志文件的基础目录
- RABBITMQ_MNESIA_BASE：存放Mnesia数据文件的基础目录，如果设置了RABBITMQ_MNESIA_DIR，这个设置就会失效。
- RABBITMQ_MNESIA_DIR：设置Mnesia数据文件目录。
- RABBITMQ_NODENAME：rabbitmq节点的名称，需要确保名称唯一。
- RABBITMQ_SASL_LOGS：System Application Support Libraries 日志文件
- RABBITMQ_SERVICENAME：在操作系统上rabbitmq服务名称。

### 配置文件

环境变量配置，多数用来空值文件目录。配置文件用来管理引擎，例如：授权，行为，内存限制，磁盘限制，exchange，queue，binding等。默认配置文件在`/etc/rabbitmq/rabbitmq.config`。 常用配置变量：

- auth_mechanisms：配置不同的授权机制。
- auth_backends：设置SASL授权数据库L.默认: [rabbit_auth_backend_ internal]
- default_user：设置可以访问rabbitmq的默认用户的username
- default_pass：默认用户的密码
- default_permission：默认用户的权限
- disk_free_limit：设置保存在磁盘上消息的大小，超过时将发出提醒。
- heartbeat：确认客户端是否还存活，
- hipe_compile：rabbitmq使用默认的erlang编译器编译，我们可以选择高性能的erlang编译器
- log_levels：设置日志级别none,error,warning,info
- tcp_listeners：可以同时设置绑定的ip和端口
- ssl_listeners：客户端通过ssl连接rabbitmq时的端口号和ip
- vm_memory_high_watermark：可使用的内存空间大小，超过时将发出提醒。
- collect_statistics：设置statistics collection mode，默认none，可选：none,coarse,fine
- collect_statistics_interval：设置statistics collection interval单位毫秒，默认5000
- msg_store_file_size_limit：设置保存诶条消息的文件大小.默认:16777216

### 参数管理

我们可以直接使用`rabbitmqctl set_parameter`给指定的组件设置参数。 `clear_parameter`用来清楚指定组件的参数。

### Policy管理

`rabbitmqctl set_policy|clear_policy`

### 内存管理

`rabbitmqctl set_vm_memory_high_watermark`

## Architecture and Messaging

### 消息和它的使用场景

消息在producer和customer之间传输。**Message Broker** 用来控制消息流动。控制并不是很简单的事情，所以broker需要很多额外的信息。下面是消息常见的问题以及broker如何解决他们。

#### 关联软件系统

多个模块之间直接通信频繁，关联性较大。修改其中一个模块，会影响其他模块。那么broker可以放在这些模块中间，作为中转站，各个模块只需把自己要发送的消息发给borker，broker再发给消息接受者。

#### 多个平台

系统有java，python，.net ...多个平台组成。他们通过broker连接。

#### 企业应用的消息

![raw](./src/enterprise msg raw.png) 企业应用例如人力资源，项目管理系统，客户管理系统等，他们之间通信频繁。broker保证他们之间的消息准确到达。 ![msg](./src/enterprise rabbit.png)

### Message Broker

message Broker是消息管理器，他负责很多任务：

- 确保消息发给正确的接受者
- 将消息路由到正确的队列和接受者
- 支持不同的路由算法：Pub-Sub，Direct，Topic Based等
- 扩展队列
- 支持消息的持久存储以及临时存储

### Message consumers

producer发送消息给broker，broker将消息路由到指定consumer。consumer等待到来的消息并进行处理。 consumer可以满足同步或者异步，通常不适用同步。consumer是消息系统的终点。

### Messages

消息是消息系统的主要实体。 消息有一些属性。headers包含sender，receiver，format。bodies是消息的内容可以有很多格式例如：JSON，XML，Binary等等。

### AMQP 元素

Producer创建消息，然后消息到达Exchange，然后路由到Queue。

- Message Flow：消息的生命周期
- Exchange：接受消息，然后路由到消息队列
- Message Queue：将消息保存在内存或者磁盘，并且发给Consumer
- Bindings：声明Exchange和Queue关系，这个关系指明消息如何被路由到正确的Queue。 ![amqp](./src/amqp.png)

### Message Flow

Producer-->Exchange-->Queue--Consumer

### Exchange

Exchange将消息路由到Queue，路由规则由Bindings来定义。它包含几个重要属性：

- Name：通常服务器会自动指定名字
- Durable：消息队列是否持久，依赖于是否设置为持久或者临时(broker重启时是否自动创建他)
- Auto-delete：当所有队列完成时，是否自动删除exchange

### Message Queue

消息队列以FIFO方式保存消息。如果一个队列有多个reader，通常其中一个reader优先级较高。那么优先的reader在其他reader之前读取了消息，这个模型成为`weak FIFO`。他有几个重要属性：

- Name:队列的名字
- Durable：如果设置，那么队列不可丢失任何消息
- Exclusive：如果设置，那么链断关闭时，队列会被删除
- Auto-delete：如果设置，那么当所有consumer都取消订阅时，队列会被自动删除

### Bindings

binding是exchange将消息路由到queue的路由规则。binding通过`routing key`定义。

### AMQP Message

Message是AMQP的原子单元，包含几个属性：

- 消息体
- Header
- Properties

### 虚拟主机

虚拟主机有独立的环境，环境包含，用户组，exchange，queue等。客户端可以从虚拟主机列表选择虚拟主机，每个主机的授权机制可以不同，

### Exchange 类型

Exchange的类型定义路由算法。AMQP中有5个默认类型，我们可以创建类型。

#### direct

流程：

1. 一个queue通过路由key`K`绑定到Exchange
2. producer向exchange发送一条消息，消息的路由key`R`
3. 如果`R`等于`K`那么消息被路由到queue

#### fan-out

流程：

1. 一个queue绑定到exchange时没有带任何参数
2. 当producer发送消息到exchange时，消息会被发送给所有没带参数的queue

### topic

流程：

1. queue通过路由pattern`P`绑定到exchange
2. producer向exchange发送一条消息，消息的路由key`R`
3. 如果R匹配P那么消息发送到queue
4. 匹配算法：路由key必须包含0或多个词组用`.`分割，例如`news.tech`。路由pattern与模式匹配类似，`*`代表匹配一个字符，`#`匹配一个活或多个字符，例如：`news.*`匹配`news.tech`。

### header

header是最强大的类型。他通过匹配消息header来路由消息。exchange会忽略路由key。当创建exchange时，给他指定关联headers，消息headers通过`x-match`匹配exchange的headers

## 集群与高可用

两种高可靠性方案：

1. 在broker之间传递消息
2. 集群，协调多个rabbitmq服务器节点

### Federation in RabbitMQ

Federation可以在多个rabbitmq服务器时处理大量消息，他是通过broker之间传递消息，不需要通过集群。 使用Federation的原因：

- 松耦合
- WAN-友好
- 可扩展
- 独立性

Federation插件在标准服务中已经可用，通过下面命令启用： `rabbitmq-plugins enable rabbitmq_federation` 如果你使用了rabbitmq的management插件，那么你可以通过rabbitmq_federation_management插件来监控federation。 `rabbitmq-plugins enable rabbitmq_federation_management` Federation相关信息和配置会保存在RabbitMQ数据库中。和Federation相关的配置有3个：

1. Upstreams：他定义如何连接到另一台RabbitMQ服务器
2. Upstream sets：设置upstream组
3. Policies：他是Federation的规则集合

我们可以通过`rabbitmqctl`来管理Federation，例如定义upstream： `rabbitmqctl set_parameter federation-upstream my-upstream'{"uri":"amqp://localhost","expires":72000}'` 定义Policy：`rabbitmqctl set_policy --apply-to exchanges federate-me "^amq\." '{"federation-upstream-set":"all"}'`

### Clustering in RabbitMQ

集群是我们的主要解决方案。RabbitMQ服务器提供了集群机制。集群装置通过给节点复制所有的data/states来实现可扩展性和可靠性。 每个节点需要选择把数据存在磁盘上还是内存中。如果管理员选择内存，那么消息只会在内存中。如果选择磁盘，那么磁盘和内存都会保存。

### Creating clusters

首先启动几个RabbitMQ服务

```shell
mastering-rabbitmq1$ rabbitmq-server –detached
mastering-rabbitmq2$ rabbitmq-server -detached
mastering-rabbitmq3$ rabbitmq-server –detached
mastering-rabbitmq4$ rabbitmq-server –detached
```

现在我们可以使用`cluster_status`来查看只有一个节点的集群是否已经启动了，

```shell
mastering-rabbitmq1$ rabbitmqctl cluster_status
Cluster status of node rabbit@mastering-rabbitmq1 ...
[{nodes,[{disc,[rabbit@mastering-rabbitmq1]}]},
 {running_nodes,[rabbit@mastering-rabbitmq1]},
 {partitions,[]}]
...done.

mastering-rabbitmq2$ rabbitmqctl cluster_status
Cluster status of node rabbit@mastering-rabbitmq2 ...
[{nodes,[{disc,[rabbit@mastering-rabbitmq2]}]},
 {running_nodes,[rabbit@mastering-rabbitmq2]},
 {partitions,[]}]
...done.

mastering-rabbitmq3$ rabbitmqctl cluster_status
Cluster status of node rabbit@mastering-rabbitmq3 ...
[{nodes,[{disc,[rabbit@mastering-rabbitmq3]}]},
 {running_nodes,[rabbit@mastering-rabbitmq3]},
 {partitions,[]}]
...done.

mastering-rabbitmq4$ rabbitmqctl cluster_status
Cluster status of node rabbit@mastering-rabbitmq4 ...
[{nodes,[{disc,[rabbit@mastering-rabbitmq4]}]},
 {running_nodes,[rabbit@mastering-rabbitmq4]},
  {partitions,[]}]
...done.
```

检查完每个节点状态后，接下来通过`join_cluster`将一个集群加入到另一个集群，首先`stop_app`，然后加入集群，然后`start_app`，这里我们将服务器2，加入到服务器1

```shell
mastering-rabbitmq2$ rabbitmqctl stop_app
Stopping node rabbit@mastering-rabbitmq2 ...done.
mastering-rabbitmq2$ rabbitmqctl join_cluster rabbit@mastering-
rabbitmq1
Clustering node rabbit@mastering-rabbitmq2 with [rabbit@mastering-
rabbitmq1] ...done.
mastering-rabbitmq2$ rabbitmqctl start_app
Starting node rabbit@mastering-rabbitmq2 ...done.
```

再来看一下服务器1,2的状态

```shell
mastering-rabbitmq1$ rabbitmqctl cluster_status
Cluster status of node rabbit@mastering-rabbitmq1 ...
[{nodes,[{disc,[rabbit@mastering-rabbitmq1]}],
{disc,[rabbit@mastering-rabbitmq2]}]},
},{running_nodes,[rabbit@mastering-rabbitmq1,rabbit@mastering-rabbitmq2]},{partitions,[]}]
...done.

mastering-rabbitmq2$ rabbitmqctl cluster_status
Cluster status of node rabbit@mastering-rabbitmq2 ...
[{nodes,[{disc,[rabbit@mastering-rabbitmq2]}],
{disc,[rabbit@mastering-rabbitmq1]}]},
},{running_nodes,[rabbit@mastering-rabbitmq2,rabbit@mastering-rabbitmq1]},{partitions,[]}]
 ...done.
```

### Changing the cluster node types

我们通过`change_cluster_node_type`可以修改节点的类型,首先`stop_app`-->修改类型-->`start_app`;

```shell
mastering-rabbitmq3$ rabbitmqctl stop_app
Stopping node rabbit@mastering-rabbitmq3 ...done.

mastering-rabbitmq3$ rabbitmqctl change_cluster_node_type ram
Turning rabbit@mastering-rabbitmq2 into a ram node
...done.

mastering-rabbitmq3$ rabbitmqctl start_app
Starting node rabbit@mastering-rabbitmq3 ...done.
```

### Updating cluster nodes

有时候其中一个失败，我们希望将他从集群中移除掉。通过`reset`可以将节点移除掉：

```shell
mastering-rabbitmq4$ rabbitmqctl stop_app
Stopping node rabbit@mastering-rabbitmq4 ...done.

mastering-rabbitmq4$ rabbitmqctl reset
Resetting node rabbit@mastering-rabbitmq4
...done.

mastering-rabbitmq4$ rabbitmqctl start_app
Starting node rabbit@mastering-rabbitmq4
...done.
```

上面这个方法是一处自身，还有一个方法可以直接一处其他节点，通过`forget_cluster_node`

```shell
mastering-rabbitmq4$ rabbitmqctl forget_cluster_node rabbit@mastering-rabbitmq3
Removing node rabbit@mastering-rabbitmq3 from cluster ...
...done.
```

有时候我们需要在一台机器上跑多个RabbitMQ服务，可以通过给定不同的实例名称和端口来解决。

```shell
mastering-rabbitmq1$ RABBITMQ_NODE_PORT=5672 RABBITMQ_NODENAME=rabbit1-node rabbitmq-server –detached

mastering-rabbitmq1$ RABBITMQ_NODE_PORT=5673 RABBITMQ_NODENAME=rabbit2-node rabbitmq-server –detached

mastering-rabbitmq1$ rabbitmqctl –n rabbit2-node stop_app
Stopping node rabbit2-node@mastering-rabbitmq1 ...done.

mastering-rabbitmq1$ rabbitmqctl –n rabbit2-node join_cluster rabbit@hostname
Clustering node rabbit2-node@mastering-rabbitmq1 with [rabbit1-node@mastering-rabbitmq1] ...done.

mastering-rabbitmq1$ rabbitmqctl –n rabbit2-node start_app
Starting node rabbit2-node@mastering-rabbitmq3 ...done.
```

### 集群配置文件

在RabbitMQ的`configuration`文件中配置集群节点信息， cluster_nodes 如果是磁盘节点类型：`[{rabbit,[{cluster_nodes,{['rabbit@mastering-rabbitmq1', 'rabbit@mastering-rabbitmq2','rabbit@mastering-rabbitmq3', 'rabbit@mastering-rabbitmq4'],disc}}]}]`. 如果是内存节点类型： `[{rabbit,[{cluster_nodes,{['rabbit@mastering-rabbitmq1', 'rabbit@mastering-rabbitmq2','rabbit@mastering-rabbitmq3', 'rabbit@mastering-rabbitmq4'],ram}}]}]`. cluster_partition_handling:默认为ignore，可选：Ignore, pause_minority, autoheal

### 队列的负载均衡

RabbitMQ的负载均衡在TCP层，我们可以使用`HAProxy`来实现负载均衡。 HAProxy有自己的配置文件，常见的RabbitMQ负载配置：

```shell
(HAProxy)
    global
    log     127.0.0.1 alert
    log     127.0.0.1 alert debug

    defaults
    log        global
    mode       http
    option     dontlognull
    option     redispatch
    retries    3
    contimeout 5000
    clitimeout 50000
    srvtimeout 50000
    listen rabbitmq 192.168.1.1:5000
    mode    tcp
    stats   enable
    balance roundrobin
    option  forwardfor
    option  tcpka
    server  rabbit01 192.168.1.1:5672 check inter 5000 downinter 500
    server  rabbit02 192.168.1.2:5672 check inter 5000 backup
    server  rabbit03 192.168.1.3:5672 check inter 5000 backup
```

我们还可以使用nginx的`nginx_tcp_proxy_module`来实现负载均衡

```
tcp {
     upstream cluster {
       # simple round-robin
       server 192.168.1.1:5672;
       server 192.168.1.2:5672;
       check interval=3000 rise=2 fall=5 timeout=1000;
}
server {
listen 5672;
    proxy_pass cluster;
  }
}
```

## Plugins and Plugin Development

查看有哪些插件`rabbitmq-plugins list` 启用插件`rabbitmq-plugins enable rabbitmq_jsonrpc` 停用插件`rabbitmq-plugins disable rabbitmq_jsonrpc`

## Managing Your RabbitMQ Server

RabbitMQ支持的管理特性：

- 添加，更新，查询：用户、虚拟主机、权限
- 声明，展示，删除：exchange、queue、binding
- 发送，接收：消息
- 监控：queue长度，全局消息速率，每个channel消息速率，每个连个的数据速率等等
- 将对象定义导入/导出为JSON
- 强制关闭连接
- 清楚队列

我们可以使用rabbitmqctl来进行管理操作，有3中常见方式来管理RabbitMQ：

1. 命令行
2. 浏览器插件
3. REST 接口

### 命令行

#### 集群命令

- join_cluster {clusternode} [--ram]:加入到指定的集群，如果--ram指定了那么节点的类型为ram。例如：`rabbitmqctl join_cluster newcl@local --ram`
- forget_cluster_node [--offline]:从集群中移除掉远程节点，如果是使用--offline，那么RabbitMQ会把掉线的远程节点移除。
- change_cluster_node_type {disc|ram}:修改节点的类型
- cluster_status:显示集群的状态
- update_cluster_nodes {clusternode}:使用最新的信息来更新所有的集群，如果给出了clusternode，那么只会更新指定集群

#### 用户命令

- `add_user <username> <password>`:使用给定的用户名和密码添加一个新的用户
- `delete_user <username>`:删除指定的用户
- `change_password <username> <password>`:修改用户密码
- `clear_password <username>`:清楚用户的密码
- `set_user_tags <username> <tag>`:给用户设置一个tag
- `list_users`:显示所有的用户

#### 虚拟主机和权限

- `add_vhost <vhostpath>`:添加新的虚拟主机
- `delete_vhost <vhostpath>`:删除指定的虚拟主机
- `list_vhosts [<vhostinfoitem>...]`:显示所有虚拟主机的信息，vhosinfoitem指定要显示那些信息
- `set_permissions [-p <vhostpath>] <user> <conf> <write> <read>`:给指定的用户设置权限，例如写和读，如果制定了额vhostpath，那么用户的权限只针对该虚拟主机。
- `clear_permissions [-p <vhostpath>] <username>`:清楚指定用户的所有权限，如果指定了vhostpath，那么只会清楚该虚拟主机上该用户的权限。
- `list_permissions [-p <vhostpath>]`:显示所有权限，如果指定vhostpath，那么只显示该虚拟主机的权限
- `list_user_permissions [-p <vhostpath>] <username>`:显示给定给用户的权限，如果指定了vhostpath那么只会先用户在该虚拟主机上的权限

#### 其他命令

- `set_parameter [-p <vhostpath>] {component_name} {name} {value}`:设置参数，如果指定了vhostpath那么只会设置该虚拟主机的参数
- `clear_parameter [-p <vhostpath>] {component_name} {key}`:清除给定的参数，如果指定了vhostpath那么只会清除该虚拟主机的参数
- `list_parameters [-p <vhostpath>]`:清除所有参数，如果指定了vhostpath那么只会清除该虚拟主机的所有参数
- `set_policy [-p <vhostpath>] [--priority priority] [--apply-to apply-to] {name} {pattern} {definition}`:设置policy
- `clear_policy [-p <vhostpath>] <name>`:清除指定的policy
- `list_policies [-p <vhostpath>]`:显示所有的policy
- `list_queues [-p <vhostpath>] [<queueinfoitem>...]`:显示所有队列的信息，queueinfoitem指定显示那些信息，vhostpath指定哪一个虚拟主机。
- `list_exchanges [-p <vhostpath>] [<exchangeinfoitem>...]`:显示所有的exchange信息。
- `list_bindings [-p <vhostpath>] [<bindinginfoitem>...]`:显示所有的binding信息
- `list_connections [<connectioninfoitem>...]`:显示所有的链接信息
- `list_consumers [-p <vhostpath>]`:显示所有的consumer
- `list_channels [<channnelinfoitem>...]`:显示所有的channel信息
- `status`:显示当前的RabbitMQ broker状态
- `environment`:显示环境变量
- `report`:生成一个系统报告到文件中：`rabbitmqctl report > report.txt`
- `eval <expr>`:执行Erlang表达式
- `close_connnection <connectionpid> <explanation>`:根据Erlang进程ID关闭链接
- `trace_on [-p <vhost>]`:启动跟踪，如果指定了vhost那么只会跟踪该虚拟主机
- `trace_off [-p <vhost>]`:关闭跟踪
- `set_vm_memory_high_watermark <fracion>`:设置信息的内存限制，例如`rabbitmqctl set_vm_memory_high_watermark 0.4`

### web管理

1. rabbitmq-plugins enable rabbitmq_management
2. rabbitmqctl stop
3. rabbitmq-server
4. 浏览器打开`http://localhost:15672/`
5. 默认用户guest:guest

### REST 接口

## Monitoring

## Security in RabbitMQ

`sudo rabbitmqctl set_permissions -p / jack ".*" ".*" ".*"`

## Python Client Programming

### 依赖库

`pip install pika`

### 构建Producer

```python
#!/usr/bin/env python
import pika
print "* Connecting to RabbitMQ broker"
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='pages')
# default empty exchange with routing key equal to the queue name
# will route the message to that queue
channel.basic_publish(exchange='',routing_key='pages',body='testing: 1, 2, 3')
print "* Done sending!"
connection.close()
```

上面使用的是block链接，也可以选择non-blocking链接`Select connection`。下一步建立channel，声明queue，发送消息。

### 构建Consumer

```python
import pika
def handler(ch,method,properties,body):
    print("-> Handled: [%s] " % body)
connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()
print("Handling messages.")
channel.basic_consume(handler,queue='pages',no_ack=True)
channel.start_consuming()
```

和producer不同的是，consumer鉴定queue已经存在了，所有没有再次声明他。

### 定时任务[schedule](https://github.com/dbader/schedule)

`pip install schedule`

```python
import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
# 这个循环结构类似于启动一个守护进程永不退出
```

下面每5秒发送一条消息

```python
#!/usr/bin/env python
import pika
import schedule
import time
urls = [ "http://ebay.to/1G163Lh" ]
print "* Connecting to RabbitMQ broker"
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='pages')
def produce():
    for url in urls:
        print("* Pushed: [%s]" % (url))
        channel.basic_publish(exchange='', routing_key='pages', body=url)

schedule.every(5).seconds.do(produce)
while True:
    schedule.run_pending()
    time.sleep(1)

connection.close()
```

### 错误处理，使用acknowledgement

当使用no_ack=False模式时，会确保消息被处理，否则消息会保存下来，继续留在队列中。

```python
import pika
def handler(ch,method,properties,body):
    print("-> Handled: [%s] " % body)
connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()
print("Handling messages.")
channel.basic_consume(handler,queue='pages',no_ack=False)
channel.start_consuming()
```

### Pika Api

#### Connecting

一种方式是通过ConnectionParameters来指定链接参数，另一种是给定义包含所有需要参数的URL。

**pika.URLParameters('amqps://www:pwd@rabbit1/web_messages')**

`amqps://www-data:rabbit_pwd@rabbit1/web_messages`这个配置URL指定连接到rabbit1服务器下的web_messages虚拟主机。

`amqps://www-data:rabbit_pwd@rabbit1/web_messages?heartbeat_interval=30`这个参数指定heartbeat_interval为30

`amqp://www-data:rabbit_pwd@rabbit1/web_messages?heartbeat_interval=30&ssl_options=%7B%27keyfile%27%3A+%27%2Fetc%2Fssl%2Fmyey.pem%27%2C+%27certfile%27%3A+%27%2Fetc%2Fssl%2Fmycert.pem%27%7D`指定了ssl的参数

其他可用的参数：

- backpressure_detection:默认禁用，
- channel_ma:channel允许的最大链接数
- channel_attempts:默认1
- frame_max:frame的最大值
- heartbeat_interval:client/server heartbeat interval，以前5比较合适，现在一般是30
- locale:客户端的locale
- retry_delay:再次尝试链接的时间间隔，通常和chanel_attempts一起使用
- socket_timeou:默认0.25
- ssl_options:URL编码字典keys: ca_certs, cert_reqs, certfile, keyfile, ssl_version.

**pika.ConnectionParameters(host='localhost',heartbeat_interval=30,retry_delay=2)**

### BlockingConnection

常用属性：

- add_backpressure_callback:添加回调函数，当客户端接受到broker的backpresure事件是执行的回调
- basic_nack:broker是否支持nack
- channel:创建新的channel
- close:关闭连接
- is_closed/is_closing/is_open:检查连接状态

### BlockingChannel

- add_on_close_callback:添加channel关闭时的回调函数
- add_on_flow_callback:添加回调函数，当客户端接受到flow control事件时
- add_on_return_callback:添加回调，当发送消息的客户端，收到来自服务端的拒绝时。这个回调函数用处很大，如果不这么做的话可能使系统隐藏大的bug
- basic_ack/basic_nack:这是很重的一个属性。如果你使用acknowledge的话必须使用这个属性。当调用他时，必须指定`delivery_tag`，他会在consumer的处理函数中传递。
- basic_consume:这是另一个重要的属性。它的参数

  - consumer_callback:毁掉函数
  - queue:队列名称
  - no_ack:是否使用acknowledge
  - exclusive:means not to allow any other on this queue
  - consumer_tag:通常不用
  - arguments:自定的参数，通常不用

- badic_get:和basic_consume类似，但是他只接受一条消息，包括queue和no_ack参数

- basic_publish:

  - exchage:用来发布消息
  - routing_key:用来绑定的路由key
  - body:消息内容
  - mandatory:如果false，服务器会直接丢弃掉不能路由到队列的消息，否则想客户端发回消息。
  - Immediate:和前面类似，但是服务器不保证消息放入到路由到队列中
  - basic_qos:
  - prefetch_size:
  - prefetch_count:
  - all_channels:将规则应用到所有channel
  - basic_recover:告诉服务器重新发送所有没有收到确认的消息

### Delcaring queues and exchanges

- exchange_declare:如果exchange不存在的话就创建。如果exchange已经存在，再次声明时如果使用了不同的参数，就会报错：

  - exchange：名称
  - exchange_type:类型
  - passive:检查exchange是否存在，不存在则创建
  - durable:将他设置为永久性，broker重启时他会自动被创建
  - auto_delete:没有队列绑定时，自动删除
  - internal:This can only be published into by other exchanges

- queue_declare:如果不存在则创建，

  - queue:名称
  - passive:passive名称
  - durable:永久性，broker重启时自动创建
  - exclusive:允许在consumer之间共享
  - auto_delete:当一个consumer断开连接时删除掉

- queue_bind:

  - queue:队列名
  - exchange:exchange名
  - routing_key:路由key
  - no_wait:不等待绑定是否完成

### 授权

普通授权

```python
import pika
credentials = pika.PlainCredentials('guest','guest')
parameters = pika.ConnectionParameters('rabbit1',5672,'/',credentials)
```

ssl连接，使用URLParameters。`amqps_URI = "amqps://user:pass@host:10000/vhost"`

```python
 ssl_options = ({"ca_certs": "caroot.pem",
                  "certfile": "client.pem",
                  "keyfile": "key.pem"})
parameters = pika.ConnectionParameters(host,5671,credentials=ExternalCredentials(),ssl=True,ssl_options=ssl_options)
```

### Celery

consumer.py

```python
#!/usr/bin/env python
import requests
fromBeautifulSoup import BeautifulSoup
from celery import Celery
app = Celery('celery_pages', broker='amqp://guest@localhost//')
@app.task
def scrape(url):
    print "-> Starting: [%s]" % (url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    print "-> Extracted: %s" % (soup.html.head.title)
    print "-> Done: [%s]" % (url)
```

producer.py

```python
#!/usr/bin/env python
import schedule
import time
from celery import Celery
from celery_scraper import scrape
app = Celery('celery_pages', broker='amqp://guest@localhost//')
urls = [ "http://ebay.to/1G163Lh" ]
def produce():
    forurl in urls:
    scrape.delay(url)
    print("* Submitted: [%s]" % (url))

schedule.every(10).seconds.do(produce)
while True:
    schedule.run_pending()
    time.sleep(1)
```

### Celery其他特性

定时任务,类似于cron的表达式结构 `celery -A proj cron.py`

```python
from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}
```
