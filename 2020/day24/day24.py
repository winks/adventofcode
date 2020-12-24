import sys
import timeit
import re

fname = '../input/day24/input.txt'
#fname = '../input/day24/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def pprint(g):
    cb = 0
    for row in g:
        for t in row:
            if t == 'b':
                cb += 1
        print(' '.join(row).replace('w', '.'))
    print("{} black tiles".format(cb))
    return cb

def ppart1(lines):
    OFF = 4
    if len(lines) > 50:
        OFF = 15
    ground = []
    for y in range(0, 3*OFF):
        ground.append([])
        for x in range(0, 3*OFF):
            ground[y].append('w')
    pprint(ground)

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
        #break
    return (pprint(ground), ground)


def ppart2(grid):
    pass

start = timeit.default_timer()
if part1:
    (num, grid) = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    (num, grid) = ppart1(grid)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
