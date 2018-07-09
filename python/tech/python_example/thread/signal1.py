import os,signal,time,sys

pid=os.getpid()
received=False
def signal_user1(signum,frame):
    global received
    received=True
    print('CHILD %6s: Received USR1'%pid)
    sys.stdout.flush()

print('CHILD %6s: setting up signal handler'%pid)
sys.stdout.flush()

signal.signal(signal.SIGUSR1,signal_user1)
print('CHILD %6s: Pausing to wait for signal'%pid)
sys.stdout.flush()
time.sleep(3)
if not received:
    print('CHILD %6s:Never recevied signal'%pid)
    sys.stdout.flush()