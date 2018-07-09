import signal


def alarm(n, stack):
    return


signal.signal(signal.SIGALRM, alarm)
signalname = dict((getattr(signal, n), n) for n in dir(signal) if n.startswith('SIG') and '_' not in n)



for s, name in sorted(signalname.items()):
    handler = signal.getsignal(s)
    if handler is signal.SIG_DFL:
        handler = 'SIG_DFL'
    elif handler is signal.SIG_IGN:
        handler = 'SIG_IGN'
    print('%-10s (%2d):' % (name, s), handler)

print(dir(signal))