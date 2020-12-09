import sys
import timeit

fname = '../input/day01/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname, "r") as fh:
    lines = fh.readlines()

def ppart1(limit, line):
    m = {}
    for line in lines:
        line = int(line.strip())
        other = (limit - line)
        if other in m:
            return (line * other)
        m[line] = True
    return 0

def ppart2(limit, lines):
    m = {}
    n = {}
    for line in lines:
        line = int(line.strip())
        if len(m) < 2:
            m[line] = line
            continue
        for mm in m.keys():
            if line + mm >= limit:
                continue
            if line in n.keys():
                return line * n[line][0] * n[line][1]
            other = (limit - mm - line)
            n[other] = (line, mm)
        m[line] = line
    return 0

if part1:
    start = timeit.default_timer()
    num = ppart1(2020, lines)
    end = timeit.default_timer()
    print("#", (end-start) * 1000)
    print(num)

else:
    start = timeit.default_timer()
    num = ppart2(2020, lines)
    end = timeit.default_timer()
    print("#", (end-start) * 1000)
    print(num)
