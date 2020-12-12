import sys
import timeit

fname = '../input/day12/input.txt'
fname = '../input/day12/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: (s.strip()[0], int(s.strip()[1:])), lines))

def dist(a, b):
    return abs(a) + abs(b)

def pp(x):
    (a, b) = x
    if a == 0:
        if b == 1:
            return 'N'
        elif b == -1:
            return 'S'
        else: 
            return 'x'
    elif a == 1:
        if b == 0:
            return 'E'
        else:
            return 'y'
    elif a == -1:
        if b == 0:
            return 'W'
        else:
            return 'z'

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
    mod = int(line[1] / 90)
    if line[0] == 'L':
        for x in range(0, mod):
            if fac == (0, 1):
                fac = (-1, 0)
            elif fac == (-1, 0):
                fac = (0, -1)
            elif fac == (0, -1):
                fac = (1, 0)
            else:
                fac = (0, 1)
    elif line[0] == 'R':
        for x in range(0, mod):
            if fac == (0, 1):
                fac = (1, 0)
            elif fac == (1, 0):
                fac = (0, -1)
            elif fac == (0, -1):
                fac = (-1, 0)
            else:
                fac = (0, 1)
    return fac

def turn2(line, fac):
    mod = int((line[1] % 360) / 90)
    #bl = [(0, 1), (-1, 0), (0, -1), (1, 0)]
    if mod == 2:
        return (-1 * fac[0], -1 * fac[1])
    elif (line[0] == 'L' and mod == 1) or (line[0] == 'R' and mod == 3):
        return (-1 * fac[1], fac[0])
    elif (line[0] == 'L' and mod == 3) or (line[0] == 'R' and mod == 1):
        return (fac[1], -1 * fac[0])
    return fac

def ori(cur, wpx):
    pass

def ppart1(lines):
    fac = (1, 0)
    cur = (0, 0)
    #print(lines)
    for line in lines:
        (c, f) = move(line, cur, fac)
        fac = turn2(line, fac)
        print(line, cur, fac, pp(fac))
    return dist(cur[0], cur[1])

def ppart2(lines):
    cur = (0, 0)
    wpx = (10, 1)
    for line in lines:
        (c2, wpx) = move(line, cur, wpx)
        if line[0] == 'F':
            cur = c2
        wpx = turn2(line, wpx)
        print(line, cur, wpx)
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
