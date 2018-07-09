import os, signal, subprocess, time, sys

proc = subprocess.Popen(['python3', 'signal1.py'])
print('PARENT :Pausing before sending signal...')
sys.stdout.flush()
time.sleep(1)
print('PARENT : signal child')
sys.stdout.flush()
# print(proc.communicate()[0])
os.kill(proc.pid, signal.SIGUSR1)