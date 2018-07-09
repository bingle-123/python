# Ajax

本身不是一种新技术，而是一个在 2005年被Jesse James Garrett提出的新术语。（异步JavaScript和XML）Asynchronous JavaScript + XML,当使用结合了这些技术的AJAX模型以后， 网页程序能够快速地将渐步更新呈现在用户界面上，不需要重载（刷新）整个页面。这使得程序能够更快地回应用户的操作。

尽管X在Ajax中代表XML, 但由于JSON的许多优势，比如更加轻量以及作为Javascript的一部分，目前JSON的使用比XML更加普遍。JSON和XML都被用于在Ajax模型中打包信息。

# XMLHttpRequest

XMLHttpRequest 是一个 API，它为客户端提供了在客户端和服务器之间传输数据的功能。它提供了一个通过 URL 来获取数据的简单方式，并且不会使整个页面刷新。这使得网页只更新一部分页面而不会打扰到用户。XMLHttpRequest 在 AJAX 中被大量使用

XMLHttpRequest 最初由微软设计，随后被 Mozilla、Apple 和 Google采纳。如今，该对象已经被 W3C组织标准化。 通过它，你可以很容易的取回一个 URL 上的资源数据。尽管名字里有 XML，但 XMLHttpRequest 可以取回所有类型的数据资源，并不局限于 XML。而且除了 HTTP ，它还支持 file 和 ftp 协议


## readyState
返回xhr当前所处的状态

### UNSENT 0
XMLHttpRequest xhr已被创建， 但尚未调用 open() 方法。

### OPENED 1
open() 方法已经被触发。在这个状态中，可以通过  setRequestHeader() 方法来设置请求的头部， 可以调用 send() 方法来发起请求。

### HEADERS_RECEIVED 2
send() 方法已经被调用，响应头也已经被接收。

### LOADING 3
响应体部分正在被接收。如果 responseType 属性是“text”或空字符串， responseText 将会在载入的过程中拥有部分响应数据。

### DONE 4
请求操作已经完成。这意味着数据传输已经彻底完成或失败。

## response 
属性返回响应的正文

## responseText
类似于response

## responseType
响应主体的数据类型

## status
返回了响应中的状态码 100~199;200~299;300~399;400~499;500~599

## statusText
返回响应的状态码说明

## timeout
设置响应的超时时间,秒单位;如果超时了,会触发超时时间,通过绑定的ontimeout函数来处理

## abort() 方法

取消请求,通常和超时一起使用

## getAllResponseHeaders() 方法
返回所有的响应头

## setRequestHeader(key,value) 方法
设置请求头

## onreadystatechange 绑定回调函数
只要 readyState 属性发生变化，就会调用相应的处理函数

## ontimeout 绑定回调函数
当超时事件触发

## upload.onprogress 绑定回调函数

在请求过程中不断触发,请求的进度事件,常用于向服务器发送大量数据时,检测已经发送的数据量;例如跟踪文件上传进度条。

该回调函数的event,包含的属性:
- loaded:已经发送的数据
- total:要发送的数据总数


```javascript
var xhr=new XMLHttpRequest()
xhr.timeout = 2000; // 超时时间，单位是毫秒

 xhr.onreadystatechange=function(e){ 
     return 
     var readystate=xhr.readyState
     switch(readystate){
         case 0:{
             console.log('xhr已被创建');
             break;
         };
         case 1:{
             console.log('open() 方法已经被触发')
              break;
         };
         case 2:{
             console.log('send() 方法已经被调用，响应头也已经被接收。')
              break;
         };
         case 3:{
             console.log('响应体部分正在被接收')
             console.log(xhr.response)
              break;
         };
         case 4:{
             console.log('请求操作已经完成')
             console.log('response:',xhr.response)
             console.log('responseText:',xhr.responseText)
             console.log('responseType:',xhr.responseType)
             console.log('status:',xhr.status)
             console.log('statusText:',xhr.statusText)
             console.log('getAllResponseHeaders',xhr.getAllResponseHeaders())
              break;
         }
     }
 }
xhr.open('get','/tajax',true)
xhr.ontimeout = function (e) {
  console.log('超时了')
  xhr.abort()
};
xhr.upload.onprogress=function(event){
    console.log(event.loaded)
    console.log(event.loaded)
}
xhr.onabort=function(e){
    console.log('被取消了')
}
xhr.send()
```



