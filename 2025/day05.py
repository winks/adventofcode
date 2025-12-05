import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

fresh = {}
sp = []
rv1 = {}

def chk(num, fresh):
    for i in fresh.keys():
        if num >= i:
            for v in fresh[i]:
                if num <= v:
                    return num
    return None

if part1:
    i = 0
    for line in lines:
        if len(line.strip()) == 0:
            continue
        if '-' in line:
            p = line.split('-')
            k = int(p[0])
            v = int(p[1])
            if k in fresh:
                fresh[k].append(v)
            else:
                fresh[k] = [v]
        else:
            i += 1
            num = int(line)
            r = chk(num, fresh)
            if r is not None:
                rv1[num] = True
    print(len(rv1.keys()))
else:
    rv2 = 0
    for line in lines:
        if len(line.strip()) == 0:
            break
        if '-' in line:
            p = line.split('-')
            k = int(p[0])
            v = int(p[1])
            if k in fresh:
                if v > fresh[k]:
                    fresh[k] = v
            else:
                fresh[k] = v

    def merge(fresh):
        first = True
        lastk = 0
        for k in sorted(fresh.keys()):
            if first:
                first = False
                lastk = k
                continue
            v = fresh[k]
            if k <= fresh[lastk]:
                fresh[lastk] = max(v, fresh[lastk])
                del fresh[k]
                return fresh
            if v <= fresh[lastk]:
                fresh[lastk] = v
                del fresh[k]
                return fresh
            lastk = k
        return fresh

    le0 = len(fresh.keys())
    m = fresh

    while True:
        m = merge(m)
        if len(m.keys()) == le0:
            break
        else:
            le0 = len(m.keys())

    for k in m.keys():
        rv2 += (m[k] - k + 1)
    print(rv2)

