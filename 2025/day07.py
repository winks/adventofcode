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

for line in lines:
    tmp = []
    for i in range(0, len(line)):
        tmp.append(line[i])
    maze.append(tmp)

def pp(maze):
    for y in range(0, len(maze)):
        print(''.join(maze[y]))

def cp(maze):
    m = []
    for y in range(0, len(maze)):
        t = []
        for x in range(0, len(maze[0])):
            t.append(maze[y][x])
        m.append(t)
    return m

def get_n(y, x, maze):
    rv = []
    for iy in range(y-1, y+2):
        for ix in range(x-1,x+2):
            if iy >= 0 and iy <= len(maze)-1 and ix >= 0 and ix <= len(maze[0])-1:
                if iy == y and ix == x:
                    continue
                rv.append(maze[iy][ix])
    return rv

def get_start(maze):
    for y in range(0, len(maze)):
        for x in range(0, len(maze[0])):
            if maze[y][x] == 'S':
                return (y,x)
    return None

def upd(maze, beams):
    for b in beams:
        maze[b[0]][b[1]] = '|'
    return maze

def down(maze, cur):
    acc = set()
    spc = 0
    for c in cur:
        if c[0] + 1 >= len(maze):
            return (None, spc)
        n = maze[c[0]+1][c[1]]
        #print(c,n)
        if n == '.':
            acc.add((c[0]+1,c[1]))
        elif  n == '^':
            acc.add((c[0]+1,c[1]-1))
            acc.add((c[0]+1,c[1]+1))
            spc += 1
    return (acc, spc)

def down2(maze, cur):
    acc = {}
    for c in cur.keys():
        cv = cur[c]
        if c[0] + 1 >= len(maze):
            return None
        ny = c[0]+1
        n = maze[ny][c[1]]
        if n == '.':
            cd = (ny,c[1])
            if cd not in acc:
                acc[cd] = 0
            acc[cd] += cv
        elif n == '^':
            cl = (ny,c[1]-1)
            cr = (ny,c[1]+1)
            if cl not in acc:
                acc[cl] = 0
            if cr not in acc:
                acc[cr] = 0
            acc[cl] += cv
            acc[cr] += cv
    return acc

if part1:
    pp(maze)
    s = get_start(maze)
    count = 0
    nxt = [s]
    while True:
        (n, c) = down(maze, nxt)
        if n is None:
            break
        count += c
        maze = upd(maze, n)
        nxt = n
    pp(maze)
    print(count)
else:
    s = tuple(get_start(maze))
    nxt = {s: 1}
    while True:
        n = down2(maze, nxt)
        if n is None:
            break
        nxt = n
    print(sum(nxt.values()))
