import sys
import timeit

fname = '../input/day12/input.txt'
#fname = '../input/day12/test'

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
            return 'E'
        elif b == -1:
            return 'W'
        else: 
            return 'x'
    elif a == 1:
        if b == 0:
            return 'S'
        else:
            return 'y'
    elif a == -1:
        if b == 0:
            return 'N'
        else:
            return 'z'


def ppart1(lines):
    fac = (0, 1)
    cur = (0, 0)
    print(lines)
    print((0, 0))
    for line in lines:
        if line[0] == 'F':
            cur = (cur[0] + line[1] * fac[0], cur[1] + line[1] * fac[1])
        elif line[0] == 'N':
            cur = (cur[0] - line[1], cur[1])
        elif line[0] == 'S':
            cur = (cur[0] + line[1], cur[1])
        elif line[0] == 'E':
            cur = (cur[0], cur[1] + line[1])
        elif line[0] == 'W':
            cur = (cur[0], cur[1] - line[1])
        elif line[0] == 'L':
            mod = int(line[1] / 90)
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
            mod = int(line[1] / 90)
            for x in range(0, mod):
                if fac == (0, 1):
                    fac = (1, 0)
                elif fac == (1, 0):
                    fac = (0, -1)
                elif fac == (0, -1):
                    fac = (-1, 0)
                else:
                    fac = (0, 1)
            
        print(line, cur, pp(fac))
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
