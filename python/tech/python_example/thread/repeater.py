import sys

sys.stdout.write('repeater.py: staring\n')
# sys.stdout.flush()

while True:
    nextline = sys.stdin.readline()
    if not nextline:
        break
    sys.stdout.write(nextline)
    sys.stdout.flush()
sys.stdout.write('repeater.py: exting\n')
# sys.stdout.flush()