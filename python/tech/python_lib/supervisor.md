# Supervisor: A Process Control System
Supervisor是一个C/S系统用于监听控制系统进程.


## Overview

### 方便性

rc.d脚本,写起来比较麻烦,并且,rc.d进程在发生错误退出后,不一定会重启

### 确定性

进程的pid具有欺骗性,不能够明确知道进程存活/死亡状态,supervisor中进程作为子进程启动,所有他知道准确的状态

### 进程组

进程可以被分组,并且可以重启说暂停一个进程组

## 组件

### supervisord


### supervisorctl

shell环境,是supervisord的功能子集.通过UNIX domain socket或者TCP链接

### WebServer

### XML-RPC 接口

## 安装

不支持python3

pip install supervisor

### 创建配置文件

`echo_supervisord_conf` 给出一份配置模板

```shell
# 进入root
su
# 添加配置文件
echo_supervisord_conf > /etc/supervisord.conf

# 如果没有root权限.那么配置文件可以不放在/etc下,放在其他地方
echo_supervisord_conf > ~/supervisord.conf
supervisord -c  ~/supervisord.conf
```

## 启动Supervisor

### 添加程序

program区域配置的程序会在supervisord启动的时候启动

```
[program:foo]
command=/bin/cat
```

### 启动supervisord

`supervisord` 会以守护进程启动,并且默认把操作日志写到`$CWD/supervisor.log`

使用`-n`可以不在后台启动,debug时非常有用

修改配置文件时需要`kill -HUP supervisord`

### 命令行参数

- c --configuration FILENAME -- 配置文件路径 如果没有给出,会从当前目录开始寻找
- n --nodaemon -- 不以守护进程启动 (与配置文件中'nodaemon=true'相同)
- u --user USER -- 以某个用户启动supervisord,也可以是uid
- m --umask UMASK -- 守护进程的umask,默认022
- d --directory DIRECTORY -- 守护进程时chadir路径
- l --logfile FILENAME -- 日志文件地址
- y --logfile_maxbytes BYTES -- 使用 BYTES 来限制日志文件大小
- z --logfile_backups NUM -- 当日志达到最大限制时保存多少个备份
- e --loglevel LEVEL -- 日志级别(debug,info,warn,error,critical)
- j --pidfile FILENAME -- 守护进程的进程pid保存文件
- i --identifier STR -- 当前这个supervisord实例的识别码
- q --childlogdir DIRECTORY -- 子进程的日志文件夹
- k --nocleanup --  prevent the process from performing cleanup (removal of
                    old automatic child log files) at startup.
- a --minfds NUM -- 为了成功启动二使用的最小数目的文件描述符
- t --strip_ansi -- 在进程的输出中删除掉ansi编译码
- - minprocs NUM  -- the minimum number of processes available for start success
- - profile_options OPTIONS -- run supervisord under profiler and output
                                results based on OPTIONS, which  is a comma-sep'd
                                list of 'cumulative', 'calls', and/or 'callers',
                                e.g. 'cumulative,callers')


### 启动 supervisorctl

`supervisorctl`会启动一个交互shell

- ?或者help 显示帮助
- `add name [...]`: Activates any updates in config for process/group
- `remove name [...]`: Removes process/group from active config
- `update`: Reload config and then add and remove as necessary (restarts programs)
- `clear name`: Clear a process’ log files.
- `clear name name` : Clear multiple process’ log files
- `clear all`: Clear all process’ log files
- `fg process`:Connect to a process in foreground mode Press Ctrl+C to exit foreground
- `pid`: Get the PID of supervisord.
- `pid name`:Get the PID of a single child process by name.
- `pid all`:Get the PID of every child process, one per line.
- `reread`:Reload the daemon’s configuration files, without add/remove (no restarts)
- `restart name`:Restart a process Note: restart does not reread config files. For that, see reread and update.
- `restart gname:* `: Restart all processes in a group Note: restart does not reread config files. For that, see reread and update.
- `restart name name`:Restart multiple processes or groups Note: restart does not reread config files. For that, see reread and update.
- `restart all`:Restart all processes Note: restart does not reread config files. For that, see reread and update.
- `signal`
- `start name`: Start a process
- `start gname:* `: Start all processes in a group
- `start name name`: Start multiple processes or groups
- `start all`:Start all processes
- `status`:Get all process status info.
- `status name`: Get status on a single process by name.
- `status name name`:Get status on multiple named processes.
- `stop name`: Stop a process
- `stop gname:* `: Stop all processes in a group
- `stop name name`:Stop multiple processes or groups
- `stop all`:Stop all processes
- `tail [-f] name> [stdout|stderr] (default stdout)` :Output the last part of process logs Ex: tail -f name Continuous tail of named process stdout Ctrl-C to exit. tail -100 name last 100 bytes of process stdout tail name stderr last 1600 bytes of process stderr

### 信号

supervisord对信号的处理

- SIGTERM:supervisord and all its subprocesses will shut down. This may take several seconds.
- SIGINT:supervisord and all its subprocesses will shut down. This may take several seconds.
- SIGQUIT:supervisord and all its subprocesses will shut down. This may take several seconds.
- SIGHUP:supervisord will stop all processes, reload the configuration from the first config file it finds, and start all processes.
- SIGUSR2:supervisord will close and reopen the main activity log and all child log files.

## 配置文件

## 环境变量

可以直接使用环境变量
```ini
[program:example]
command=/usr/bin/example --loglevel=%(ENV_LOGLEVEL)s
```

## unix http server

监听unix domain socket.如果没有配置的话,unix domain server不会启动

### file (可空)

domain文件地址,例如:`/tmp/supervisord.sock`.HTTP/XML-RPC请求会发送给他.可以使用`%(here)s`参数,他表示配置文件的地址


### chmod (可空)
 
默认0777, UNIX domain socket权限

### chown (可空)

默认使用启动者和组

socket所属用户和组

### 

### [program:x]

### command


