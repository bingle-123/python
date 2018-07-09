import signal, os, time


def receivesignal(signum, stack):
    print('recevied ', signum)

signal.signal(signal.SIGUSR1,receivesignal)
signal.signal(signal.SIGUSR2,receivesignal)
# signal.alarm(1)
print('my pid is :',os.getpid())

while True:
    print('waiting ......')
    time.sleep(5)