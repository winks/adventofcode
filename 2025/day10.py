import itertools
import numpy
import scipy.optimize as opt
import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def parse(line):
    ild = [1 if x == '#' else 0 for x in line.split(' ')[0][1:-1]]
    btns = line[line.find(']')+1:line.find('{')].strip().split(' ')
    btns = list(map(lambda s: s[1:-1], btns))
    btns = list(map(lambda s: list(map(lambda a: int(a), s.split(','))), btns))
    jolt = line.split('{')[1].replace('}','').split(',')
    jolt = list(map(lambda s: int(s), jolt))
    bbtns = []
    for br in btns:
        t = []
        for i in range(0, len(ild)):
            if i in br:
                t.append(1)
            else:
                t.append(0)
        bbtns.append(t)
    return (ild, bbtns, jolt)

def h1(pp, ild):
    for px in pp:
        s = [0] * len(ild)
        for p in px:
            for pi in range(0, len(s)):
                s[pi] += p[pi]
        s = list(map(lambda x: 0 if x % 2 == 0 else 1, s))
        if s == ild:
            return i
    return 0

if part1:
    rv1 = []
    for line in lines:
        (ild, bbtns, jolt) = parse(line)
        for i in range(1, 11):
            pp = list(itertools.combinations(bbtns, i))
            r = h1(pp, ild)
            if r > 0:
                rv1.append(r)
                break

    print(sum(rv1))
else:
    rv2 = []
    for line in lines:
        (ild, bbtns, jolt) = parse(line)
        pm = []
        for j in jolt:
            pm.append([])
        for i in range(0, len(bbtns)):
            for j in range(0, len(jolt)):
                pm[j].append(bbtns[i][j])

        cons = [opt.LinearConstraint(pm, lb=jolt, ub=jolt)]
        c = numpy.ones(len(bbtns), dtype=float)
        integ = numpy.ones(len(bbtns), dtype=int)
        bounds = opt.Bounds(lb=numpy.zeros(len(bbtns)),
                            ub=numpy.full(len(bbtns), numpy.inf))
        rv = opt.milp(c=c, constraints=cons, integrality=integ, bounds=bounds)
        rv2.append(int(round(rv.fun)))
    print(sum(rv2))

