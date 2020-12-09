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

#g1 = 0
#g2 = 0

def chk(limit, lines):
    #global g1
    #global g2
    m = {}
    for line in lines:
        other = (limit - line)
        #g1 += 1
        #g2 += 1
        if other in m:
            return True
        m[line] = True
    return False

def ppart1(lines):
    #global g1
    pre = []
    for line in lines:
        line = line.strip()
        cur = int(line)
        if len(pre) < cut:
            pre.append(cur)
            #g1 += 1
        else:
            if not chk(cur, pre):
                return cur
            pre.pop(0)
            pre.append(cur)
    return None

def ppart2(target, lines):
    #global g2
    cand = []
    for line in lines:
        line = line.strip()
        cur = int(line)
        #g2 += 1
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

#print(g1)
#print(g2)
