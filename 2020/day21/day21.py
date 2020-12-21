import sys
import timeit
import re
from copy import deepcopy

fname = '../input/day21/input.txt'
#fname = '../input/day21/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    p = re.compile('(.*) \(contains (.*)\)$')
    allall = set()
    xlines = []
    for line in lines:
        m = p.match(line)
        if not m:
            continue
        ing = m.groups()[0].split(" ")
        alle = m.groups()[1].replace(",", "").split(" ")
        xlines.append((set(ing), alle))
        for a in alle:
            allall.add(a)

    dx = {}
    for a in allall:
        for xl in xlines:
            if a not in xl[1]:
                continue
            if a not in dx:
                dx[a] = []
            dx[a].append(xl[0])

    xx = {}
    xy = {}
    for a in dx.keys():
        if len(dx[a]) == 1:
            continue
        common = set(dx[a][0])
        for li in range(1, len(dx[a])):
            common = common & dx[a][li]
        if len(common) == 1:
            xx[a] = common
        elif len(common) > 0:
            xy[a] = common

    elim = set()
    for k in xx.keys():
        elim = elim | xx[k]

    todo = list(xy.keys()).copy()
    while True:
        k = todo.pop()
        tmp = xy[k] - elim
        if len(tmp) == 1:
            xx[k] = tmp
            elim = elim | tmp
            del xy[k]
        else:
            todo.insert(0, k)
        if len(xy) == 0:
            break

    for a in dx.keys():
        if len(dx[a]) != 1:
            continue
        for li in dx[a]:
            tmp = set()
            for i in li:
                if i not in elim:
                    tmp.add(i)
            if len(tmp) == 1:
                xx[a] = tmp
                elim = elim | tmp

    rest = []
    for line in xlines:
        for item in line[0]:
            if item not in elim:
                rest.append(item)

    return (len(rest), xx)

def ppart2(xx):
    rv = []
    for kx in sorted(xx.keys()):
        rv.append(xx[kx].pop())
    return ",".join(rv)

start = timeit.default_timer()
if part1:
    (num, _) = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    (_, foo) = ppart1(lines)
    num = ppart2(foo)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
