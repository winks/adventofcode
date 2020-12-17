import sys
import timeit
from copy import deepcopy

fname = '../input/day17/input.txt'
fname = '../input/day17/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def pprint(m, layer=False):
    def x(m):
        for line in m:
            print(" ".join(line))
        print('---')
    
    if layer:
        for la in m:
            x(la)
        print('---------')
    else:
        x(m)

def ppart1(lines):
    #lines = list(map(int, lines.split(',')))
    OFF = 2
    layers = []
    m = []
    for row in range(0, len(lines)+2*OFF):
        for col in range(0, len(lines)+2*OFF):
            #print((row,col))
            #if len(m) <= col:
            if len(m) <= row:
                m.append([])
            #if len(m[col])<= row:
            if len(m[row]) <= col:
                #m[col].append([])
                m[row].append([])
            #m[col][row] = lines[row][col]
            #if col > len(lines):
            #    m[row][col] = '_'
            #elif row > len(m):
            #    print(3)
            #else:
            #    print(m, row, col)
            #    m[row][col] = lines[row][col]
            m[row][col] = '.'
    m0 = deepcopy(m)
    pprint(m)
    layers.append(deepcopy(m0), deepcopy(m0), deepcopy(m0))

    for row in range(0, len(lines)):
        for col in range(0, len(lines)):
            m[row+OFF][col+OFF] = lines[row][col]
    pprint(m)

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
        
        
        pprint(m2)
        


    m1 = cycle(m)


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
