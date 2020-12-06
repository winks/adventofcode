import sys
import re

fname = '../input/day06/input.txt'
#fname = '../input/day06/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()

i = 0

pp = []
pps = 0
tmp = ""
tmp2 = set()
pp2 = []
pp2x = []
for line in lines:
    line = line.strip()
    print(i, line)
    tmp = tmp + " " + line
    if len(line) > 0:
        for c in line:
            #print('_',c)
            tmp2.add(c)
        print(tmp2)
        pp2x.append(tmp2)
        tmp2 = set()
    if len(line) < 1 and i > 0:
        pp.append(tmp)
        tmp = ""
        pp2.append(pp2x)
        print("#", tmp2, pp2x)
        tmp2 = set()
        pp2x = []
        continue
    i = i + 1

pp.append(tmp)
pp2.append(pp2x)
#print(pp)

for p in pp:
    tmpc = set()
    for c in p:
        if c != ' ':
            tmpc.add(c)
    print(tmpc)
    pps = pps + len(tmpc)

print("-----")
print(pp2)
c2 = 0
for p in pp2:
    if len(p) == 1:
        x = len(p[0])
        print(" . ", x, p[0])
        c2 = c2 + len(p[0])
    else:
        lst = p[0]
        done = set()
        for px in p[1:]:
            lst2 = lst.intersection(px)
            x = len(lst2)
            print(".. ", x, lst, px, lst2)
            ##dx1 = sorted(lst)
            ##dx2 = sorted(px)
            ##dx3 = ",".join(dx1 + dx2)
            ##print(dx3)
            ##if dx3 not in done:
            ##    c2 = c2 + x
            ##    done.add(dx3)
            lst = lst2
        #else:
        #    print(",,", lst)
        c2 = c2 + len(lst)
    print()

# 8361
# 8346
# 6781

if part1:
    print(pps)
else:
    print(c2)