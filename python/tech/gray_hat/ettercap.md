# Ettercap

Ettercap刚开始只是作为一个网络嗅探器,但在开发过程中,它获得了越来越多的功能,在中间的攻击人方面,是一个强大而又灵活的工具.它支持很多种协议(即使是加密的),包括网络和主机产品特征分析.

它主要有2个嗅探选项:

UNIFIED,这个模式可以嗅探到网络上的所有数据包,可以选择混杂模式(-p选项).如果嗅探到的数据包不是ettercap主机的就自动用第3层路由转发.所以,你可以用不同的工具作中间人攻击(MITM)然后使用ettercap修改并转发数据包.系统内核ip_forwarding的转发功能默认是被ettercap禁用的.这是网关上的干扰行为.这样做的目的是为了防止一个数据包被转发两次,这是一种网关攻击行为,所以,我们推荐在geteways ONLY和UNOFFENSIVE MODE ENABLED的模式下使用ettercap.在ettercap开始监听一个网络接口之后,启用了网关攻击模式,数据包就不会由路由器转发到第二个接口.

BRIDGED,这个模式采用的是双网卡,在进行嗅探病过滤内容时将数据从其中一个网卡传输到另一个网卡.因为这种嗅探方式隐藏的,因为没有方法找出网络上的中间人,可以看做是第1层攻击,这样你就成为了网络上两个合法实体的中间人.不要在网关使用它,否则他会把从网关转发到网桥.提示：你可以使用content过滤引擎来丢弃不需要被转发的数据,这种方式在ettercap中成为一个内联IPS

你可以在UNIFIED模式下使用中间人攻击.可以选择喜欢的攻击方式模块,这些模块是独立与ettercap的嗅探和过滤进程的.所以你可以同时启动多个攻击模块,或者使用自己的工具.关键是:到达ettercap的数据包必须包含正确的mac地址和不同的ip(只有这些数据包才会被转发)

## ettercap的特性

- SSH1:可以嗅探到账户和密码,包括SSH1连接中的数据.
- SSL:可以嗅探ssl数据,伪造的证书会发送给目标,并且回话是加密的
- 链接中注入字符:可以向服务器或者客户端链接中注入数据,来模拟响应或请求
- 数据包 过滤或丢弃:可以给TCP或者UDP有效payload中的特定字符串(甚至是16进制)设置一个过滤脚本来替换为你自己的或者直接丢弃掉数据包.过滤引擎可以匹配网络协议的任何字段,并且随意更改数据
- Remote traffic sniffing through tunnels and route mangling:You can play with linux cooked interfaces or use the integrated plugin to sniff tunneled or route-mangled remote connections and perform mitm attacks on them.
- Plug-ins support:可以使用ettercap的api创建自己的插件
- Password collector for:嗅探一下密码TELNET, FTP, POP, RLOGIN, SSH1, ICQ, SMB, MySQL, HTTP, NNTP, X11, NAPSTER, IRC, RIP, BGP, SOCKS 5, IMAP 4, VNC, LDAP, NFS, SNMP, HALF LIFE, QUAKE 3, MSN, YMSG
- Passive OS fingerprint:可以被动的扫描网络(不用发送任何数据包),并且获得网络上主机的具体信息:操作系统,运行的服务,打开的端口,IP,mac地址和网络适配器
- Kill a connection:关闭一个连接

## 目标说明

没有明确的来源于目标的定义.两个目标是用来过滤从一个发送到另一个的数据流量,或则反向发送的数据,因为他们是全双工通信

目标格式是`MAC/IPs/PORTs`,任何一部分默认都是全部,所以你可以省略其中一个,或两个.例如:`//80`表示任何MAC任何IP的80端口;`/10.0.0.1/`表示任何MAC地址但是只有IP是10.0.0.1并且是任何端口

MAC地址必须是唯一的,格式是`00:11:22:33:44:55`

IP是一个范围,可以使用`-`表示某个区间,可以使用`,`表示单个不同的ip,可以使用`;`表示不同的ip.例如:`10.0.0.1-5;10.0.1.33`表示`10.0.0.1,2,3,4,5`和`10.0.1.33`

PORTs也是范围可以用`-`表示某个区间,使用`,`表示不同端口.例如:`20-25,80,110`表示`20,21,22,23,24,25,80,100`

> 可以使用`-R`选项表示不匹配的目标,例如匹配`10.0.0.1`范为外的目标可以用`ettercat -R /10.0.0.1/`

> 目标也负责局域网的初始扫描,你可以用他们来限制尽在子网掩码主机的一个子集,连个目标之间合并的结果将会被扫描,记住如果没有指定目标一位置无目标,但是如果使用`//`表示子网内所有主机

## 权限

ettercap需要用root权限来打开link层sockets,初始化之后,root权限不在需要.所以ettercap讲降权为UID=65535(nobody).因为ettercap必须写日志文件,它必须在有权限的目录下被执行.例如:`/tmp/`.如果你想降权到其他UID,可以到处环境变量`EC_UID=uid`(EC\_UID=1000)或者在配置文件etter.conf文件中设置正确的参数.

## Ssl中间攻击

当启动ssl中间攻击时,ettercap替换掉真正的ssl证书.可以修改证书:

```
openssl genrsa -out etter.ssl.crt 1024
openssl req -new -key etter.ssl.crt -out tmp.csr
openssl x509 -req -days 1825 -in tmp.csr -signkey etter.ssl.crt -out tmp.new
cat tmp.new >> etter.ssl.crt
rm -f tmp.new tmp.csr
```

ssl中间现在还不能用在桥接模式

## 参数

一般参数都可以组合在一起使用,如果参数不支持组合使用ettercap会有提示警告.

## 嗅探和攻击选项

ettercap NG 有一些新的统一的嗅探方式.表示内核中的`ip_forwarding`总是被禁用的并且转发通过ettercap来实现.每一个目的mac地址等于主机mac地址并且目的ip地址和绑定的网口不同的数据包会被ettercap转发(Every packet with destination mac address equal to the host's mac address and destination ip address different for the one bound to the iface will be forwarded by ettercap).在转发之前,ettercap可以过滤,嗅探,log或者丢弃他们.这些数据包如何被劫持是无关紧要的,ettercap会去处理他们.你甚至可以使用外部软件来劫持数据包.

你可以完全控制ettercap应该接收什么.你可以使用内置的中间攻击模块,把网口设置为混杂模式,使用插件或者使用任意你想用的方式.

> 重要:如果是你在gateway上运行ettercap那么需要在ettercap进程结束后打开`ip_forwarding`,因为ettercap被降权了,所以没法自己打开`ip_forwarding`


### -M  --mitm <METHOD:ARGS>

激活中间人攻击,它完全独立于的嗅探.目的在于劫持数据包,并把数据包重定向到ettercap.必要时嗅探引擎会转发这些数据包.你可以选择你喜欢的mitm或者几个结合起来使用.如果mitm method需要参数的话,可以在`:`后面跟上.`(-M dhcp:ip_pool,netmask,etc)`

#### 攻击方式

#### arp ([remote]双向欺骗,[oneway]单项欺骗):

这个方式实施arp投毒,arp的 请求/响应 会发送给受害者来毒化他们的arp缓存.一旦受害者被毒化,那么受害者发送的数据包都会发送给攻击者.在静默模式下(-z选项)只有第一个目标被选中,如果你想在静默模式下毒化多个目标,那么使用`-j`选项来从文件中加载目标列表.

如果你不选择任何目标,那么将会被当做`ANY`:网络上的所有主机.目标列表和主机列表(通过arp scan创建)拼接在一起,他们的结果被用来确定被攻击的受害者.

remote是可选的参数,但是如果你想要嗅探远程ip毒化网关必须指定它.显然,如果你选择了一个受害者并且网关在目标列表中,ettercap将会只嗅探他们之间的链接,但是要想使得ettercap能够嗅探通过网关的链接,就必须使用这个参数(you have to specify it if you want to sniff remote ip address poisoning a gateway. Indeed if you specify a victim and the gw in the TARGETS, ettercap will sniff only connection between them, but to enable ettercap to sniff connections that pass thru the gw, you have to use this parameter.)

oneway参数使得ettercap只单向毒化(比如只毒化t1到t2),当你想要毒化客户端,而不破坏路由的时候,很有用.

例如:
```
目标列表
/10.0.0.1-5/ /10.0.0.15-20/
主机列表
10.0.0.1 10.0.0.3 10.0.0.16 10.0.0.18
受害者就是
1 and 16, 1 and 18, 3 and 16, 3 and 18
```

#### icmp (MAC/IP)

这种攻击实施 ICMP 重定向.通过在局域网中伪造一个ICMP重定向报文伪装成最近的一台路由主机,让所有连接到互联网的主机的数据包都发送给攻击者,再由攻击者转发给真正的网关.只有client被重定向,因为网关不会接受重定向消息.**需要保证过滤器不会修改payload的length**.你可以修改数据包,但是length不可改变,因为tcp序号不会同时更新.

你必须将真正的网关的mac和ip作为参数传进来:`-M icmp:00:11:22:33:44:55/10.0.0.1`


#### dhcp (ip_pool/netmask/dns)
实施DHCP伪装.给新接入主机分配动态IP地址.所以参数中必须给定IP地址池,子网掩码,DNS主机地址.

如果client发送了dhcp请求ettercap会确认请求,并且只修改gw的选项

警告：如果和真实的DHCP分配了重复的IP地址,将会在局域网中造成冲突,所以在一般情况下要谨慎使用这种攻击模式,他会把整个局域网弄得很糟糕.就算停止攻击,所有受害主机还会认为攻击者就是网关,直到租用时间期限到了为止.

例如:
```
-M dhcp:192.168.0.30,35,50-60/255.255.255.0/192.168.0.1
reply to DHCP offer and request.

-M dhcp:/255.255.255.0/192.168.0.1
reply only to DHCP request.
```

#### port ([remote],[tree])

实施端口窃取.但arp投毒不可用时,这个方法比较有效.他会使用arp数据包来进行泛红攻击.如果你不指定`tree`属性,被窃取的数据包的目标的MAC地址会和攻击的MAC地址一样(其他的 NICs 不会看到这些数据包),源MAC地址是主机列表中的一个.这种方式窃取主机列中受害者的主机的端口.使用low delays,被指定MAC的数据包会被攻击者获取到.

当攻击者获取到被盗取的数据包后,停止泛洪,并且执行arp请求来获取到数据包的真正的目的地.当收到arp响应是说明受害者可以接受数据包了.然后将数据包发送给受害者.再次启动泛洪


### -o, --only-mitm

这个选项禁用嗅探线程,并且只启动mitm.如果你想用ettercap来实施攻击,用其他嗅探工具嗅探,这个方式有效.**数据包不会ettercap转发出去,内核负责转发,需要打开ip_forwarding**

### -f, --pcapfilter <FILTER>
在pacp库中设置过滤器,格式和tcpdump一样.记住,这种过滤器不会嗅探wire外的数据包,所以如果你想使用mimt,,ettercap将不能够转发劫持到的数据包.这个功能可以减少ettercap的decoding模块的的网络负载.

### -B, --bridge <IFACE>

BRIDGED 模式 


## 离线嗅探

### -r, --read <FILE>

这个选项将数据包从已保存的pcap文件中嗅探,而不是在线嗅探.可以读取tcpdump或者wireshark等抓包软件保存下来的数据包,然后执行你想要的数据分析(例如用户名,密码).

显然从文件离线嗅探时不可以同时使用(arp或bridging,等)在线嗅探

### -w, --write <FILE>

当使用在线嗅探是,你想把数据包保存下来用其他分析工具去分析,这个参数可以把数据包写到文件中

建议:如果和`-r`一起使用,那么你可以在过滤已经dump的数据包或者破译wep wifi时把他们dump到另一个文件

## 用户界面

### -T, --text

文本界面,h帮助

### -q, --quiet

静默模式,它只与控制台界面结合使用,它不会打印输出数据,如果想要转储pcap文件是很有用的.例如:`ettercap -Tq -L dumpfile -r pcapfile`

### -s, --script <COMMANDS>

With this option you can feed ettercap with command as they were typed on the keyboard by the user. This way you can use ettercap within your favourite scripts. There is a special command you can issue thru this command: s(x). this command will sleep for x seconds.
example:

ettercap -T -s 'lq' will print the list of the hosts and exit
ettercap -T -s 's(300)olqq' will collect the infos for 5 minutes, print the

list of the local profiles and exit


### -C, --curses

基于Ncurses的GUI.(ettercap_curses(8))

### -G, --gtk

 GTK2GUI

### -D, –daemonize

此选项将ettercap从当前终端分离,创建一个守护进程在后台运行

## 一般选项

### -i, –iface < IFACE > 

手动选择网卡,这个选项需要 libnet >= 1.1.2

### -I, –iflist 

列出可用网卡列表

### -A, --address <ADDRESS>

使用<ADDRESS>来代替自动获取到的当前网卡的地址,当你的一个网卡有多个ip是有用

### -n, --netmask <NETMASK>

Use this <NETMASK> instead of the one associated with the current iface. This option is useful if you have the NIC with an associated netmask of class B and you want to scan (with the arp scan) only a class C.

### -R, --reversed

目标列表,除了给出的目标之外的所有其他主机

### -t, --proto <PROTO>

嗅探给定的协议,默认是(TCP+UDP). 协议可选"tcp", "udp" or "all"

### -z, --silent

这个选项不进行arp初始化扫描,

NOTE: you will not have the hosts list, so you can't use the multipoison feature. you can only select two hosts for an ARP poisoning attack, specifying them through the TARGETs

### -p, --nopromisc

ettercap默认开起网卡的混杂模式,来嗅探网络上的所有数据.

### -S, --nosslmitm

通常ettercap伪造ssl证书来嗅探https,这个选项禁用它

### -u, --unoffensive

ettercap启动时会禁用内核的转发,而使用自己的转发功能.这个选项禁用这个动作,把转发任务留给内核.如果你想运行多个ettecap实例的话这个选项很有用.其中一个ettercap负责转发,其他完成其他工作,而不需要负责转发数据包.否则他们会重复接受数据包.

他会基金用链接的session.它提高新能,但是就不能够实时修改数据包.

如果你想要使用mimt,必须启动独立的ettercap.

如果你使用的网卡没有ip的话那么必须使用这个参数

如果你在网关上使用ettercap,这个选项很有用,这样网关就不会回关闭转发功能,并且网关可以正确的路由数据包

### -j, --load-hosts <FILENAME>

他可以加载使用`-k`选项创建的主机列表文件(下面)

### -k, --save-hosts <FILENAME>

把主机列表保存到文件中.但有很多主机并且不想启动时开启arp风暴.使用这个参数吧主机列表保存下来,然后使用`-j`选项加载

### -P, --plugin <PLUGIN>

启动选择的插件,`ettercap_plugin(8)`

### -F, --filter <FILE>

从文件加载过滤器.

### -W, --wep-key <KEY>

可以加载wep密码进行WIFI密码破解,解码器只会传递解密成功的密码,其他的消息都会被跳过.

### -a, --config <CONFIG>

载入一个配置文件,不使用默认的/etc/etter.conf配置文件.如果经常在多种不同的环境下做渗透这个选项非常有用.


## 可视化选项

### -e, --regex <REGEX>

只处理匹配regex的数据包,结合`-L`很有用.它只记录匹配posix正则表达式的数据包.这个功能对可视化操作有一定影响,它只会显示匹配的正则表达式.

### -V, --visual <FORMAT>

数据包的显示格式

#### hex

以16进制打印数据包

例如:
```
HTTP/1.1 304 Not Modified
是
0000: 4854 5450 2f31 2e31 2033 3034 204e 6f74 HTTP/1.1 304 Not
0010: 204d 6f64 6966 6965 64 Modified
```
#### ascii

只打印可打印的字符,其他的表示为`.`

#### text

只打印可打印的字符,其他的忽略掉

#### ebcdic

把EBCDIC文本转为ASCII

#### html

在文本中删除所有html标签 
例: 
```
< title >This is the title< /title>, but the following < string > will not be displayed. 
显示结果为：
This is the title, but the following will not be displayed.
```

#### utf8

以utf-8格式显示.执行编码转换的声明在etter.conf文件中.

### -d, --dns

Resolve ip addresses into hostnames.
NOTE: this may seriously slow down ettercap while logging passive information. Every time a new host is found, a query to the dns is performed. Ettercap keeps a cache for already resolved host to increase the speed, but new hosts need a new query and the dns may take up to 2 or 3 seconds to respond for an unknown host.

HINT: ettercap collects the dns replies it sniffs in the resolution table, so even if you specify to not resolve the hostnames, some of them will be resolved because the reply was previously sniffed. think about it as a passive dns resolution for free... ;)

### -E, --ext-headers

打印输出数据包报头(例:mac addresses //MAC地址)

### -Q, --superquiet

超级安静模式,不会打印输出收集到的用户名和密码,只会保存成文件。使用插件时,会显示所有收集到的信息,使用这个选项就可以什么都不显示.
例:`ettercap -TzQP finger /192.168.0.1/22`

## 日志记录选项

### -L, --log <LOGFILE>

所有数据包保存到二进制文件中.可以使用` etterlog(8)`解析成可读的数据.所有被嗅探到的数据包都会保存,包括他们的被动信息(主机信息,用户密码).给定日志文件(LOGFILE)时,ettercap会创建LOGFILE.ecp(数据包)和LOGFILE.eci(信息)

注意:如果你使用了这个选项,那么不需要关心权限,因为他在开始时以最高权限打开的.但是如果你启动日志之前ettercap已经启动的话,那么你的目录需要是UID=65535或者uid=EC_UID,来保证可写.

log文件可以使用`-c`来压缩

### -l, --log-info <LOGFILE>

类似于`-L`但是只会记录每个主机的被动信息,用户,密码.这个文件被命名为LOGFILE.eci

### -m, --log-msg <LOGFILE>

把所有ettercap打印的用户消息保存在LOGFILE文件中.但使用demaon或者你想记录所有消息时比较有用

### -c, --compress

使用gzip算法压缩日志文件,ettercaplog处理日志的压缩和解压缩

### -o, --only-local

只存储本地局域网的信息

### -O, --only-remote

存储远程主机信息

## 标准选项

### -U, --update

更新ettercap,如果只想查看有什么更新,使用`-zU`

## 例子

### ettercap -Tp

在控制台模式下(-T)不使用混杂模式(-p),你只会看到自己的通信

### ettercap -Tzq

在控制台模式下(-T),不使用ARP初始化(-z),不显示数据包内容(-q安静模式),但是会显示用户名和密码和其他消息。

### ettercap -T -j /tmp/victims -M arp /10.0.0.1-7/ /10.0.0.10-20/

在控制台模式下(-T),加载主机列表(-j),对目标执行arp毒化中间人攻击(-M)arp

### ettercap -T -M arp // //

在控制台模式下(-T)，对整个局域网执行ARP毒化攻击(-M)arp

### ettercap -T -M arp:remote /192.168.1.1/ /192.168.1.2-10/

在控制台模式下(-T)，执行ARP双向欺骗(-M arp:remote)

### ettercap -Tzq //110

在控制台模式下(-T)，不使用ARP初始化(-z)，使用安静模式(-q)，监听所有主机110端口(pop3协议端口)

### ettercap -Tzq /10.0.0.1/21,22,23
在控制台模式下(-T)，不进行ARP初始化(-z)，使用安静模式(-q)，监听目标10.0.0.1的21，22，23端口(FTP、SSH、TELNET)

### ettercap -P list

打印输出可用插件列表。








# EttercapFilter

只支持if/else流程控制,有点类似C语言,但是后面必须跟着`{}`,即使只有一条语句,且 `if`和`(`之间要空格.`if () {}`

函数名和括号之间不加空格,`func(args...);`

`if`语句中的条件判断可以函数或者比较, 还可以使用`||`和`&&` 例如:`if (tcp.src == 21 && search(DATA.data, "ettercap")) {}`

比较运算符可以使用`==,>,<,>=,<=`,可以比较数字,字符串和IP地址,ip地址必须使用`''`,例如`'192.168.1.1'`,字符串使用`""`

赋值操作的右操作数可以是数字,字符串,和16进制`0x..` ,还支持`+=`,`-=`

## 函数

## 变量

DATA.data 数据包
ip.proto == TCP 类型,UDP/TCP
tcp.dst == 80 TCP端口
ip.src == '10.0.0.2' IP地址
ip.ttl < 20 路由中继

### search(where,what)

在`where`缓冲中搜索`what`,`where`可以使`DATA.data`或者`DECODED.data`.`DATA`是在链路上传输的有效载荷(TCP或者UDP),`DECODED`是解码器解码或编码后的有效载荷

所以如果你在ssl链接中search,那么最好使用`DECODED.data`,因为数据是被加密的.

`what`字符串可能是二进制,所以你需要转义它;`search(DATA.data, "\x41\x42\x43")`

### regex(where, regex)

与search类似,但是`regex`只能是string

### pcre\_regex(where, pcre\_regex ... )

这个函数会执行perl的模式匹配

### replace(what, with)

可以使用二进制,但是必须转义,只在`DATA.data`可以执行replace

### inject(what)

这个函数在数据包开始处理后,在数据包后面插入`what`制定的数据包,他只能在DATA.data之后插入,
可以使用这个方法来替换整个数据包,先drop(),然后插入,例如:`inject("./fake_packet")`

### log(what, where)

这个方法在where文件中保存what,例如:`log(DECODED.data, "/tmp/interesting.log")`

只有payload被dump,packet的任何信息都不会被保存.所以你可以在文件中看到数据流.如果需要保存packet,需要使用`-L`参数,并且使用`etterlog`来分析

`where`必须是个可写文件

### msg(message)

向用户消息窗口打印消息,例如终端

### drop()

将packet标记为`to be dropped`,这样packet就不会被发送给目标

### kill()

关闭链接,如果是TCP那么`RST`会发送给链接的两边(来源和目标).如果是UDP,那么`ICMP PORT UNREACHABLE`会发送给来源端

### exec(command)

执行shell命令.必须提供完整的路径名,因为这里没有上下文环境.没办法知道这个命令是否执行成功,而且他是一个异步子进程运行.

### exit()

让过滤引擎退出
