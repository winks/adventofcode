import sys

fname = '../input/day02/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

valid = 0

with open(fname) as fh:
    for line in fh.readlines():
        parts = line.split(':')
        passw = parts[1].strip()
        parts = parts[0].split(' ')
        match = parts[1]
        parts = parts[0].split('-')
        n1 = int(parts[0])
        n2 = int(parts[1])
        if part1:
            vc = 0
            for i in range(0, len(passw)):
                if passw[i] == match:
                    vc = vc + 1
            if vc >= n1 and vc <= n2:
                valid = valid + 1
        else:
            if (passw[n1-1] == match and not passw[n2-1] == match) or \
                    (not passw[n1-1] == match and passw[n2-1] == match):
                valid = valid + 1
    print(valid)

