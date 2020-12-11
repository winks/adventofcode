import sys
import timeit

fname = '../input/day11/input.txt'
#fname = '../input/day11/test'

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
    for yy in range(y-1, y+2):
        for xx in range(x-1, x+2):
            if yy == y and xx == x:
                continue
            if yy < 0 or xx < 0:
                continue
            if yy >= len(lines) or xx >= len(lines[y]):
                continue
            ne.append((yy,xx))
    for a in ne:
        #print(a)
        if lines[a[0]][a[1]] == '#':
            occ += 1
    return (occ, ne)

def neigh2(lines, y, x, d=False):
    occ = 0
    ne = []
    #print('ne2',y,x)
    for direc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        #print('dir',direc)
        for i in range(1, len(lines) * len(lines[0])):
            yy = y + i * direc[0]
            xx = x + i * direc[1]
            #print('looking at',yy,xx,'=',lines[yy][xx])
            if yy == y and xx == x:
                continue
            if yy < 0 or xx < 0:
                continue
            if yy >= len(lines) or xx >= len(lines[y]):
                continue
            if d:
                print('looking at',yy,xx,'=',lines[yy][xx],direc)
            if lines[yy][xx] == '#':
                ne.append((yy,xx))
                break
            if lines[yy][xx] == 'L':
                break
            #i += 1
    for a in ne:
        #print(a)
        if lines[a[0]][a[1]] == '#':
            occ += 1
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
    if len(l1) != len(l2):
        #print('__len', len(l1))
        return False
    for y in range(0, len(l1)):
        if l1[y] != l2[y]:
            #print('__eq', y, l1[y], l2[y])
            return False
    return True

def ppart2(lines):
    #print(cnt(lines, 'L'))
    #fmt(lines)
    def run(lines,d=False):
        l2 = lines.copy()
        for y in range(0, len(lines)):
            for x in range(0, len(lines[y])):
                ne = neigh2(lines, y, x)
                if lines[y][x] == '.':
                    continue
                if lines[y][x] == 'L' and ne[0] == 0:
                    #l2[y][x] = '#'
                    l2[y] = l2[y][0:x] + '#' + l2[y][x+1:]
                if lines[y][x] == '#' and ne[0] >= 5:
                    #l2[y][x] = 'L'
                    l2[y] = l2[y][0:x] + 'L' + l2[y][x+1:]
        if d:
            print(lines[0])
            print(lines[1])
            print(lines[2])
            print(lines[3])
            print()
            print(l2[0])
            print(l2[1])
            print(l2[2])
            print(l2[3])
            for x in range(0, len(lines[0])):
                print(neigh(lines, 0, x)[0], neigh(lines, 1, x)[0], neigh(lines, 2, x)[0], neigh(lines, 3, x)[0])
            print()

        return l2
    l0 = lines.copy()
    l1 = run(lines.copy())
    it = 1

    #fmt(l1)
    #print(neigh2(l1,1,0,True))
    #print(neigh2(l1,1,1,True))
    #l0 = l1
    #l1 = run(l1,d=True)
    #fmt(l1)

    #print(neigh2(l0,2,0,True))
    #return

    while not eq(l1, l0): # and it < 2:
        l0 = l1
        l1 = run(l0)
        #fmt(l1)
        #print('---',cnt(l1, '#'))
        it += 1

    print("After",it,"runs:",cnt(l1, '#'))

def ppart1(lines):
    print(cnt(lines, 'L'))
    fmt(lines)
    #print(neigh(lines, 0, 0))
    #print(fmt(lines, 0, 1))
    #print(neigh(lines, 0, 1))
    def run(lines,d=False):
        l2 = lines.copy()
        for y in range(0, len(lines)):
            for x in range(0, len(lines[y])):
                ne = neigh(lines, y, x)
                if lines[y][x] == 'L' and ne[0] == 0:
                    #l2[y][x] = '#'
                    l2[y] = l2[y][0:x] + '#' + l2[y][x+1:]
                if lines[y][x] == '#' and ne[0] >= 4:
                    #l2[y][x] = 'L'
                    l2[y] = l2[y][0:x] + 'L' + l2[y][x+1:]
        if d:
            print(lines[0])
            print(lines[1])
            for x in range(0, len(lines[0])):
                print(neigh(lines, 0, x)[0], neigh(lines, 1, x)[0])
            print()
            print(l2[0])
            print(l2[1])
            print()

        return l2
    #l2 = run(lines)
    #print(cnt(l2, '#'))
    #fmt(l2)
    #print('---', cnt(l2, '#'))
    ##l3 = run(l2, True)
    #l3 = run(l2)
    #fmt(l3)
    #print('---', cnt(l3, '#'))
    #l4 = run(l3)
    #fmt(l4)
    #print('---', cnt(l4, '#'))
    #l5 = run(l4)
    #fmt(l5)
    #print('---', cnt(l5, '#'))
    #print(l5 == l4)
    #l6 = run(l5)
    #fmt(l6)
    #print('---', cnt(l6, '#'))
    #print(l6 == l5, eq(l6,l5))
    #l7 = run(l6)
    #fmt(l7)
    #print('---', cnt(l7, '#'))
    #print(l7 == l6, eq(l7,l6))
    l0 = lines.copy()
    l1 = run(lines.copy())
    it = 1
    while not eq(l1, l0):
        l0 = l1
        l1 = run(l0)
        it += 1

    print("After",it,"runs:",cnt(l1, '#'))

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
