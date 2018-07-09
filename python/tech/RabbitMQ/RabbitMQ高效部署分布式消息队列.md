# RabbitMQ 高效部署分布式消息队列

##  Ubuntu安装启动

```shell
# 安装
sudo apt-get install rabbitmq-server

# 启动
# {start|stop|status|rotate-logs|restart|condrestart|try-restart|reload|force-reload}
sudo service rabbitmq-server start

# rabbitmq 命令只有 root 或者 rabbitmq 可以调用
# 切换到 rabbitmq 用户
su rabbitmq

# 查看状态
rabbitmqctl status
Status of node rabbit@ubuntu ...
[{pid,6109},
 {running_applications,[{rabbit,"RabbitMQ","3.5.7"},
                        {os_mon,"CPO  CXC 138 46","2.4"},
                        {mnesia,"MNESIA  CXC 138 12","4.13.3"},
                        {xmerl,"XML parser","1.3.10"},
                        {sasl,"SASL  CXC 138 11","2.7"},
                        {stdlib,"ERTS  CXC 138 10","2.8"},
                        {kernel,"ERTS  CXC 138 10","4.2"}]},
 {os,{unix,linux}},
 {erlang_version,"Erlang/OTP 18 [erts-7.3] [source] [64-bit] [async-threads:64] [kernel-poll:true]\n"},
 {memory,[{total,40200176},
          {connection_readers,0},
          {connection_writers,0},
          {connection_channels,0},
          {connection_other,2592},
          {queue_procs,2592},
          {queue_slave_procs,0},
          {plugins,0},
          {other_proc,13190624},
          {mnesia,57488},
          {mgmt_db,0},
          {msg_index,35120},
          {other_ets,737464},
          {binary,10800},
          {code,16972203},
          {atom,654217},
          {other_system,8537076}]},
 {alarms,[]},
 {listeners,[{clustering,25672,"::"},{amqp,5672,"::"}]},
 {vm_memory_high_watermark,0.4},
 {vm_memory_limit,416219136},
 {disk_free_limit,50000000},
 {disk_free,58918543360},
 {file_descriptors,[{total_limit,65436},
                    {total_used,3},
                    {sockets_limit,58890},
                    {sockets_used,1}]},
 {processes,[{limit,1048576},{used,123}]},
 {run_queue,0},
 {uptime,77}]
```

## 消息通信

### 生产者和消费者

生产者(producer)创建消息,然后发送给代理服务器(RabbitMQ).消息包含两个部分:payload和label.payload可以是任何数据,RabbitMQ使用label来决定谁会得到消息.

消费者订阅(queue)

应用程序既可以作为生产者也可以作为消费者.

当TCP链接打开时,应用程序可以创建一条AMQP信道.信道建立在TCP内的虚拟链接.AMQP命令都是通过信道发送出去的.每条信道有一个唯一ID.消息发布,订阅,接受都是通过信道完成.(TCP链接建立开销大,系统很快会达到瓶颈期,所以使用了信道.每个线程使用一个信道,保证线程的独立)

如果一个应用程序中有多个生产和消费者,那么可以在一个TCP链接下开多个信道,而不是每个线程开启TCP链接

### 队列

AMQP消息路由包含三部分:交换器,队列,绑定.绑定决定消息如何路由到特定的队列.

消费者通过两种方式从特定的队列中接受消息:
- 通过AMPQ的`basic.consume`订阅命令.这样信道会变成接受模式,直到取消订阅为止.
- 如果只是订阅一条消息,而不是持续订阅.使用`basic.get`命令.如果想要再次获得一条消息,需要再次发送`basic.get`.但是不应该使用循环来代替`basic.consume`.所以`basic.get`之后一般会取消订阅

如果消息到达的队列,没有订阅者,那么消息会一直保存在队列中

当消费者接受到消息时,需要发送确认,消费者通过`basic.ack`显示的想RabbitMQ发送一条确认,或者在订阅时设置`auto_ack=true`

**消费者对消息的确认和告诉生产者消息已经被接受了是两件不相关的事情**

如果消费者对某条消息处理发生错误,或者想要拒绝该条消息,有两种方式:
- 断开连接 *对RabbitMQ会增加负担,不推荐*
- 使用 `basic.reject` 来拒绝, **如果 reject 的 requeue 设置为 true 那么消息会被重新发送给下一个订阅者,如果是 false 的话那么消息会被删除,当然也可以使用 `basic.ack` 来让 RabbitMQ 删除该条消息,只不过消费者还是没有处理这条消息**

> `basic.reject requeue=false`方式时,被拒绝的消息会被 RabbitMQ 保存下来,他们被称为 `dead letter`

#### 创建队列

消费者和生产者都可以通过 `queue.declare` 命令来创建队列.如果消费者在同一条信道上订阅了另一队列时,就无法再创建队里.必须先取消订阅,将信道置为传输模式.

创建队列时,需要指定队列名称.消费者订阅队列时需要队列名称,并且在创建绑定时也需要指定队里名称.如果没有指定名称 RabbitMQ 会自动分配一个,并且在 queue.declare 命令的相应中返回.

队列的一些有用参数
- `exclusive` 如果为 true, 那么队列将变成私有,此时只有你的应用程序才能够消费队列消息.当你想要限制一个队列只有一个消费者的时候很有帮助
- `auto-delete` 当最后一个消费者取消订阅时,队列会自动一处.如果需要使用临时队列时exclusive 和 auto-delete 一起使用,当消费者断开连接时队里就自动删除了.

如果队里已经声明过了,再次声明会返会与创建新队列结果一致.实际中应当使用生产者和消费者都去声明队列.这样确保消息队列.

### 交换器和绑定

