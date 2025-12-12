import functools
import itertools
import math
import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def pp(maze):
    for y in range(0, len(maze)):
        print(''.join(map(lambda x: str(x).replace("0","."), maze[y])))

def size(part):
    rv = 0
    for y in part:
        rv += sum(y)
    return rv

parts = []
part = []
for line in lines[0:30]:
    if len(line) == 0:
        parts.append(part)
        part = []
        continue
    if ':' in line:
        continue

    pt = []
    for f in line:
        pt.append(0 if f == '.' else 1)
    part.append(pt)

#for p in parts:
#    pp(p)
#    print(size(p))
#    print()

rv = 0
for line in lines[30:]:
    if len(line) < 1:
        continue
    a = line.split(':')
    (xl, yl) = list(map(lambda a: int(a), a[0].split('x')))
    todo = list(map(lambda a: int(a), a[1].strip().split(' ')))
    sm = 0
    for i in range(0, len(todo)):
        sz = size(parts[i])
        sm += sz * todo[i]
    if sm > xl*yl:
        #print("too small")
        continue
    xx = math.floor(xl/3)
    yy = math.floor(yl/3)
    if xx * yy >= sum(todo):
        rv += 1

print(rv)
