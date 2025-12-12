import functools as ft
import collections
import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

paths = {}
for line in lines:
    p = line.split(': ')
    k = p[0]
    vs = p[1].split(' ')
    #print(k, vs)
    if k not in paths:
        paths[k] = []
    for v in vs:
        paths[k].append(v)
#print(paths)

def bfs(start, end):
    rv = []
    q = collections.deque([[start]])
    seen = set([start])
    while q:
        p = q.popleft()
        p1 = p[-1]
        if p1 == end:
            rv.append(p)
            continue
        for v in paths[p1]:
            if v not in seen:
                q.append(p + [v])
                seen.add(p1)
    return rv

@ft.cache
def dfs(start, end):
    r = 0
    for x in paths[start]:
        if x == end:
            r += 1
        elif x not in paths:
            continue
        else:
            r += dfs(x, end)
    return r

if part1:
    rv = bfs('you', 'out')
    print(len(rv))
else:
    r1 = dfs('svr', 'fft')
    r2 = dfs('fft', 'dac')
    r3 = dfs('dac', 'out')
    print((r1)*(r2)*(r3))
