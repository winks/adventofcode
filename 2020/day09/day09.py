import sys
import re
import timeit

fname = '../input/day09/input.txt'
cut = 25

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()

def chk(num, pre):
    for p1 in pre:
        for p2 in pre:
            if p1 != p2 and p1 + p2 == num:
                return True
    return False

def ppart1(lines):
    pre = []
    for line in lines:
        line = line.strip()
        cur = int(line)
        if len(pre) < cut:
            pre.append(cur)
        else:
            if not chk(cur, pre):
                return cur
            pre.pop(0)
            pre.append(cur)
    return None

def ppart2(target, lines):
    cand = []
    for line in lines:
        line = line.strip()
        cur = int(line)
        if sum(cand) == target:
            return min(cand) + max(cand)
        while sum(cand) > target:
            cand.pop(0)
            if sum(cand) == target:
                return min(cand) + max(cand)
        cand.append(cur)

start = timeit.default_timer()
target = ppart1(lines)

if part1:
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(ppart1(lines))
else:
    p2 = ppart2(target, lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(p2)

