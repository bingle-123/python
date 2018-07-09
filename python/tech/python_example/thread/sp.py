import subprocess
import sys
print('One line at a time')
proc = subprocess.Popen('python repeater.py', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

for i in range(5):
    proc.stdin.write(('%d\n' % i).encode())
output = proc.stdout.readline()
print(output)
remainder = proc.communicate()[0]
print(remainder.decode())

print('All line at a time')
proc = subprocess.Popen('python repeater.py', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

for i in range(5):
    proc.stdin.write(('%d\n' % i).encode())
remainder = proc.communicate()[0]
print(remainder)

