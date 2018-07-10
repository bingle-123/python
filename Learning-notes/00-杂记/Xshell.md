## 阿里云

1. 阿里云  `APP `监控服务器状态

- 登录阿里云 -->控制台

- 云服务器  `ECS`

- 实例

- 39.104.171.126(公)

  172.24.25.143(私)

  kernel   系统内核  `(centos)   ` ` Windows NT` 内核

- `CentOS`    `RedCat` 的 衍生版  以后企业应用一般都是 红帽子

- root  超级权限管理员     root   密码 : !@#$1234qwer

- Xshell 软件 链接操作服务器   Mac ShellCraft 安装   

- 苹果Mac下载软件网址  xclient.info

# `Xshell `使用

1. 新建会话
2. 指定公网 IP 
3. 返回 密钥指纹 保存
4. shell  人机对话的环境 操作系统内核(centOs)   同过命令控制硬件
5. 命令行提示符
6. bash   (bsh)    (shell 种类)   zsh   csh  
7. 装的东西越多 漏洞越多
8. Linux 的内核是开源的  下载 kernel.org 网站下载 开源内核  第二位(中间)是偶数是稳定版本
9. linux --> 基于 MINIX -- > 基于 UniX       
   - Linux 是通用操作系统
   - 第一台计算机    --> 帕斯卡发明的    Pascal   17岁 
   - 第一台数字计算机  ---差分机---没有软件只有硬件   -- 第一个程序员Ada
   - 第一台电子数字计算机    - ENIAC -  
   - 图灵   程序员  --死于一个毒苹果   --苹果Logo 纪念它
10. 内核是Linux  Linux发行版本    Redhat  Linux  Ubantu 
11. Nginx    -可以把阿里云变为 Web 服务器
    MySQL    -关系型数据库 -持久化数据   
    Redis    - 非关系型数据库
    FTP
    Mail
    防火墙   iptables /filewalls

## 1. 基础命令

```shell
root 提示符是  #
普通用户是  $
who  查看哪些用户登录了系统
whoami 查看自己是谁
w  查看详细信息
clear 清屏     windows  cls
ps  查看内核  查看 shell 种类    bash  zsh csh
	adduser  创建用户 + 用户名
	passwd   + 用户名  回车   输入密码
	logout 断开服务器连接
	reboot  重启服务器   也可以使用 init 6 
	shutdown  关闭服务器   也可以使用 init 0 
uname 查看操作系统	
hostname  主机名 
tab tab 自动补全功能

查看帮助
	man shutdown   查看命令的使用手册    man + 命令
	info  + 命令    专业角度详细解释命令
	命令 --help  查看帮助
	whatis + 命令名 查看简短的秒数 
	apropos
	-   --  命令后面的参数
pwd 打印当前工作目录
	/root root用户是的根目录
	其他用户的是  /home/用户名   不是超级管理员的都在home下
which + python  那个是python 找到python解释器的位置
whereis+文件/应用  查看文件/应用所在的目录


```

## 2. 命令 模式  身份切换

1. `sudo`  扮演超级管理员身份
2. `su` + 用户名  切换用户
3. 命令 [参数]|[对象]

+++

##  **`文件创建删除`**

1.  ~ 当前用户的主目录  `pwd` 查看当前用户主目录  `print working directory`

2. `mkdir `创建文件夹  `make directory` 

3. `rmdir` 删除文件夹

4. #### `ls `查看文件夹   `list directory contents`

   1. `ls -l  ` 查看完整的文件目录详情    列表开头是d 开始的都是问价夹
   2. touch 创建空文件  `touch hello.py`    修改文件的访问时间戳  (访问时间改变)
      - touch 可以修改每个文件的时间参数
      - 文件参数
        - 修改参数修改内容    
        - 访问权限   
        - 最后访问时间
   3. `ls -a  ` 查看所有文件       以  .  开头的文件和文件夹都是隐藏文件
   4. `ls -la  `查看所有信息  长格式所有文件
   5. `ls --help | less  `少显示
   6. `ls -d   `显示问价夹
   7. `ls -r    reverse `  反转显示    按首字母反序显示
   8. `ls -R  `平铺式显示文件   所有文件夹都展开显示  `reucrsive ` ()递归)

5. #### 进入目录文件   `cd`  + 文件名

   1. 回到上级目录  `cd ..  `相对路径   也可以用绝对路径  `cd /home/目录名  `
   2. `cd ~ `回到用户主目录
   3. `cd /   ` 系统根目录  


   - 默认能保存 1000 条
        echo 回声命令
           echo 'print("hello")' > hello.py

   12. #### 剪切 mv   move    也可以用于改名字   原文件夹移动

   13. Ctrl + c 终止命令

   14. #### jobs   查看有没有后台程序

       1. fg  %1 将一号任务放在前台使用 
       2. bg %1 将任务放回后台
       3. ctrl + z  停止任务

   15. top 查看CPU占用率

   16. wc    查看行数  单词书  字节数   word count     -l 查看行数 -w 单词数

   17. uniq 去除相邻的重复内容  只是显示了排序后的结果 ,原文件不会改变

   18. #### sort 排序 字母顺序  中文按照编码排序

   ```Python
   for value in range(0x4e00, 0x9fa6):
       print(chr(val))   # 打印所有中文
   ```

   ```

 
   ```

  4. #### wget + 网址   网络下载文件
      wget -O + 文件名 + 地址   将文件放在哪个位置

   5. #### cat  查看文件内容 concatenate    cat + 文件名

      1.  cat  文件名 | less / more   分页查看   | 添加管道
      2.  cat + meminfo     内存信息    cat + cpuinfo cpu信息
      3.  head 查看文件开头    head 文件名 - n   查看开头多少行
      4.  tail 文件结尾   -n 
      5.  find -name *.html查找文件   在当前路径下查找文

  6. #### grep 查找字符串 在一段字符串中

      1. cat 文件名 | grep  查找内容 可加正则表达式
      2. grep + 查找的内容 + 文件名 -n  出现在多少行
      3. grep  查找内容     . / -n  当前路径下是所有文件下查找
      4. grep  查找内容   >  文件名 &  将查找的内容输出重定向 后台执行    在在后面加    2> error.txt   将错误输出写入到error.txt中   (f覆盖模式)
        < 输入重定向
      5. \>> 文件名   追加模式   

   7. **rmdir 删除文件夹**

   8. **rm   删除文件 和文件目录**

      1. rm -f 强行删除
      2. rm -r 递归删除
      3. rm -i  interactive  询问递归删除
      4. rm -rf  递归强行删除    危险操作  

   9. **复制文件  cp     cp  文件名   要复制到文件目录 / 复制后的文件名**

   10. **history 输入命令记录   !num 再次输入**
   - 默认能保存 1000 条   可修改
        echo 回声命令
           echo 'print("hello")' > hello.py

      12. **剪切 mv   move    也可以用于改名字   原文件夹移动**
      13. Ctrl + c **终止命令**
      14. **jobs   查看有没有后台程序**
       1. fg  %1 将一号任务放在前台使用 
       2. bg %1 将任务放回后台
       3. ctrl + z  停止任务
      15. **top 查看CPU占用率**
      16. **wc    查看行数  单词书  字节数   word count     -l 查看行数 -w 单词数**
      17. **uniq 去除相邻的重复内容  只是显示了排序后的结果 ,原文件不会改变**
      18. **sort 排序 字母顺序  中文按照编码排序**
      19. **`diff ` **比较文件的不同   版本比较
     20. `file `查看文件的性质`text `  编码方式 
     21. `date`  `cal `日历    `script` 录制脚本   给用户发消息  `write`    `wall` 给所有人发出警告   `mesg` 控制要不要接受消息 y / n 

   ```Python
   for value in range(0x4e00, 0x9fa6):
       print(chr(val))   # 打印所有中文
   ```



## 1.` echo  ssh scp usrdel ln`

1.  **echo **回声命令  可以创建文件并写入内容
   1. echo  `' print("hello")' > hello.py `  创建文件 并写入内容
   2. echo  `$a`   取`变量` a 的值  `已设置  a = 2`
   3. `echo  $((a + b)) `计算   a + b 的值
   4. `echo  $HISTSIZE`查看历史记录条数
   5. `HISTSIZE=2000`设置保存的历史指令的条数
2.  **`usrdel`删除用户**
3. `ssh root@IP`地址   远程连接其他服务器    wall 超级管理员发警告
4. `scp `安全拷贝      可以从其他服务器里拷贝东西  
   - **`scp 原文件 目标文件  hellokitty@ip :/home/hellokitty`**
5. `cat /etc/centos-release` 查看操作系统的版本
6. **`ls -l | grep hello` 加管道过滤 只显示有 hello的**
7. **`find` 找文件本身    `grep `找文件的内容**

##  2. 链接(备份) 

**硬链接**   `ln`   更改之后所有的都改变了

-  没有拷贝文件  ,不消耗内存, 只是创建一个链接引用文件


- 给文件创建引用   `ln  文件名 要备份到的位置和新的文件名`


- 只要对象有引用  垃圾回收不会回收文件,文件不会被删除
- `ls -l  文件名`查看文件的**状态**  链接的个数 链接为  1  `rm`会被删除
- 硬链接数表示文件被备份多少份   链接数是 1 时删除会被删除

**软链接**   `ln -s`

- ` ln -s  文件位置   软链接名  ` 给文件创建软链接 

## 3. 压缩 归档文件

**压缩**

1. `gzip`**压缩文件**     压缩比

2. `gunzip`  +文件名**解压缩文件** `后缀是.gz` 的文件  

   - `gz` 解压缩    

3.  `xz`  将 后缀是 `.xz`格式的文件解压缩    

   -  `-z  ` 压缩 后面  加` - 8` 指定压缩比 
   - ` -d`  解压缩  

   **归档**

4. `tar  -tf  ` 查看归档文件的内容

   - **`tar -cvf  all.tar *` **归档文件   将文件归档到all.tar 中  
     - `*` 表示将所有文件归档到一个文件中
     - 也可以写文件路径
   - **`tar -xvf`** 解归档   把一个文件 拆成多个文件
     - `-v  `列出过程   不加也可以 
     - `-f `指定文件名

### **快捷键  别名** `alias` 

1. 指令的别名
   - `alias ll='ls -l' ` `ll`是 一个别名
   - `unalias ll` 取消设置的别名
2. `~/.bashrc` 修改文件设置内容

## 4. **vim 文本编辑器**

1. **启动和退出**

   - `vim + 文件名` 打开或创建文件

2. **命令模式和编辑模式**

   - `i / a `进入编辑模式
   - `Esc`退出编辑模式 进入命令模式
   - w 保存   q 退出      q! 强行退出

3. **定标操作**

   - `G ` 去末尾
   - `gg `回到开始   行号 + `gg` 光标移到某行

4. **文本操作**

   - `:   `进入末行模式    `set nu` 出现行号


   - 复制代码  `yy + 数字 多少行`
   - 粘贴  `p`
   - `dd` 删除 + 数字  删除行
   - `Ctrl   `
     * `e `后一行  ` y `前一行
     * `f  `前一页 ` b `后一页

5. **查找和替换**

   - 正则

6. **参数设定**

7. `vim .vimrc `修改设置 `set nu   syntax off ts=4``vim .vimrc `修改设置 `set nu   syntax off ts=4``vim .vimrc `修改设置 `set nu   syntax off ts=4`

8. 删除单词    光标在第一个单词  ` dw `

9. **vim 编辑快捷键**

   ```shell
   进入 末行模式    编辑快捷键
   inoremap pymain if __name__ == '__main__':    
   i 编辑模式用的快捷键   nore 不要递归  map 映射
   d$ 删除贯标处到行位
   !加命令   执行系统命令
   / 搜索的内容  n 下一处  N 上一处
       可以加正则表达式   /\w\+ 需要转义  量词要加反斜杠
   替换
   	末行模式 :1,10s/替换前的元素/替换后的元素/替换模式
      s 替换
      替换模式 g global  i ignore 忽略大小写
   ```

   ```python
   scores = []
   the_max, *marks, the_min = scores   # 去除第一个和最后一个元素
   ```

10. 高级技巧

   - 映射快捷键
   - 录制宏

## 要点

```shell
映射快捷键 vim映射快捷键  inoremap key 
yum装软件 yum  install/remoov     
	list installed  查看安装过的软件
	yum search  查找
	yum update 更新
nginx  变为http服务器   命令行  输入 nginx
ps -ef /-aux  显示进程列表  | grep nginx
强行结束进程   kill -9 + 进程号  强行结束
netstat -nap|grep 80   查看网络端口80    p 查看进程号
```



**other**

- !v   把刚才执行过的以 `v`  打头的命令再执行一次
- `rw-` 文件的所有者权限 `r--` 同组用户权限 `r--` 其他用户的权限

```shell
rw- 不能执行文件   +x  ./文件名 执行文件
rex  r-x   r-x  文件所有者可以读 写 执行(execute) 其他能读和执行
chmod u+x + 文件名  加执行权限 
chmod o+x,g+x 文件名   给同组用户 其他用户添加执行权限
chmod 777 + 文件名   所有人都有读写权限  二进制  
rwx  rwx  rwx    rwx rw- rw- rwx r-- r--  rw- -wx  -wx 
111  111  111    111 110 110 111 100 100  110  011  011
7    7    7       7   6  6   7   4   4     6    3    3
4 只读   5 读 执行  6 读写  7 读写执行
```



```shell
vim 中文    在中文字符串前加  u
文件开头  #encoding: utf-8   #!/usr/bin/python3
意外退出 提示  d + delate 不恢复文件
```

创建可执行的文件的快捷软链接`ln -s ~/guess.py ~/bin/guess`  或者`/usr/bin/guess`

`fdisk -l` 查看磁盘使用情况

## 5. 升级 python 2 -> 3

```shell
官网  下载Linux 原代码  source   带b的是测试版
解压缩  xz -d    tar -xvf 

源代码构建安装 
cd Python-3.6
yum install gcc  安装gcc
gcc --version
make --version  构建工具

安装依赖库（因为没有这些依赖库可能在源代码构件安装时因为缺失底层依赖库而失败）。
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel

切换至Python源代码目录并执行下面的命令进行配置和安装。
cd Python-3.6.1
./configure --prefix=/usr/local/python3.6 --enable-optimizations
创建软链接
ln -s /usr/local/python3.6/bin/python3 /usr/bin/python3


make && make install
configure
make  && make install    前面的成功后执行后面的

符号链接  ln -s /usr/local/

```



## 6. 安装软件

```
yum / rpm
压缩文件安装tar.gz / tar.xz
	-src  源代码构建安装  make && make install
	- bin 注册环境变量安装   重启服务器会失效
	解压后有 bin 文件有二进制程序可以跑
	但是韩式要注册path环境变量将 bin 复制到path环境变量中 echo $PATH(查看环境变量)
	 root: export PATH=$PATH:+bin的目录 增加
	 
	 永久有效
	 查看 ~ 所有文件  隐藏文件.bash_profile文件
	 vim .bash_profile
	 在 PATH 里添加 bin文件目录
hell.sh shell 脚本格式文件 实现自动化操作
	写入命令 更改为可执行格式 +x 然后执行
```



### yum 

- `yum` `yellowdog upgrade modified`   包管理工具
  -  前身  rpm  `redhat package manager`  
  -  yum 服务器仓库
- `yum list insatlled | grep Nginx`
- `yum search Nginx` 找网络有没有资源
- `yum install nginx`
- yum update 更新


- 反向代理


### rpm  

- **红帽子包管理工具**


-  `rpm -i `安装  +`vh`
-  `rpm -e` 移除  +` vh`
- `rpm -vh` 查看安装过程
- `rpm -qa `查询所有 搜索软件包
-  `-rpm -e` 移除

### `xargs` 参数化

- `rpm -qa | grep jdk | xargs rmp -e` 将`grep` 搜索到的结果 `xargs`(作为参数用来) 进行后面的操作

## 7. `nginx` HTTP服务器

### 1.介绍

- `Apache`     `LAMP` `Linux Apache MySQL PHP`  做网站黄金组合

  - **Apache HTTP Server**（简称[**Apache**](https://baike.baidu.com/item/Apache/6265)）是[Apache软件基金会](https://baike.baidu.com/item/Apache%E8%BD%AF%E4%BB%B6%E5%9F%BA%E9%87%91%E4%BC%9A)的一个开放源码的网页服务器，可以在大多数计算机操作系统中运行，由于其多平台和安全性被广泛使用，是最流行的Web服务器端软件之一。它快速、可靠并且可通过简单的`API`扩展，将`Perl/Python`等解释器编译到服务器中。

- `Nginx`      `LNMP`   `LInux Apache MySQLO Python` 现在最快组合

  - `Nginx `是一个很强大的高性能[Web](https://baike.baidu.com/item/Web/150564)和[反向代理](https://baike.baidu.com/item/%E5%8F%8D%E5%90%91%E4%BB%A3%E7%90%86)服务器，它具有很多非常优越的特性：

    在连接高并发的情况下，`Nginx`是[Apache](https://baike.baidu.com/item/Apache/6265)服务器不错的替代品：`Nginx`在美国是做虚拟主机生意的老板们经常选择的软件平台之一。能够支持高达 50,000 个并发连接数的响应，感谢`Nginx`为我们选择了 `epoll and kqueue`作为开发模型。

`DNS` 将域名翻译成`IP`地址

域名备案流程: 

### 2.停机

`nginx -s stop `停止

## 8. 阿里云防火墙处理

- 实例 -> 管理 -> 实例安全组 -> 内网入方向规则

  - 安全组列表  ->配置规则  -> 入方向 -> 容许 ->  HTTP(80)
    - 授权对象 0.0.0.0

- 替换页面

  - `/usr/share/nginx/html  ` 进入页面目录
  - `404 /50x`
  - `config`文件  server  连接端口  
    - `cd /etc/nginx/  `  下面的 `nginx.config` 配置文件
    -  页面路径  root ..

- 上传文件

  -  先安装`Xftp.exe`     点击上传到`/usr/share/nginx/html `

  苹果下:  打开终端      输入命令:  `sftp`  root@公网`IP`

  - 连接成功 `  sftp>  ls  `      列出目录   get + 文件 下载文件
  - put 上传    put + 文件名



集群技术 分摊请求  负载均衡

-  `LVS + keepalice `将普通服务器改为负载均衡服务器
- ​

## 去`IOE`运动

2008 阿里巴巴   去`IOE`运动  多台小型机器 组装可以构成性能好的服务器

IBM  小型机

Oracle  数据库

- - `GFS/TFS/Tair  ` 自制 的数据存储系统    

`EMC(HP) `存储设备

Java  Spring框架

## 9.进程处理

- 查看进程
  - `ps -ef|grep ssh` 查看进程

## 10. Linux系统防火墙

### 1.自带防火墙

- `systemctl start firewalld`/ `iptables`启动防火墙


- `firewall -cmd` 配置防火墙    开端口`--add-port=80/tcp  -- permanent -zone=public`
- 企业级防火墙  两层防火墙 DMZ -`Demilitary zone`

### 2.`iptables`防火墙设置

- `iptables -L -n` 查看防火墙设置

- `iptables -F`清除预设表filter中的所有规则链

- `iptables -X`清除预设表filter中使用者自己设置的规则

- 设定预定规则

  - `[root@tp ~]# iptables -P INPUT DROP`

    `[root@tp ~]# iptables -P OUTPUT ACCEPT`

    `[root@tp ~]# iptables -P FORWARD DROP`
    **上面的意思是,当超出了IPTABLES里filter表里的两个链规则(INPUT,FORWARD)时,不在这两个规则里的数据包怎么处理呢,那就是DROP(放弃).应该说这样配置是很安全的.我们要控制流入数据包**

    **而对于OUTPUT链,也就是流出的包我们不用做太多限制,而是采取ACCEPT,也就是说,不在着个规则里的包怎么办呢,那就是通过.**

    **可以看出INPUT,FORWARD两个链采用的是允许什么包通过,而OUTPUT链采用的是不允许什么包通过.**

    **这样设置还是挺合理的,当然你也可以三个链都DROP,但这样做我认为是没有必要的,而且要写的规则就会增加.但如果你只想要有限的几个规则是,如只做WEB服务器.还是推荐三个链都是DROP.**

   ```shell
  添加规则.
  首先添加INPUT链,INPUT链的默认规则是DROP,所以我们就写需要ACCETP(通过)的链
  为了能采用远程SSH登陆,我们要开启22端口.
  [root@tp ~]# iptables -A INPUT -p tcp --dport 22 -j ACCEPT
  [root@tp ~]# iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT (注:这个规则,如果你把OUTPUT 设置成DROP的就要写上这一部,好多人都是望了写这一部规则导致,始终无法SSH.在远程一下,是不是好了.
  其他的端口也一样,如果开启了web服务器,OUTPUT设置成DROP的话,同样也要添加一条链:
  [root@tp ~]# iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT ,其他同理.)
  如果做了WEB服务器,开启80端口.
  [root@tp ~]# iptables -A INPUT -p tcp --dport 80 -j ACCEPT
  如果做了邮件服务器,开启25,110端口.
  [root@tp ~]# iptables -A INPUT -p tcp --dport 110 -j ACCEPT
  [root@tp ~]# iptables -A INPUT -p tcp --dport 25 -j ACCEPT
  如果做了FTP服务器,开启21端口
  [root@tp ~]# iptables -A INPUT -p tcp --dport 21 -j ACCEPT
  [root@tp ~]# iptables -A INPUT -p tcp --dport 20 -j ACCEPT
  如果做了DNS服务器,开启53端口
  [root@tp ~]# iptables -A INPUT -p tcp --dport 53 -j ACCEPT
  如果你还做了其他的服务器,需要开启哪个端口,照写就行了.
  上面主要写的都是INPUT链,凡是不在上面的规则里的,都DROP
  允许icmp包通过,也就是允许ping,
  [root@tp ~]# iptables -A OUTPUT -p icmp -j ACCEPT (OUTPUT设置成DROP的话)
  [root@tp ~]# iptables -A INPUT -p icmp -j ACCEPT    (INPUT设置成DROP的话)
  允许loopback!(不然会导致DNS无法正常关闭等问题)
  IPTABLES -A INPUT -i lo -p all -j ACCEPT (如果是INPUT DROP)
  IPTABLES -A OUTPUT -o lo -p all -j ACCEPT(如果是OUTPUT DROP)
  下面写OUTPUT链,OUTPUT链默认规则是ACCEPT,所以我们就写需要DROP(放弃)的链.
  减少不安全的端口连接
  [root@tp ~]# iptables -A OUTPUT -p tcp --sport 31337 -j DROP
  [root@tp ~]# iptables -A OUTPUT -p tcp --dport 31337 -j DROP
  有些些特洛伊木马会扫描端口31337到31340(即黑客语言中的 elite 端口)上的服务。既然合法服务都不使用这些非标准端口来通信,阻塞这些端口能够有效地减少你的网络上可能被感染的机器和它们的远程主服务器进行独立通信的机会
  还有其他端口也一样,像:31335、27444、27665、20034 NetBus、9704、137-139（smb）,2049(NFS)端口也应被禁止,我在这写的也不全,有兴趣的朋友应该去查一下相关资料.
   ```

当然出入更安全的考虑你也可以包OUTPUT链设置成DROP,那你添加的规则就多一些,就像上边添加
允许SSH登陆一样.照着写就行了.

下面写一下更加细致的规则,就是限制到某台机器
如:我们只允许192.168.0.3的机器进行SSH连接
[root@tp ~]# iptables -A INPUT -s 192.168.0.3 -p tcp --dport 22 -j ACCEPT
如果要允许,或限制一段IP地址可用 192.168.0.0/24 表示192.168.0.1-255端的所有IP.
24表示子网掩码数.但要记得把 /etc/sysconfig/iptables 里的这一行删了.
-A INPUT -p tcp -m tcp --dport 22 -j ACCEPT 因为它表示所有地址都可以登陆.
或采用命令方式:
[root@tp ~]# iptables -D INPUT -p tcp --dport 22 -j ACCEPT
然后保存,我再说一边,反是采用命令的方式,只在当时生效,如果想要重起后也起作用,那就要保存.写入到/etc/sysconfig/iptables文件里.
[root@tp ~]# /etc/rc.d/init.d/iptables save
这样写 !192.168.0.3 表示除了192.168.0.3的ip地址
其他的规则连接也一样这么设置.

在下面就是FORWARD链,FORWARD链的默认规则是DROP,所以我们就写需要ACCETP(通过)的链,对正在转发链的监控.
开启转发功能,(在做NAT时,FORWARD默认规则是DROP时,必须做)
[root@tp ~]# iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
[root@tp ~]# iptables -A FORWARD -i eth1 -o eh0 -j ACCEPT
丢弃坏的TCP包
[root@tp ~]#iptables -A FORWARD -p TCP ! --syn -m state --state NEW -j DROP
处理IP碎片数量,防止攻击,允许每秒100个
[root@tp ~]#iptables -A FORWARD -f -m limit --limit 100/s --limit-burst 100 -j ACCEPT
设置ICMP包过滤,允许每秒1个包,限制触发条件是10个包.
[root@tp ~]#iptables -A FORWARD -p icmp -m limit --limit 1/s --limit-burst 10 -j ACCEPT
我在前面只所以允许ICMP包通过,就是因为我在这里有限制.

二、配置一个NAT表放火墙
1,查看本机关于NAT的设置情况
[root@tp rc.d]# iptables -t nat -L
Chain PREROUTING (policy ACCEPT)
target      prot opt source                destination         
Chain POSTROUTING (policy ACCEPT)
target      prot opt source                destination         
SNAT        all    --    192.168.0.0/24        anywhere              to:211.101.46.235
Chain OUTPUT (policy ACCEPT)
target      prot opt source                destination   
我的NAT已经配置好了的(只是提供最简单的代理上网功能,还没有添加防火墙规则).关于怎么配置NAT,参考我的另一篇文章
当然你如果还没有配置NAT的话,你也不用清除规则,因为NAT在默认情况下是什么都没有的
如果你想清除,命令是
[root@tp ~]# iptables -F -t nat
[root@tp ~]# iptables -X -t nat
[root@tp ~]# iptables -Z -t nat

2,添加规则
添加基本的NAT地址转换,(关于如何配置NAT可以看我的另一篇文章),
添加规则,我们只添加DROP链.因为默认链全是ACCEPT.
防止外网用内网IP欺骗
[root@tp sysconfig]# iptables -t nat -A PREROUTING -i eth0 -s 10.0.0.0/8 -j DROP
[root@tp sysconfig]# iptables -t nat -A PREROUTING -i eth0 -s 172.16.0.0/12 -j DROP
[root@tp sysconfig]# iptables -t nat -A PREROUTING -i eth0 -s 192.168.0.0/16 -j DROP
如果我们想,比如阻止MSN,QQ,BT等的话,需要找到它们所用的端口或者IP,(个人认为没有太大必要)
例：
禁止与211.101.46.253的所有连接
[root@tp ~]# iptables -t nat -A PREROUTING    -d 211.101.46.253 -j DROP
禁用FTP(21)端口
[root@tp ~]# iptables -t nat -A PREROUTING -p tcp --dport 21 -j DROP
这样写范围太大了,我们可以更精确的定义.
[root@tp ~]# iptables -t nat -A PREROUTING    -p tcp --dport 21 -d 211.101.46.253 -j DROP
这样只禁用211.101.46.253地址的FTP连接,其他连接还可以.如web(80端口)连接.
按照我写的,你只要找到QQ,MSN等其他软件的IP地址,和端口,以及基于什么协议,只要照着写就行了.

三、最后
drop非法连接
[root@tp ~]# iptables -A INPUT    -m state --state INVALID -j DROP
[root@tp ~]# iptables -A OUTPUT    -m state --state INVALID -j DROP
[root@tp ~]# iptables-A FORWARD -m state --state INVALID -j DROP
允许所有已经建立的和相关的连接（必须配置否则httpd无法连接）
[root@tp ~]# iptables-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
[root@tp ~]# iptables-A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
[root@tp ~]# /etc/rc.d/init.d/iptables save

这样就可以写到/etc/sysconfig/iptables文件里了.写入后记得把防火墙重起一下,才能起作用．

[root@tp ~]# service iptables restart
   ```



## 10.定时任务

### 1.介绍

- 通过crontab 命令，我们可以在固定的间隔时间执行指定的系统指令或 shell script脚本。时间间隔的单位可以是分钟、小时、日、月、周及以上的任意组合。这个命令非常适合周期性的日志分析或数据备份等工作。

### 2.命令

- `contab [-u user] file  crontab [-u user ][-e |-l | -r]`
- -u user：用来设定某个用户的crontab服务；
- file：file是命令文件的名字,表示将file做为crontab的任务列表文件并载入crontab。如果在命令行中没有指定这个文件，crontab命令将接受标准输入（键盘）上键入的命令，并将它们载入crontab。
- -e：编辑某个用户的crontab文件内容。如果不指定用户，则表示编辑当前用户的crontab文件。
- -l：显示某个用户的crontab文件内容，如果不指定用户，则表示显示当前用户的crontab文件内容。
- -r：从/var/spool/cron目录中删除某个用户的crontab文件，如果不指定用户，则默认删除当前用户的crontab文件。
- -i：在删除用户的crontab文件时给确认提示。

### 3.更改设置

- 





## 11. `MySQL`

### 1.安装

* 介绍
  * `mysqle.com` 官网
  * 已经不是开源的软件了
* 安装
  * 社区版  `mysql community server `
    * `mariadb` `mysql`分支 ,作者做的另外一个版本
    * `yum install mariadb-server mariadb`
  * `rpm -ivh mysqle`
* .so 静态库文件后缀
* 启动服务器  `systemctl start mariadb `
* `ps -ef |grep mysql `查找进程
* `netstat -nap | grep 3306 `查看`mysql`的端口情况
* `netstat -nap | grep 3306`
* `systemctl status mariadb`  查看状态

`mysqld`     `d` 守护进程  后台进程

**以前的 5.x 版本用 `service` 代替 `systemctl`**

服务器专用    HTTP服务器 和其他的不能同时使用







### 3.进入`mysql`

* `mysql -u root -p`  `mysql` 的超级管理员初次登录密码是空的
* `qwertyyuiop8`
* 退出  quit

### 4.停止服务

- `systemctl stop mariadb`


- `nginx -s stop `停止



### 5.开机自启

- `systemctl enable mariadb`
- 停止开机自启
  -  ` systemctl disable mariadb`  或者 `删除符号链接`
- `centos6用 ``checkconfig` `serveice`配置开机自启

## 12.`redias` 数据库

### 1.下载

- 下载到的是源代码
- 

### 2.构建安装

### 2.1 下载

- 进入解压后的目录 有目录`Makfile 目录`
- 构建  `make`
- 安装 `make install`     (make && make install)

### 2.2 改配置文件   `redias.config`

- 进入`redias`文件夹
- 复制  `redias.config`
- 更改 61行  bind:
  - 原来绑定的是本机 
  - 改为的阿里云内网地址(末行模式 `!ifconfig `查看` inet `)172.24.25.143
- 84行 为端口 默认设置是 6379, 可自己更改
- `:/require  (搜索)  ` 480行 去注释  改pass 密码: `qwertyuiop8`

### 2.3 启动

- `redis-server myredis.config > myredis.log &`

### 2.4 连接

- `redis-cli -h 172.24.25.143(内网地址) -p 6379(端口号)`
- 进入后输入`auth + 密码 `


- 退出
  -  将后台移到前台   `ctrl + c `保存数据退出
  - `fg %1 `移动到前台
  - `bg %1` 移动到后台启动





# shell脚本编辑

- 变量定义
  - 数字字母下划线, 不能数字开头,不能使用关键字
  - 使用定义过的变量只要在变量名前加  $ 即可
  - $(ls ) 将当前目录下的文件遍历出来
-  去变量值  $
- 变量边界 ${}
- 子符长度${#}
- 去元素   ${数组名[下标]}

## `$`的使用

- `$#`传递到脚本的参数
- `$*`以一个单字符串显示向脚本传递的参数,  即 传递给脚本的参数组装
- `$$`脚本运行的进程号
- `$!`后台运行的最后一个进程号

## `test`命令

### 数值测试

- `-eq ` 等于则为 true  ` equal`
- `-ne `不等于 true   `not equal`
- `-gt`  大于为true  `great`
- `-ge `大于等于 true ` great equal`
- `-lt `小于 true  `little`
- ` -le `小于等于 true     `little equal`

### 字符串测试

=    !=   -z    字符串长度为0   -n  字符串长度不为0

### 文件测试

- -e 文件存在  true
- -r 可读文件
- -w 可写文件
- -x 可执行
- -s 文件至少有一个字符
-  -d 文件存在且为目录
- -f 文件为普通文件
-  -c 文件为特殊文件 
- -b 文件为块特殊文件

 















# 0000

### Python

### `heapq`

### `sys`

- 命令行参数  在输入命令是给的参数 
- `sys.argv`  接受所有的参数  保存在数组中

### `yield` 

​```python
# 生成式   列表已存在,占用空间大
list1 = [x for x in range(10)]

#生成器    得到的是 generator  对象 引用 
list3 = (x for c in range(10))
for i in list3:   # 在需要用的时候再计算出值
    print(i)
   
# 生成器函数
def fibo(n):  #普通函数 
    a, b = (0, 1)
    for _ in range(n):
        a, b = b, a + b
    return a

def fibo(n):  #生成器函数   保留上次计算的值 不会重复计算 
    a, b = (0, 1)
    for _ in range(n):
        a, b = b, a + b
    	yield a

   ```

```python
string.center(占据的位置大小, [,空位填补])
string.ljust()
string.rjust()
# 二选一列表
[[0], [1]][True] = [1]
[[0], [1]][False] = [0]

```



#### 英语 美国 美式键盘 默认

raw_input()  输入

## `bootstrap cdn` 下载4.x版本

[] 找到列表中第二大元素

[]列表字符串重复次数前3 的找出来



I/O 操作会中断`cpu`, 防止`cpu` 被频繁的打断 ,会将频繁输出的内容放在输出缓存区里, 等缓存区存满才会输出

flush=True 刷新缓冲区





计算机文化

## python 函数

- abs()
- all()
- any()
- ascii()
- bin()
- boll()
- bytearray()
- bytes()
- zip() 将多个容器变为一个容器



### 处理数据

1. filter() 过滤
2. map() 映射
3. reduce  归约操作
4. zip() 将两个容器变为一个容器

### python3 -m IPython  

- 启动ipython



## Git

- windows

```shell
切换到目录
git init 将文件夹变文本地仓库
notepad test.txt 创建文件
git add + filename    git add . 将当前文件目录的所有文件添加版本控制
初次要设置用户名和邮箱
 git config --global user.name 'zhang'
 git config --global user.email 'zhang.email'
本地仓库
git commit -m "修改的内容,提交的原因"
git status 查看暂存区状态, 有没有修改文件 -commit 提交
git log 查看日志

回到历史版本
git reset --hard  版本号的前六位
git reflog 查看历史日志

git log --pretty=oneline  单行查看日志

撤回暂存区内容
git checkout --文件名(不加表示撤掉所有)
修改之后重新提交

Gitlab 可以自己搭建服务器
```

###  克隆

```
git clone  url 在桌面克隆一个远程仓库
add . 
commit -m
git push origin master (origin 项目的别名) 将项目提交到主干上面
git pull 从远端同步到本地
```

### 添加远端仓库

- 将本地仓库 添加到远端仓库
- `git remote add origin url`
- 提交   `git -u origin master` 第一次使用加  -u

### 本地建仓库提交到远端

- `makdir hello`
- `cd hello`
- `git init`
- `git add .`
- `git status`
- `git commit -m  ""说明"`
- `git log `

重置版本

- `git reset --hard   id`
- `git reflog`
- `git remote add origin (url)`
- `git push -u origin master`
- `git pull  (url)`

#### 远端已存在的项目

- `git clone (url)`
- `cd hello `
- `git add .`
- `git checkout  --`
- `git commit -m  "说明"`
- `git push origin master`
- `git pull`



### git 使用流程

- `git cone <url>`
- `cd <dir>`


- `git branch  分支名 `   创建
- `git checkout 分支名 `  切换
- 合并   切换到`master `分支
  - `git merge  cool-function `将分支合并到master
  - `git push origin master`



生成的静态文档的页面

- `jekyll `生成页面  
- `hexo ` `(bootcss)`里面  

在`linux `

- 安装   `git scm`
- linux  <!---->