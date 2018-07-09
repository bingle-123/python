#  gray

requires
```bash
pip install pyPdf python-nmap pygeoip mechanize BeautifulSoup4 nmap

sudo apt-get install python-bluez bluetooth python-obexftp 
```

```python
import socket
def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket() s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return
def main():
    ip1 = '192.168.95.148'
    ip2 = '192.168.95.149'
    port = 21
    banner1 = retBanner(ip1, port)
    if banner1:
        print '[+] ' + ip1 + ': ' + banner1 banner2 = retBanner(ip2, port)
    if banner2:
        print '[+] ' + ip2 + ': ' + banner2 
if __name__ == '__main__': 
    main()
```

## SSH

`pip install pxssh`

```python
import pxssh
def send_command(s, cmd):
    s.sendline(cmd) 
    s.prompt() 
    print(s.before)
def connect(host, user, password): 
    try:
        s = pxssh.pxssh()
        s.login(host, user, password) 
        return s
    except:
        print '[-] Error Connecting' exit(0)
s = connect('127.0.0.1', 'root', 'toor') 
send_command(s, 'ls ~')
```