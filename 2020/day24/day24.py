import sys
import timeit
import re
from copy import deepcopy

fname = '../input/day24/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def pprint(g, quiet=False):
    cb = 0
    em = '. ' * len(g)
    if not quiet:
        print('#',em)
    for row in g:
        for t in row:
            if t == 'b':
                cb += 1
        if not quiet:
            r = ' '.join(row).replace('w', '.')
            if 'b' in r:
                print("#", r)
    if not quiet:
        print('#',em)
        print("# {} black tiles".format(cb))
    return cb

def ppart1(lines, off=None):
    OFF = 5
    if len(lines) > 50:
        OFF = 16
    if off:
        OFF = off
    ground = []
    for y in range(0, 3*OFF):
        ground.append([])
        for x in range(0, 3*OFF):
            ground[y].append('w')
    #pprint(ground)

    ok = {'se': (1, -1), 'sw': (0, -1), 'nw': (-1, 1), 'ne': (0, 1), 'e': (1, 0), 'w': (-1, 0)}
    ins = []

    for line in lines:
        dirs = []
        pos = 0
        #print(line)
        while pos != len(line):
            if line[pos:pos+2] == 'se':
                dirs.append("se")
                pos +=  2
            elif line[pos:pos+2] == 'sw':
                dirs.append("sw")
                pos +=  2
            elif line[pos:pos+2] == 'nw':
                dirs.append("nw")
                pos +=  2
            elif line[pos:pos+2] == 'ne':
                dirs.append("ne")
                pos +=  2
            elif line[pos:pos+1] == 'e':
                dirs.append("e")
                pos +=  1
            elif line[pos:pos+1] == 'w':
                dirs.append("w")
                pos +=  1
            else:
                print("meh")

        #print(dirs)
        if pos != len(line):
            print(len(line), len(dirs), pos)
            print(line[pos:])
        bork = list(filter(lambda s: s not in ok, dirs))
        if len(bork) > 0:
            print("bork", bork)
        ins.append(dirs)

    xx = {}
    for tile in ins:
        pos = (OFF, OFF)
        for step in tile:
            pos = (pos[0] + ok[step][1], pos[1] + ok[step][0])
        x = "{}_{}".format(pos[0], pos[1])
        if x not in xx:
            xx[x] = 0
        xx[x] += 1
        if ground[pos[0]][pos[1]] == 'w':
            ground[pos[0]][pos[1]] = 'b'
        elif ground[pos[0]][pos[1]] == 'b':
            ground[pos[0]][pos[1]] = 'w'
    return (pprint(ground), ground)

def neigh(tile):
    ok = {'se': (1, -1), 'sw': (0, -1), 'nw': (-1, 1), 'ne': (0, 1), 'e': (1, 0), 'w': (-1, 0)}

    ne = []
    for k in ok.keys():
        ne.append((tile[0] + ok[k][1], tile[1] + ok[k][0]))
    return ne

def flip(tile_color, neigh, grid):
    b = 0
    for ne in neigh:
        if 0 <= ne[1] < len(grid) and 0 <= ne[0] < len(grid):
            if grid[ne[1]][ne[0]] == 'b':
                b += 1
    if tile_color == 'b' and (b == 0 or b > 2):
        return True
    if tile_color == 'w' and b == 2:
        return True
    return False

def ppart2(grid):
    rv = 0
    for i in range(0, 100):
        orig = deepcopy(grid)
        for y in range(0, len(orig)):
            for x in range(0, len(orig[0])):
                nex = neigh((x, y))
                will_flip = flip(orig[y][x], nex, orig)
                if will_flip:
                    if grid[y][x] == 'b':
                        grid[y][x] = 'w'
                    else:
                        grid[y][x] = 'b'
        rv = pprint(grid, True)
        if i < 10 or i % 10 == 0:
            print("#",i,'=',rv)
    #pprint(grid)
    return rv

start = timeit.default_timer()
if part1:
    (num, grid) = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    off = 47
    if len(lines) > 20:
        off = 100
    (_, grid) = ppart1(lines, off)
    num = ppart2(grid)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
