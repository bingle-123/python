# 集群配置

## ubuntu设置
### 固定 IP

`sudo vim /etc/network/interfaces`

```shell 
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto enp0s3
#iface enp0s3 inet dhcp
iface enp0s3 inet static
address 192.168.1.161 
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 114.114.114.114 
```

## redis 设置

### 修改监听地址

```
sudo vim /etc/redis/redis.conf

bind 192.168.1.160 127.0.0.1
```
### 主从复制

主数据库负责读写,从数据库负责读.主数据库发生数据变动,自动同步到从数据库

```
sudo service redis-server stop
redis-server --slaveof 192.168.1.160 6379
```
或者
```
192.168.1.161:6379> slaveof 192.168.1.160 6379

如果本数据库已经是其他数据库的从数据库了,那么会解除与原来主数据库关系,转而与新的数据库同步.
slaveof no one 使得当前数据库停止接收其他数据库的同步并转为主数据库
```

测试

```
# 链接到主数据库添加数据
redis-cli -h 192.168.1.160
192.168.1.160:6379> set test test
OK
192.168.1.160:6379> INFO
.....
# Replication
role:master
connected_slaves:1
slave0:ip=192.168.1.161,port=6379,state=online,offset=393,lag=0
master_repl_offset:393
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:2
repl_backlog_histlen:392
.....

# 连接到从数据可以看到
redis-cli -h 192.168.1.161
get test 
"test"
# 从数据库添加数据不允许
192.168.1.161:6379> set s 123
(error) READONLY You can't write against a read only slave.
# 可以设置从数据库的配置`slave-read-only`为 no 来允许从数据库可写,但是不应该这么做,因为从数据库更新不会同步到其他数据库,并且主数据库的更新会覆盖掉从数据更新
# 查看集群信息
192.168.1.161:6379> INFO
......
# Replication
role:slave
master_host:192.168.1.160
master_port:6379
master_link_status:up
master_last_io_seconds_ago:2
master_sync_in_progress:0
slave_repl_offset:309
slave_priority:100
slave_read_only:1
connected_slaves:0
master_repl_offset:0
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0
.....

```

### 原理

当从数据库启动后,会向主数据库发送 SYNC 命令.主数据库接收到 SYNC 后会在后台保存快照,并将快照期间的命令缓存起来,当快照完成时, redis 会将快照文件和所有缓存的命令发送到从数据库

### 数据库持久化

为了提高性能,可以通过复制功能建立从数据库,并启用从数据库的持久化,同时禁用主数据的持久化.

当主数据库挂掉后,需要把一个从数据库`salveof no one`变成主数据库,把原来的主数据库重启变成新的从数据库,然后数据会同步回来.

### 哨兵

一主多从在整个系统中起到了数据冗余和读写分离的作用.当主数据库挂掉后,可以手动将从数据库变成主数据库.



#### 什么是哨兵

哨兵包括两个功能:

- 监控主数据库和从数据库是否运行正常
- 主数据库挂掉,自动把从数据库变成主数据库

哨兵是一个独立的进程

通常设置两个哨兵,哨兵之间互相监控

建立一个一主二从的集群

建立 sentinel.conf 内容:`sentinel monitor mymaster 127.0.0.1 6379 1` mymaster 是要监控的数据库的名字,名字只能由大小写字母,数字,`. - _`组成,后面是主数据库的地址和端口,1表示最低通过票数

安装:`sudo apt-get install redis-sentinel`

启动:`redis-sentinel /path/to/sentinel.conf`

### 集群


## RabbitMQ

```shell
rabbitmqctl add_vhost v_host_spider
rabbitmqctl add_user spider spider_pwd
rabbitmqctl set_permissions -p v_host_spider spider '.*' '.*' '.*'
```

## postgresql

### 修改 postgres 用户密码

sudo passwd postgresq 

### 添加 postgresql 用户

```
su postgres 

psql -d postgres 

create role dev superuser login password 'smart';
```

### 修改登录验证

```
sudo vim /etc/postgresql/9.5/main/pg_hba.conf

# "local" is for Unix domain socket connections only
local   all             all                                     md5
# IPv4 local connections:
host all all 0.0.0.0/0 md5

sudo vim /etc/postgresql/9.5/main/postgresql.conf

listen_addresses='*'
```

