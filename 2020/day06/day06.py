import sys
import re

fname = '../input/day06/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()

pp1 = []
tmp1 = ""
pp2 = []
tmp2 = set()
pp2x = []

i = 0
for line in lines:
    line = line.strip()
    tmp1 = tmp1 + " " + line
    if len(line) > 0:
        for c in line:
            tmp2.add(c)
        pp2x.append(tmp2)
        tmp2 = set()
    if len(line) < 1 and i > 0:
        pp1.append(tmp1)
        tmp1 = ""
        pp2.append(pp2x)
        tmp2 = set()
        pp2x = []
        continue
    i = i + 1

pp1.append(tmp1)
pp2.append(pp2x)

def ppart1(pp):
    rv = 0
    for p in pp:
        tmpc = set()
        for c in p:
            if c != ' ':
                tmpc.add(c)
        rv = rv + len(tmpc)
    return rv

def ppart2(pp2):
    c2 = 0
    for p in pp2:
        if len(p) == 1:
            #print(" . ", len(p[0]), p[0])
            c2 = c2 + len(p[0])
        else:
            lst = p[0]
            for px in p[1:]:
                lst2 = lst.intersection(px)
                #print(".. ", len(lst2), lst, px, lst2)
                lst = lst2
            c2 = c2 + len(lst)
    return c2

if part1:
    print(ppart1(pp1))
else:
    print(ppart2(pp2))