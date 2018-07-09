# import socket
# import optparse

# def retBanner(ip, port):
#     try:
#         socket.setdefaulttimeout(2)
#         s = socket.socket()
#         s.connect((ip, port))
#         banner = s.recv(1024)
#         return banner
#     except:
#         return


# def main():
#     ip1 = '192.168.1.106'
#     ip2 = '192.168.1.106'
#     port = 21
#     banner1 = retBanner(ip1, port)
#     if banner1:
#         print('[+] ' + ip1 + ': ' + str(banner1))
#     banner2 = retBanner(ip2, port)
#     if banner2:
#         print('[+] ' + ip2 + ': ' + str(banner2))


# if __name__ == '__main__':
#     main()

# coding=UTF-8
import pexpect
PROMPT = ['# ', '>>> ', '> ', '\$ ']


def send_command(child, cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)


def connect(user, host, password):
    ssh_newkey = 'Are you sure you want to continue connecting'
    connStr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connStr)
    ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if ret == 0:
        print('[-] Error Connecting') 
        return
    if ret == 1:
        child.sendline('yes')
        ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    if ret == 0:
        print('[-] Error Connecting') 
        return
    child.sendline(password) 
    child.expect(PROMPT) 
    return child
def main():
    host = '192.168.1.106'
    user = 'u'
    password = 'a'
    child = connect(user, host, password) 
    send_command(child, 'cat /etc/shadow | grep root')
if __name__ == '__main__': 
    main()
