import sys
import timeit
from copy import deepcopy

fname = '../input/day17/input.txt'
#fname = '../input/day17/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def pprint(m, layer=False, hyper=False):
    def pm(m):
        print('+-+')
        for line in m:
            print(" ".join(line))
        print('+-+')

    def pl(m,i=None):
        print('.----------------.',i and i)
        for la in m:
            pm(la)
        print('\----------------/')

    if hyper:
        print('.================.')
        for hx in range(0, len(m)):
            pl(m[hx], hx)
        print('\================/')
    elif layer:
        pl(m)
    else:
        pm(m)

def cnt3(m, z, y, x):
    direc = []
    for i1 in range(-1,2):
        for i2 in range(-1,2):
            for i3 in range(-1,2):
                if not (i1 == 0 and i2 == 0 and i3 == 0):
                    direc.append((i1, i2, i3))
    act = 0
    for d in direc:
        if z+d[0] < 0 or z+d[0]+1 > len(m):
            continue
        if y+d[1] < 0 or y+d[1]+1 > len(m[0]):
            continue
        if x+d[2] < 0 or x+d[2]+1 > len(m[0][0]):
            continue
        if m[z+d[0]][y+d[1]][x+d[2]] == '#':
            act += 1
    return act

def cnt4(m, w, z, y, x):
    direc = []
    for i1 in range(-1,2):
        for i2 in range(-1,2):
            for i3 in range(-1,2):
                for i4 in range(-1,2):
                    if not (i1 == 0 and i2 == 0 and i3 == 0 and i4 == 0):
                        direc.append((i1, i2, i3, i4))
    act = 0
    for d in direc:
        if w+d[0] < 0 or w+d[0]+1 > len(m):
            continue
        if z+d[1] < 0 or z+d[1]+1 > len(m[0]):
            continue
        if y+d[2] < 0 or y+d[2]+1 > len(m[0][0]):
            continue
        if x+d[3] < 0 or x+d[3]+1 > len(m[0][0][0]):
            continue
        if m[w+d[0]][z+d[1]][y+d[2]][x+d[3]] == '#':
            act += 1
    return act

def cycle3(lm):
    lm2 = deepcopy(lm)
    for z in range(0, len(lm2)):
        for y in range(0, len(lm2[0])):
            for x in range(0, len(lm2[0])):
                c = cnt3(lm, z, y, x)
                if lm[z][y][x] == '#':
                    if 2 <= c <= 3:
                        lm2[z][y][x] = '#'
                    else:
                        lm2[z][y][x] = '.'
                if lm[z][y][x] == '.' and c == 3:
                    lm2[z][y][x] = '#'
    return lm2

def cycle4(lm, OFF=0):
    lm2 = deepcopy(lm)
    for w in range(0, len(lm2)):
        for z in range(0, len(lm2[0])):
            for y in range(0, len(lm2[0][0])):
                for x in range(0, len(lm2[0][0])):
                    c = cnt4(lm, w, z, y, x)
                    if lm[w][z][y][x] == '#':
                        if 2 <= c <= 3:
                            lm2[w][z][y][x] = '#'
                        else:
                            lm2[w][z][y][x] = '.'
                    if lm[w][z][y][x] == '.' and c == 3:
                        lm2[w][z][y][x] = '#'
    return lm2

def summ3(m):
    c = 0
    for z in m:
        for y in z:
            for x in y:
                if x == '#':
                    c += 1
    return c

def summ4(m):
    c = 0
    for w in m:
        for z in w:
            for y in z:
                for x in y:
                    if x == '#':
                        c += 1
    return c

def fresh(lines, OFF):
    m = []
    for row in range(0, len(lines)+2*OFF):
        for col in range(0, len(lines)+2*OFF):
            if len(m) <= row:
                m.append([])
            if len(m[row]) <= col:
                m[row].append([])
            m[row][col] = '.'
    return m

def layerize3(lines, OFF, m, use_m=True):
    layers = []
    m0 = deepcopy(m)
    for i in range(0, OFF-2):
        layers.append(deepcopy(m0))

    for row in range(0, len(lines)):
        for col in range(0, len(lines)):
            m[row+OFF][col+OFF] = lines[row][col]

    if use_m:
        layers.append(m)
    else:
        layers.append(deepcopy(m0))

    for i in range(0, OFF-2):
        layers.append(deepcopy(m0))

    return layers

def ppart1(lines):
    OFF = 10
    m = fresh(lines, OFF)
    layers = layerize3(lines, OFF, m)

    for i in range(0, 6):
        m1 = cycle3(layers)
        layers = m1
    return summ3(m1)

def ppart2(lines):
    OFF = 10
    m = fresh(lines, OFF)
    layers = layerize3(lines, OFF, deepcopy(m))
    layer_e = layerize3(lines, OFF, deepcopy(m), False)

    layers4 = []
    for i in range(0, OFF-4):
        layers4.append(deepcopy(layer_e))
    layers4.append(layers)
    for i in range(0, OFF-4):
        layers4.append(deepcopy(layer_e))

    for i in range(0, 6):
        m1 = cycle4(layers4, OFF)
        layers4 = m1
    return summ4(m1)

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

"""
    def cycle(m):
        m2 = deepcopy(m)
        for y in range(0, len(m2)):
            for x in range(0, len(m2)):
                c = cnt(m, y, x)
                if m[y][x] == '#':
                    if 2 <= c <= 3:
                        m2[y][x] = '#'
                    else:
                        m2[y][x] = '.'
                if m[y][x] == '.' and c == 3:
                    m2[y][x] = '#'
                #print((y, x), cnt(m, y, x))
        return m


    #def fresh():
    #    return [['.','.','.'],['.','.','.'],['.','.','.']]
    
    def cnt(m, y, x):
        direc = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        act = 0
        for d in direc:
            if y+d[0] < 0 or y+d[0]+1 > len(m):
                #print("  err", y)
                continue
            if x+d[1] < 0 or x+d[1]+1 > len(m[0]):
                #print("  err", x)
                continue
            if m[y+d[0]][x+d[1]] == '#':
                act += 1
        return act

"""