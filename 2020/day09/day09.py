import sys
import re
import timeit

fname = '../input/day09/input.txt'
#fname = '../input/day09/test'
cut = 25
#cut = 5

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()

pre = []
main = []

def chk(num, pre):
    for p1 in pre:
        for p2 in pre:
            if p1 != p2 and p1 + p2 == num:
                return True
    return False

i = 0
target = 0
for line in lines:
    line = line.strip()
    cur = int(line)
    if len(pre) < cut:
        pre.append(cur)
    else:
        if not chk(cur, pre):
            target = cur
            print(cur)
        pre.pop(0)
        pre.append(cur)
    i += 1

print("###",len(pre),len(main))

if part1:
    print(target)
    sys.exit()

i = 0
cand = []
for line in lines:
    line = line.strip()
    cur = int(line)
    if sum(cand) == target:
        print("!",min(cand),max(cand),min(cand)+max(cand))
        sys.exit()
    while sum(cand) > target:
        cand.pop(0)
        if sum(cand) == target:
            print("!",min(cand),max(cand),min(cand)+max(cand))
            sys.exit()
    cand.append(cur)
    #print(cand, sum(cand))
    print(sum(cand))

