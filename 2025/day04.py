import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

maze = []

def p(maze):
    for y in range(0, len(maze)):
        print(maze[y])
    #print(get_n(9,4,maze))
    #print(get_n(9,5,maze))
    print('-')


def get_n(y, x, maze):
    rv = []
    for iy in range(y-1, y+2):
        for ix in range(x-1,x+2):
            if iy >= 0 and iy <= len(maze)-1 and ix >= 0 and ix <= len(maze[0])-1:
                #print(iy,ix)
                if iy == y and ix == x:
                    continue
                rv.append(maze[iy][ix])
    return rv

def count(maze):
    rv = 0
    for y in range(0, len(maze)):
        for x in range(0, len(maze[0])):
            if maze[y][x] == '@':
                rv += 1
    return rv

def cp(maze):
    m = []
    for y in range(0, len(maze)):
        t = []
        for x in range(0, len(maze[0])):
            t.append(maze[y][x])
        m.append(t)
    return m

for line in lines:
    tmp = []
    for i in range(0, len(line)):
        tmp.append(line[i])
    maze.append(tmp)

#p(maze)

def run(maze):
    rv1 = 0
    for y in range(0, len(maze)):
        for x in range(0, len(maze[0])):
            if maze[y][x] != '@':
                continue
            t1 = get_n(y, x, maze)
            t2 = filter(lambda a: a == '@', t1)
            if len(list(t2)) < 4:
                rv1 += 1
    return rv1

def run2(maze):
    rv1 = 0
    m2 = cp(maze)
    for y in range(0, len(maze)):
        for x in range(0, len(maze[0])):
            if maze[y][x] != '@':
                continue
            t1 = get_n(y, x, maze)
            t2 = filter(lambda a: a == '@', t1)
            if len(list(t2)) < 4:
                rv1 += 1
                m2[y][x] = '.'
    return (rv1, m2)

if part1:
    rv1 = run(maze)
    print(rv1)
else:
    rv2 = 0
    m0 = cp(maze)
    c0 = count(m0)
    clast = c0
    cur = cp(maze)
    while True:
        (rm, m2) = run2(cur)
        c2 = count(m2)

        if c2 == clast:
            rv2 = c0 - c2
            break
        clast = c2
        last = cp(cur)
        cur = cp(m2)
        #print(c0, rm, c2)

    print(rv2)
