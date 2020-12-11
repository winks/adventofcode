import sys
import timeit

fname = '../input/day11/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def neigh(lines, y, x):
    occ = 0
    ne = []
    rows = len(lines)
    cols = len(lines[0])
    for yy in range(y-1, y+2):
        if yy < 0 or yy >= rows:
            continue
        for xx in range(x-1, x+2):
            if xx < 0 or xx >= cols:
                continue
            if yy == y and xx == x:
                continue
            ne.append((yy,xx))
            if lines[yy][xx] == '#':
                occ += 1
    return (occ, ne)

def neigh2(lines, y, x, d=False):
    occ = 0
    ne = []
    rows = len(lines)
    cols = len(lines[0])
    for direc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        for i in range(1, len(lines) * len(lines[0])):
            yy = y + i * direc[0]
            xx = x + i * direc[1]
            if yy < 0 or xx < 0:
                continue
            if yy == y and xx == x:
                continue
            if yy >= rows or xx >= cols:
                continue
            if d:
                print('looking at',yy,xx,'=',lines[yy][xx],direc)
            if lines[yy][xx] == '#':
                ne.append((yy,xx))
                occ += 1
                break
            if lines[yy][xx] == 'L':
                break
    return (occ, ne)

def fmt(lines, y1=None, x1=None):
    for y in range(0, len(lines)):
        a = ""
        for x in range(0, len(lines[y])):
            if x1 is None and y1 is None:
                a += lines[y][x]
            else:
                if x1 == x and y1 == y:
                    a += '@'
                else:
                    a += lines[y][x]
        print(a)
    print('------------------')

def cnt(lines, char):
    c = 0
    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            if lines[y][x] == char:
                c += 1
    return c

def eq(l1,l2):
    ll1 = len(l1)
    if ll1 != len(l2):
        return False
    for y in range(0, ll1):
        if l1[y] != l2[y]:
            return False
    return True

def run1(lines):
    l2 = lines.copy()
    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            if lines[y][x] == '.':
                continue
            ne = neigh(lines, y, x)
            if ne[0] == 0 and lines[y][x] == 'L':
                l2[y] = l2[y][0:x] + '#' + l2[y][x+1:]
            if ne[0] >= 4 and lines[y][x] == '#':
                l2[y] = l2[y][0:x] + 'L' + l2[y][x+1:]

    return l2

def run2(lines):
    l2 = lines.copy()
    for y in range(0, len(lines)):
        for x in range(0, len(lines[y])):
            ne = neigh2(lines, y, x)
            if lines[y][x] == '.':
                continue
            if ne[0] == 0 and lines[y][x] == 'L':
                l2[y] = l2[y][0:x] + '#' + l2[y][x+1:]
            if ne[0] >= 5 and lines[y][x] == '#':
                l2[y] = l2[y][0:x] + 'L' + l2[y][x+1:]

    return l2

def ppart(lines,func):
    l0 = lines.copy()
    l1 = func(lines.copy())
    it = 1

    while not eq(l1, l0):
        l0 = l1
        l1 = func(l0)
        it += 1

    print("# After",it,"runs:")
    return cnt(l1, '#')


start = timeit.default_timer()
if part1:
    num = ppart(lines, run1)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    num = ppart(lines, run2)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
