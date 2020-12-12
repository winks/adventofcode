import sys
import timeit

fname = '../input/day12/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: (s.strip()[0], int(s.strip()[1:])), lines))

def dist(a, b):
    return abs(a) + abs(b)

def move(line, cur, fac):
    if line[0] == 'F':
        cur = (cur[0] + line[1] * fac[0], cur[1] + line[1] * fac[1])
    elif line[0] == 'N':
        cur = (cur[0], cur[1] + line[1])
        fac = (fac[0], fac[1] + line[1])
    elif line[0] == 'S':
        cur = (cur[0], cur[1] - line[1])
        fac = (fac[0], fac[1] - line[1])
    elif line[0] == 'E':
        cur = (cur[0] + line[1], cur[1])
        fac = (fac[0] + line[1], fac[1])
    elif line[0] == 'W':
        cur = (cur[0] - line[1], cur[1])
        fac = (fac[0] - line[1], fac[1])
    return (cur, fac)

def turn(line, fac):
    mod = int((line[1] % 360) / 90)
    if mod == 2:
        return (-1 * fac[0], -1 * fac[1])
    elif (line[0] == 'L' and mod == 1) or (line[0] == 'R' and mod == 3):
        return (-1 * fac[1], fac[0])
    elif (line[0] == 'L' and mod == 3) or (line[0] == 'R' and mod == 1):
        return (fac[1], -1 * fac[0])
    return fac

def ppart1(lines):
    fac = (1, 0)
    cur = (0, 0)
    for line in lines:
        (cur, _) = move(line, cur, fac)
        fac = turn(line, fac)
        #print(line, cur, fac)
    return dist(cur[0], cur[1])

def ppart2(lines):
    cur = (0, 0)
    wpx = (10, 1)
    for line in lines:
        (c2, wpx) = move(line, cur, wpx)
        if line[0] == 'F':
            cur = c2
        wpx = turn(line, wpx)
        #print(line, cur, wpx)
    return dist(cur[0], cur[1])

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
