import sys
import re

fname = '../input/day07/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()

re0 = re.compile(r'^(\w+ \w+) bags contain (no other|[^\.]+) bags?\.$')
re1 = re.compile(r'(\d+) (\w+ \w+)( bags?)?')

bags = {}
for line in lines:
    line = line.strip()
    m = re0.findall(line)
    k = m[0][0]
    v = m[0][1]
    if v == 'no other':
        bags[k] = None
    else:
        p = v.split(', ')
        if len(p) == 1:
            m = re1.findall(p[0])[0]
            bags[k] = {m[1]: m[0]}
        else:
            tmp = {}
            for b in p:
                m = re1.findall(b)[0]
                tmp[m[1]] = m[0]
            bags[k] = tmp

def ppart1(item):
    tmp = set()
    todo = [item]
    while len(todo) > 0:
        to = todo.pop()
        for k,v in bags.items():
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
    if bags[item] is None:
        return 1
    for k in bags[item].keys():
        c = c +  int(bags[item][k]) * ppart2(k)
    return c + 1

if part1:
    tmp = ppart1('shiny gold')
    print(len(tmp))
else:
    tmp = ppart2('shiny gold')
    print(tmp - 1)
