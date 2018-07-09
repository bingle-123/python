from wsgiref.simple_server import make_server

def application(environ,start_reponse):
    # for key,value in environ.items():
    #     print(key,value)
    start_reponse('200 OK',[('Content-Type','text/html')])
    return 'hello '.encode()

httpd = make_server('', 8000, application)
httpd.serve_forever()
