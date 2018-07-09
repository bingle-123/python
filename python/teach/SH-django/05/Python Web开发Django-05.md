# Python Web开发Django-05

## 课程内容

### cookie,session

### 文件上传

## cookie和session

Http是短连接,数据发送完成之后,就断开了了连接。下次需要发起请求时，需要再次建立连接。

### cookie特性

客户端使⽤用cookie来保存相关信息，例例如保存⽤用户信息，那么客户端再次发起http请求的时候，服务器器可以根据cookie找到对应的⽤用户

特性：
1. 默认情况系，浏览器器关闭后，cookie⾃自动被删除
2. cookie有⽣生命周期
    1. max-age=0 关闭,就清除掉cookie
    2. max-age=None 永久有效
    3. max-age=整数标识多少秒之后过期
    4. expires datetime对象,标识到具体的时间过期


### session特性

服务端技术,⽤用于保存会话信息django把会话信息,保存在数据库中。并且使⽤了base64编码来做简单的加密。

## 文件上传




