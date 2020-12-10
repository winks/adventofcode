import sys
import timeit

fname = '../input/day10/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: int(s.strip()), lines))

lines = sorted(lines)
lines.insert(0, 0)
lines.append(lines[-1]+3)

def ppart1(lines):
    start = 0
    r1 = 0
    r3 = 0
    for cur in lines:
        diff = cur - start
        if diff == 1:
            r1 += 1
        elif diff == 3:
            r3 += 1
        start += diff
    return r1 * r3

def ppart2(lines):
    opts = []
    tmpo = []
    for i in range(1, len(lines)-1):
        cur = lines[i]
        ne = lines[i+1]
        la = lines[i-1]
        if ne - la < 3:
            tmpo.append(cur)
            if ne - cur == 2:
                opts.append(tmpo)
                tmpo = []
            else:
                pass
        else:
            if len(tmpo) > 0:
                opts.append(tmpo)
                tmpo = []
    x = 1
    for opts2 in opts:
        if len(opts2) == 3:
            x *= 7
        elif len(opts2) == 2:
            x *= 4
        elif len(opts2) == 1:
            x *= 2
    return x

start = timeit.default_timer()
if part1:
    num = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    num = ppart2(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
