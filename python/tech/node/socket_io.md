# socket.io

## 安装

npm install socket.io

## 示例

```javascript
var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res) {
    res.sendfile('index.html');
});

io.on('connection', function(socket) {
    io.emit('this',"be received by everyone")//这条消息会全局发送
    console.log('a user connected');
    socket.on('disconnect', function() {
        console.log('user disconnected');
    });
    socket.on('chat message', function(msg) {
        console.log('message: ' + msg);
        io.emit('chat message',{'msg':`hi ${msg}`})
    });
});

http.listen(3000, function() {
    console.log('listening on *:3000');
});
```

index.html

```html
<!doctype html>
<html>
<head>
    <title>Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font: 13px Helvetica, Arial;
        }

        form {
            background: #000;
            padding: 3px;
            position: fixed;
            bottom: 0;
            width: 100%;
        }

        form input {
            border: 0;
            padding: 10px;
            width: 90%;
            margin-right: .5%;
        }

        form button {
            width: 9%;
            background: rgb(130, 224, 255);
            border: none;
            padding: 10px;
        }

        #messages {
            list-style-type: none;
            margin: 0;
            padding: 0;
        }

        #messages li {
            padding: 5px 10px;
        }

        #messages li:nth-child(odd) {
            background: #eee;
        }
    </style>
</head>
<body>
    <ul id="messages"></ul>
    <form action="" id="form">
        <input id="input" autocomplete="off" /><button>Send</button>
    </form>
</body>
<script src="/socket.io/socket.io.js"></script>
<script>
    var socket = io();
    var form = document.getElementById('form');
    var input = document.getElementById('input');
    var messags = document.getElementById('messages');
    form.onsubmit = function() {
        socket.emit('chat message', input.value);
        input.value = "";
        return false;
    }
    socket.on('chat message', function(msg) {
        var li = document.createElement('li');
        li.innerHTML = msg.msg;
        messags.appendChild(li);
    })
</script>
</html>
```
## 命名空间
```javascript
var io = require('socket.io')(80);
var chat = io
    .of('/chat')
    .on('connection', function (socket) {
      socket.emit('a message', {
          that: 'only'
        , '/chat': 'will get'
      });
      chat.emit('a message', {
          everyone: 'in'
        , '/chat': 'will get'
      });
    });

var news = io
    .of('/news')
    .on('connection', function (socket) {
      socket.emit('item', { news: 'item' });
    });
```
```html
<script>
    var chat = io.connect('http://localhost/chat')
      , news = io.connect('http://localhost/news');

    chat.on('connect', function () {
      chat.emit('hi!');
    });

    news.on('news', function () {
      news.emit('woot');
    });
</script>
```

## Server Api
### 创建Server
```javascript
var io = require('socket.io')();
// or
var Server = require('socket.io');
var io = new Server();
```
Server接受可以可选参数：

## Client Api

socketio默认有namespace->room->channel
