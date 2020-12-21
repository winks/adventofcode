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
        #print("#", line, m.groups())
        ing = m.groups()[0].split(" ")
        alle = m.groups()[1].replace(",", "").split(" ")
        #print(ing, alle)
        xlines.append((ing, alle))
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
    for line in xlines:
        print(line)
    print()
    
    #print(ia)
    #for m in mul:
    #    print(m)
    #    print("---")
    #return
    #print()
    for m in mul:
        xall = m[0]
        xing = m[1]
        cand = {}
        for xi in xing:
            some = False
            for xa in xall:
                #print(xi,"has", xa, ia[xa])
                #print("__", xa, ia)
                if xa not in ia:
                    continue
                for tmp in ia[xa]:
                    if xi in tmp:
                        some = True
                    #print(some)
                if some:
                    if xa not in cand:
                        cand[xa] = []
                    cand[xa].append(xi)
            #print()

    def flt(cand):
        lo = {}
        for i in cand.keys():
            for a in cand[i]:
                if a not in lo:
                    lo[a] = set()
                lo[a].add(i)
        #print("(((")
        #print(lo)
        rv = {}
        mmin = 1

        while len(lo.keys()) > 0:
            wo = list(lo.keys()).copy()
            for i in wo:
                if len(lo[i]) < mmin:
                    del lo[i]
                    continue
                if len(lo[i]) == 1:
                    #rv[lo[i].pop()] = i
                    rv[lo[i].pop()] = i
                    del lo[i]
                elif len(lo[i]) == mmin:
                    tmp = lo[i]
                    #print(mmin, tmp, i, rv)
                    for k in rv.keys():
                        tmp.remove(k)
                    #print(mmin, tmp)
                    rv[lo[i].pop()] = i
            mmin += 1        
            #print(rv, lo)
            #print("))))))))")
        rv2 = {}
        for k in rv.keys():
            rv2[rv[k]] = k
        return rv2

    print(cand)
    cand2 = flt(cand)
    print(cand2)
    print()

    for xl in xlines:
        #if len(xl[1]) == 1 and xl[1][0] not in cand.keys():
        if len(xl[1]) == 1 and xl[1][0] not in cand.keys():
            print(xl)
            print(xl[1][0], cand2.keys())
            cand[xl[1][0]] = xl[0]
            for i in xl[0]:
                if i not in cand2.keys():
                    cand2[i] = xl[1][0]
        print("----")
    print("??????")
    print(cand)
    print(cand2)
    print("??????")
    elim = set()
    for k in cand.keys():
        for k2 in cand[k]:
            elim.add(k2)
    print("elim",elim)
    elim = list(cand2.keys())
    print("elim",elim)

    rest = []
    for line in xlines:
        for item in line[0]:
                if item not in elim:
                    rest.append(item)
    print(len(rest), rest)
    print()

"""
    c2 = {}
    for line in xlines:
        #for a in line[1]:
        if len(line[1]) == 1:
            a = line[1][0]
            if a not in c2:
                c2[a] = set()
            for i in line[0]:
                c2[a].add(i)
        else:
            print(line[1], line[0])
    for c in c2.keys():
        print(c, c2[c])


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
