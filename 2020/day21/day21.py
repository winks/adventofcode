import sys
import timeit
import re
from copy import deepcopy

fname = '../input/day21/input.txt'
fname = '../input/day21/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    p = re.compile('(.*) \(contains (.*)\)$')
    ai = {}
    ia = {}
    mul = []
    xlines = []
    for line in lines:
        m = p.match(line)
        if not m:
            continue
        print("#", line, m.groups())
        ing = m.groups()[0].split(" ")
        alle = m.groups()[1].replace(",", "").split(" ")
        print(ing, alle)
        xlines.append(ing)
        for i in ing:
            if i not in ai:
                ai[i] = set()
            for a in alle:
                ai[i].add(a)
        if len(alle) == 1:
            a = alle[0]
            if a not in ia:
                ia[a] = []
            ia[a].append(ing)
        else:
            mul.append((alle, ing))
    print()
    print(ai)
    
    print(ia)
    print(mul)
    print()
    for m in mul:
        xall = m[0]
        xing = m[1]
        cand = {}
        for xi in xing:
            some = False
            for xa in xall:
                #print(xi,"has", xa, ia[xa])
                for tmp in ia[xa]:
                    if xi in tmp:
                        some = True
                    #print(some)
                if some:
                    if xa not in cand:
                        cand[xa] = []
                    cand[xa].append(xi)
            print()
    print(cand)
    print()
    
    elim = set()
    ai2 = deepcopy(ai)
    print(ai2)
    for xi in ai2.keys():
        for ca in cand.keys():
            if ca in ai2[xi]:
                ai2[xi].remove(ca)
            for cc in cand[ca]:
                elim.add(cc)
    print(ai2)
    print(elim)

    cand2 = []
    for k in ia.keys():
        if k in cand:
            continue
        print(k, ia[k])
        for li in ia[k]:
            for ing in li:
                if ing in elim:
                    continue
                cand2.append((ing, k))
    print(cand2)
    for c in cand2:
        if c[0] in ai2 and c[1] in ai2[c[0]]:
            elim.add(c[0])
            ai2[c[0]].remove(c[1])
            cand[c[1]] = [c[0]]
    for k in ai2:
        pass
    print(cand)
    print(ai2)
    print(elim)
    for k in cand.keys():
        for x in ai2.keys():
            if k in ai2[x]:
                ai2[x].remove(k)
    print(ai2)
    print()
    print(xlines)
    rest = []
    for line in xlines:
        for item in line:
            if item not in elim:
                rest.append(item)
    print(len(rest), rest)

"""
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)

kfcds nhms
trh fvjkl sbzzf
fvjkl (contains soy)
sbzzf 

kfcds nhms
trh sbzzf
sbzzf 
"""

def ppart2(lines):
    pass

start = timeit.default_timer()
if part1:
    num = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    num = ppart2(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
