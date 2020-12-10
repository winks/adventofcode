import sys
import re
import timeit

fname = '../input/day10/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: int(s.strip()), lines))

def ppart1(lines):
    dev = 3
    lines = sorted(lines)
    mmax = lines[-1]
    start = 0
    rv = []
    r1 = 0
    r3 = 0
    for cur in lines:
        diff = cur - start
        if diff <= dev:
            rv.append((cur, diff))
            if diff == 1:
                r1 += 1
            if diff == 3:
                r3 += 1
        start += diff
    r3 += 1
    return r1 * r3

def ppart2():
    pass

start = timeit.default_timer()
if part1:
    num = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)

