# -*- coding:utf-8 -*-
__author__ = 'mering Gao'
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s (%(threadName)-10s) %(message)s', )


# basehttpserver使用socketserver的类创建基类,用来建立http服务器,httpserver可以
# 直接使用,不过basehttprequesthandler需要扩展来处理各个协议方法(get,post等等)
import http.server
import urllib.parse

class gethandelr(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path=urllib.parse.urlparse(self.path)
        message_parts=['CLIENT VALUES:',
                       'client_address=%s (%s)'%(self.client_address,self.address_string()),
                       'command=%s'%self.command,
                       'path=%s'%self.path,
                       'real path=%s'%parsed_path.path,
                       'query=%s'%parsed_path.query,
                       'request_version=%s'%self.request_version,
                       '',
                       'SERVER VALUES:',
                       'server_version=%s'%self.server_version,
                       'sys_version=%s'%self.sys_version,
                       'protocol_version=%s'%self.protocol_version,
                       '',
                       'HEADERS RECEIVED',]
        for name,value in sorted(self.headers.items()):
            message_parts.append('%s=%s'%(name,value.rstrip()))
        message_parts.append('')
        message='\r\n'.join(message_parts).encode(k)
        self.send_response(200)

        self.wfile.write(message)
        return

from http.server import HTTPServer
server=HTTPServer(('localhost',8080),gethandelr)
print('starting server user ctrl-c to stop')
server.serve_forever()