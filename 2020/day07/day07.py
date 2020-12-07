import sys
import re

fname = '../input/day07/input.txt'
#fname = '../input/day07/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()

re0 = re.compile(r'^(\w+ \w+) bags contain (no other|[^\.]+) bags?\.$')
re1 = re.compile(r'(\d+) (\w+ \w+)( bags?)?')

bags = {}
i = 0
for line in lines:
    line = line.strip()
    m = re0.findall(line)
    #print(m[0])
    k = m[0][0]
    v = m[0][1]
    if v == 'no other':
        bags[k] = None
    else:
        p = v.split(', ')
        #print(p)
        if len(p) == 1:
            m = re1.findall(p[0])
            bags[k] = {m[0][1]: m[0][0]}
        else:
            tmp = {}
            for b in p:
                m = re1.findall(b)
                #print(m)
                tmp[m[0][1]] = m[0][0]
            bags[k] = tmp

#print(bags)

def ppart1(item):
    tmp = set()
    todo = [item]
    while len(todo) > 0:
        to = todo.pop()
        for k,v in bags.items():
            #print(k,v)
            if v is None:
                continue
            for b in v.keys():
                if b == to:
                    tmp.add(k)
                    todo.append(k)
    return tmp

def ppart2(item):
    c = 0
    if item not in bags.keys():
        return 0
    m = bags[item]
    if m is None:
        #print('_r', item)
        return 1
    tc = 0
    for k in m.keys():
        n = ppart2(k)
        n2 = n * int(m[k])
        #print("#", k, n, n2)
        tc = 1 + tc + int(m[k]) * n
        #print(tc, m[k], n)
        c = c + n2
    return c + 1

if part1:
    tmp = ppart1('shiny gold')
    print(len(tmp))
else:
    tmp = ppart2('shiny gold')
    print(tmp - 1)
