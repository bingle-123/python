```sh
$ if [ $UID -ne 0 ];then
>echo "this is not root"
>else
>echo "this is root"
>fi
```
# 数学运算
```sh
$ a=4
$ b=5
$ let result=$a+$b
$ echo $result
```
```sh
$ result=$[ a + b + 1 ]
$ echo $result
```
```sh
$ result=$[ $a + 10 ]
$ echo $result
```
```sh
$ result=$(( a + 15 ))
$ echo $result
```
```sh
$ result=`expr 3 + 4`
$ echo $result
```
```sh
$ result=$(expr $a + 20 )
$ echo $result
```
# 标准输入输出以及标准错误
> 0标准输入 1标准输出 2标准错误

```sh
$ ls + 2> /tmp/error
$ ls + 2> /tmp/error 1> /tmp/stdout
$ #2>&1 将标准错误转为标准输出
$ #&>与上面一样
$ ls  2>&1  /tmp/stdout
$ ls  &> /tmp/stdout
```
> tee命令可以将stdout的一份副本保存到指定文件中，同时将另一份副本作为后续命令的stdin

```sh
$ cat fff* |tee /tmp/test |cat -n
$ cat ffff* 2> /tmp/out
$ cat -n /tmp/out
```
> \>与>>不同，默认情况下 >==1> >>==1>> 如果要最佳到文件中需要在>>前面加上1或2



# 从文件中读取数据
```sh
$ cat -n < sever.py
$ exec 可以创建文件描述符读取文件（读取模式）
$ echo 'hello test' > test.txt
$ exec 3<test.txt
$ cat <&3
```
> 再次读取文件描述符3时需要再次创建该描述符

exec也可以创建文件描述符用于写入(截断模式)
```sh
$ exec 4> output.txt
$ echo newline >&4
$ cat output.txt
```
exec还可以创建一个追加模式的文件描述符
```sh
$ exec 5>> input.txt
$ echo new line append >&5
$ cat input.txt
```
# 数组
## 定义数组
```sh
$ array_var=(1 2 3)
$ echo ${array_var[1]}
$ array_var[0]='test0'
$ array_var[1]='test1'
$ array_var[2]='test2'
$ array_var[3]='test3'
$ array_var[4]='test4'
$ array_var[5]='test5'
$ echo ${array_var[0]}
$ index=3
$ echo ${array_var[$index]}
$ echo ${array_var[*]}
$ echo ${array_var[@]}
```
## 关联数组
>关联数组中可以用任意的文本作为数组索引，首先需要使用声明语句将一个变量名声明为关联数组

```sh
$ declare -A ass_array
$ ass_array=([index]=11 [sec]=22)
$ echo ${ass_array[sec]}
$ echo ${ass_array[*]}
```
获取数组索引列表
```sh
$ echo ${!ass_array[*]}
```
临时定义命令别名，可以在.bashrc中定义
```sh
$ alias you='ls'
```
# 获取终端信息tput和stty两款终端处理工具
获取行数和列数
```sh
$ tput cols
$ tput lines
```
移动光标
```sh
$ tput cup 10 10
```
stty 输入密码不可见
```sh
$ echo -e "Enter password"
$ stty -echo
$ read password
$ stty echo
$ echo $password
$ echo Password read.
```
# 获取，设置日期和延时
日期格式化以+开头加上格式化参数
```sh
$ date +%s
$ date "+%s %B"
```
计算一组命令所花费的时间
```sh
$ start=`date +%s`
$ sleep 1
$ end=`date +%s`
$ use=$(( end - start ))
$ let use=$end-$start
$ echo “运行了$use秒”
```
测试
```sh
$ echo -n Count:
$ tput sc
$ count=0
$ while true;
$ do
$ if [ $count -lt 1 ];
$ then
$ let count++;
$ sleep 1;
```
tput rc 回复光标位置 tput ed 清楚光标位置到行尾之间的内容
```sh
tput rc;
tput ed;
echo -n $count;
else exit 0;
fi
done
```
>脚本调试bash -x script.gzip, deflate, lzma, sdchsh

# 函数和参数
## 定义
```sh
$ function fname()
$ {
$     echo '调用fname';
$ }
```
或者
```sh
$ fname()
$ {
$     echo '调用fname';
$ }
```
## 给函数传递参数 fname arg1 arg2;
```sh
$ fname()
$ {
$     echo $1,$2;#访问第一个和第二个参数
$     echo "$@";#以列表方式一次性打印所有参数，常用到这个方法获取参数
$     echo "$*";#类似于$@,但是参数被作为单个实体，很少用到
$     return 0;
$ }
```
>- $1第1个参数
>- $2第2个参数
>- $n第n个参数
>- "$@"被扩展成"$1" "$2" "$3" .....

```sh
$ fname
$ fname 'arg1' 'arg2'
```
## 递归调用
```sh
$ F()
$ {
$ echo $1;
$ F hello;
$ sleep 3;
$ }
```
## 获取函数或命令的返回值
```sh
$ echo $? #0表示成功，非0表示失败
```
## 检测上一个命令是否执行成功
```sh
$ if [ $? -eq 0 ];
$ then
$ echo "executed successfully"
$ else
$ echo "executed failed"
$ fi
```
## read命令不用按enter键
```sh
$ read -n 2 var #读取2个字符存入var中
$ echo $var
$ read -s var #无回显方式读取密码
$ read -p 'enter input:' var #显示提示信息
$ read -t 2 var #在固定时间内读取
```
## 比较与测试
```sh
$ if condition;
$ then
$ commands;
$ else if condition;
$ then
$ commands;
$ else
$ commands;
$ fi
```
## 算数比较
```sh
$ -eq -gt -lt -ge -le -ne
$ [ $var1 -eq 3 -a $var2 -eq 4] #-a表示逻辑与
$ [ $var1 -eq 3 -o $var2 -eq 4] #-o表示逻辑或
```
## 文件系统测试
- -f 如果给定的变量包含正常的文件路径和文件名，返回真
- -x 给定的变量是一个可执行文件
- -d 给定的变量是一个目录
- -e 给定的变量文件存在
- -c 给定的变量包含的是一个字符设备文件路径
- -b 给定的变量包含的是一个块设备文件的路径
- -w 给定的变脸包含的文件可写
- -r 给定的变量包含的文件可读
- -L 给定的变量包含的是一个符号链接

## 字符串比较
> 字符串比较时，最好用中括号，因为有时候单个括号会产生错误

- [[ $str1 = $str2 ]]或者[[ $str1 == $str2 ]]比较是否相等
- [[ $str1 > $str2 ]] str1字母序大于str2
- [[ -z $str1 ]] str1包含的是空字符串
- [[ -n $str1 ]] str1包含的是非空字符串

使用&& 和 ||可以链接多个条件
```sh
if [[ -n $str1 ]] && [[ -z $str2 ]];
$ then
$ commands;
$ fi
```
## test命令
test可以用来执行条件检测，他可以避免过多的使用括号
```sh
$ if test $var -eq 0;then echo "True";fi
```
# 命令
## cat
cat file1 file2 file3 将文件链接起来打印<br>
echo 'adsfad' |cat - test.txt 可以将标准输入和文件链接起来 - 被作为stdin文本的文件名<br>
cat -s test.txt 不打印连续空白的行<br>
cat -n test.txt 加上行号<br>
## script和scriptreplay
### 录制
script -t 2> time.log -a output.session开始录制<br>
time.log用于存储时序信息，描述一个命令在何时运行，output.session 用于存储命令输出<br>
-t选项用于将时序数据导入stderr 2> 将错误信息重定向到time.log<br>
CTRL+D 结束录制<br>
### 播放
scriptreplay time.log output.session<br>

## find
find base_path  列出当前目录及子目录下的所有文件和文件夹,他会从base_path位置开始向下查找<br>
find -name "*.sh" -print  指定查找的文件名 -iname忽略大小写<br>
find . \( -name "*.txt" -o -name "*.sh" \)  匹配多个条件<br>
find . -path "*/c/*" -print  -path匹配文件夹<br>
find . ! -name "*.sh"  匹配不是.sh 结尾的文件<br>
find . ! -name "*.sh" -maxdepth 1    -maxdepth -mindepth 限制搜索的深度<br>
-type根据文件类型搜索 f文件 l符号链接 d文件夹 c字符设备 b块设备 s套接字 pFIFO<br>
根据时间戳-atime最近访问时间，-mtime最后一次修改时间,-ctime权限所有权最后一次改变时间单位天<br>
-amin -mmin -cmin单位<br>
find . -type f -mtime -7 打印七天之内修改过的文件 +7超过七天 7正好7天<br>
-size基于大小 b块512字节 c字节 w字 k1024字节 M1024K字节 G1024M<br>
find . -size -1M小于1M<br>
-delete 删除匹配文件<br>
-perm基于权限<br>
find . -perm 744 -type f<br>
-user 基于用户<br>
find . -user merlin<br>
-exec 最强大的特性，他可以找到匹配的文件等，并执行以后的命令<br>
find . -type f -exec chmod 644 {} +  如果找到 f1 和f2 那么后面相当于 chmod 644 f1和chmod 644 f2<br>

## xargs
xargs 可以将标准输出转化为参数<br>
pgrep python |xargs<br>
pgrep python |xargs -n 2   制定每行最多参数个数<br>
用自己的定界符分割参数<br>
echo “splitXsplitXsplitXsplitXsplitXsplit” |xargs -d X  -d选项输入一个定界符<br>
find 命令可跟xargs用管道链接 非常好用 但是xargs有时会误用定界符，所以要使用null字符（'\0'）来作为定界符<br>
find . -name 'filename' | xargs -0 commands<br>

## tr
tr只能通过stdin，无法从命令行参数接受输入<br>
echo "HELLO WHO IS THIS" |tr 'A-Z' 'a-z'<br>
tr删除字符<br>
echo "HELLO WHO IS THIS" |tr -d 'A-M'<br>
删除不在集合内的字符<br>
echo hello 1 char 2 next 4 |tr -d -c '0-9 \n'<br>
将连续的重复字符压缩成一个字符<br>
echo 'Gnu is     not    unix '|tr -s " " #tr -s '\n'<br>

## md5
md5sum filename >md5.log<br>
md5sum -c md5.log<br>

## 加密工具与散列；crypt,gpg,base64,md5sum,sha1sum,openssl
### gpg用来加密文件
gpg -c filename#创建加密文件<br>
gpg filename#解密文件<br>

### base64
base64 filename > output.file<br>
base64 -d output.file > filename<br>
>sha1sum和msd5sum都可以用来验证文件未被改动过

## sort可以轻松的对文件内容进行排序
```sh
$ sort -n filename #按数字排序
$ sort -r filename #逆向排序
$ sort -M filename #按月份排序
$ sort -m filename1 filename2 #合并两个排序过的文件
$ sort -C filename #检查文件是否已经排序
```
## uniq消除重复行
```sh
$ uniq　-u filename　#只显示不重复的行
$ uniq　-c　filename #计算重复行数
```
## 临时文件名和随机数
```sh
$ mktmp ＃在/tmp/目录下创建临时文件
$ mktmp -d　＃在/tmp/下创建临时目录
$ mktmp -u #只生成临时文件或文件夹名而不会实际创建
```
## 分割文件
### split分割后的文件名都会有一个x作为前缀
```sh
$ split -b 10kb filename -d -a 4#-d分割后的文件以数字结尾，-a分割后的文件名后缀长度
$ split -b 10kb filename -d -a 4 slipt_file #分割的文件名以split_file为前缀
$ split -l 10 filename #每个文件10行来分割，而不是按数据块大小
```
> csplit 是split的扩展

## 字符串处理
- filename='sample.jpg'
- ${parameter%word} 最小限度从后面截取word
- ${parameter%%word} 最大限度从后面截取word
- ${parameter#word} 最小限度从前面截取word
- ${parameter##word} 最大限度从前面截取word
- ${#parameter}获得字符串的长度
- echo ${x/a/b} 只替换一个
- echo ${x//a/b} 替换所有
- name=${filename%.*}#获取文件名
- type=${filename#*.}#获取文件后缀名
- echo ${name:0-5}#重0-5个字符
- str="abcdef"
- expr substr "$str" 1 3 从第一个位置开始取3个字符， abc
- expr substr "$str" 2 5 从第二个位置开始取5个字符， bcdef
- expr substr "$str" 4 5 从第四个位置开始取5个字符， def
- echo ${str:2}           从第二个位置开始提取字符串， bcdef
- echo ${str:2:3}         从第二个位置开始提取3个字符, bcd
- echo ${str:(-6):5}        从倒数第二个位置向左提取字符串, abcde
- echo ${str:(-4):3}      从倒数第二个位置向左提取6个字符, cde

### 查找子串的位置
- str="abc"
- expr index $str "a"  #1
- expr index $str "b"  #2
- expr index $str "x"  #0
- expr index $str ""   #0

## 多进程
```sh
$ pidarray=()
$ for file in file1 file2;
$ do
$     md5sum $file &;
$     pidarray+=("$!")
$ done
$ wait ${pidarray[@]}
```
>$!获得进程pid，在bash中$!保存着最近一个后台进程的pid，将pid放入数组中，wait命令等待这些进程结束

# 以文件之名
## 生成任意大小的文件
dd if=/dev/zero of=junk.data bs=1M count=1#创建一个junk.data的文件大小1M if代表输入文件，of代表输出文件<br>
bs 代表大小 count代表需要被复制的块数<br>
如果bs为2M count为2则得到4M的文件<br>

## 文本文件比较
comm file1 file2<br>
-1删除只在file1出现的行 -2 删除只在file2 出现的行 -3 删除俩个文件相同的行<br>

## 创建不可修改的文件
sudo chattr +i filename#设置<br>
sudo chattr -i filename#取消<br>

## diff
diff -u newfile oldfile<br>
diff -u version1.txt version2.txt version.patch<br>
patch 修补文件<br>
patch -p1 version1.txt < version.patch<br>
重复上面的命令可以册小修补<br>

# 让文本飞
## 正则表达式
- ^行标记开始 ^tux匹配tux开头的行
- $行尾标记 tux$匹配以tux结尾的行
- .匹配任意一个字符 tux.匹配tuxI和tuxa等zhuanyi
- []匹配包含在[字符]之中的任意一个字符 coo[kl]匹配cool和cook
- [^]匹配除了[字符]之外的任意一个字符 90[^01]不是90和91的都能匹配
- [-]匹配[]中指定范围内的任意一个字符 [1-4][a-r]
- ?匹配之前的项0或1次
- +匹配之前的项1次或多次
- *匹配之前的项0或多次
- ()创建用于匹配的字串 ma(tri)?x匹配max或matrix
- {n}匹配之前项n次
- {n,}之前项至少出现的次数
- {n,m}之前项出现n到m次
- | 交替--匹配|两边的任意一项Oct(1st|2nd) 匹配Oct 1st或者 Oct 2nd
- \\转义 \\.  \\*  \\{  \\[  \\+  \\?  \\^  \\$

## grep
- grep -E "regex" file 来使用正则表达式匹配
- grep -E -b -o可以打印匹配的位置
- grep -l 搜索多个文件时，打印匹配的文件名
- grep 'match' dirname -R或者-r -n 递归搜索目录下的文件
- grep 'match' dirname -r --include *.{c,cpp}递归中只搜索.c和.cpp 的文件
- grep 'match' dirname -r --exclude *.{c,cpp}递归中不搜索.c和.cpp 的文件
- grep 'match' filename -A 3 打印匹配行之后的3行
- grep 'match' filename -B 3 打印匹配结果之前的5行

## cut
cut -f 2,3,5 filename 显示 2，3，5列<br>
echo 'asdf asdfafeasd asdfas wewr '|cut -d' ' -f2,4   -d自定义分隔符<br>
cut -c1-5#显示从第1到5个字符<br>
cut -c1-5,6-10 --output-delimiter ","显示1-5 6-10两个字符串用","链接<br>

## sed尽心文本替换
sed 's/pattern/replace_string/' file或者cat file|sed 's/pattern/replace_string/'<br>
sed 's/pattern/replace_string/g' 全局替换<br>
sed 's/pattern//g' 可以删除匹配的行<br>
sed 's/pattern/replace_string/2g' 从第2个开始替换<br>
sed '/^$/d' file 移除空白行<br>
sed 's/pattern/replace_string/' -i 可以直接修改源文件<br>

## 按列合并多个文件
paste file1 file2 file3<br>
paste file1 file2 file3 -d "," 用,分割<br>

# 网络请求
## wget
wget url1 url2 ...<br>
wget url -O filename -o log    -O指定保存的文件名,-o指定记录日志到文件中<br>
wget -t 5 url     -t 网络不稳定时,指定尝试次数 -t 0 表示不停的尝试<br>
wget -c url 可以断点续传<br>
wget --mirror --convert-links www.example.com 可以下载整个网站<br>
wget -r -N -l -k depth url,跟上面功能一样<br>

## 以纯文本形式下载网页lynx
lynx url -dump > response.txt #-dump 将网页以ascii编码形式保存到本地

## cURL支持http https ftp post cookie 认证 用户代理字符串 扩展头部 限速 文件大小限制等等
curl URL/file -c offset 从文件制定的偏移量开始下载<br>
curl -c - URL 字段判断断点续传位置<br>
curl http://example.com --cookie  'user=slyux,pass=back' 设置cookie<br>
curl URL --user-agent "Mozilla/5.0" 设置用户代理<br>
curl -H "HOST: www.slynux.com" -H "Accept-language: en" URL 设置http头<br>
curl -I URL 只打印http头信息<br>
### 以post方式获取网页数据
curl URL -d "username=test&pwd=pwd" 表示以post方式发送数据

# 网络设置
## ifconfig
ifconfig wlan0 192.168.1.1 设置wlan0的ip<br>
ifconfig wlan0 192.168.1.100 netmask 255.255.255.0<br>
dhclient eth0 如果链接到的是自动分配ip的网络,这样可以快速配置<br>
ifconfig eth0 hw ether 00:1c:bf:87:35进行mac地址欺骗<br>
## fping查询网络内存活的主机
fping -a 192.168.1.1/24 -g 2> /dev/null
## ssh链接远程主机并运行命令
ssh user@host 'command1;command2;command3'<br>
ssh无密码登陆<br>
ssh-keygen -t rsa<br>

# 收集进程信息
## ps是收集进程信息最重要的工具
- ps -f显示多列信息
- ps -e 获取系统每个进程信息或者使用ps -ax
- ps -ef或者ps -axf
- ps -o field1.filed2 可以定义显示哪些列信息
- ps -eo pcpu,comm
- -o 参数 pcpu cpu占用率,pid进程id,ppid父进程id,pmem内存使用率,comm可执行文件名
- cmd简单命令,user启动进程的用户,nice优先级,time累计cpu时间,etime进程启动后流失的时间,
- tty所关联的tty设备,euid有效的用户ID,stat进程状态
- ps --sort -field1,+filed2,field3...按列排序

