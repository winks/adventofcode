import collections
import re
import sys
from collections import defaultdict


def pm(lvl):
    for row in lvl:
        print(''.join(row))

def get_level(lines):
    w = 0
    h = len(lines)
    for i in range(0, len(lines)):
        if len(lines[i]) > w:
            w = len(lines[i])
    m = []
    m2 = []
    print(w,h)
    for i in range(0, w):
        t = []
        for j in range(0, h):
            mw = len(lines[i])
            if (j >= mw and mw < w):
                t.append("_")
            else:
                t.append(lines[i][j])
        m.append(t)
        m2.append(t)
    return (m, w, h, m2)

def bfs(grid, width, height, start, end):
    start = (start[0], start[1])
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if x == end[0] and y == end[1]:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != '#' and grid[y2][x2] != "B" and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def bfs2(grid, width, height, start, end, polookup, pocoords):
    start = (start[0], start[1])
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if x == end[0] and y == end[1]:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            seen2 = set()
            cell = grid[y2][x2]
            if 0 <= x2 < width and 0 <= y2 < height and cell != '#' and not re.match(r"[A-Z]", cell) and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                #print("XX", x2,y2)
                seen2.add((x2, y2))
            poc = (y2, x2)
            if poc in pocoords:
                pol = pocoords[poc]
                #print("Found portal",poc,"=",pol)
                #print("P",path)
                #print("S1",seen)
                #print("S2",seen2)
                #print("Q",queue)
                #print("===")
                if cell == pol[0]:
                    other_end = polookup[pol]
                else:
                    other_end = polookup[(pol[1],pol[0])]
                #print("TO", other_end)
                nn = path + [(other_end[1], other_end[0])]
                nn.insert(0, (0,0))
                #print("NN",nn)
                queue.append(nn)
                seen2.add((x2, y2))
            for s in seen2:
                seen.add(s)
            


def neighbors(cell, level):
    rv = []
    [x,y] = cell
    test = [ [x-1,y], [x+1,y], [x,y-1], [x,y+1] ]
    for t in test:
        rv.append(t)
    return rv

def find_portals(level, w, h):
    rv = {}
    def m(s):
        return re.match(r"[A-Z]", s)
    for x in range(1, w-1):
        for y in range(1,h-1):
            c = level[x][y]
            ne = neighbors((x,y), level)
            if m(c):
                found = False
                c1 = None
                
                for n in ne:
                    if level[n[0]][n[1]] == '.':
                        found = True
                        c1 = n
                if found:
                    sec = None
                    c2 = None
                    for n in ne:
                        if m(level[n[0]][n[1]]):
                            sec = level[n[0]][n[1]]
                            c2 = n
                    if sec:
                        if (c,sec) in rv:
                            rv[(c,sec)].append(c1)
                        else:
                            rv[(c,sec)] = c1
    #print(rv)
    #print("llllllllllllllllllllllllllllllllll")
    rv2 = {}
    for r in rv:
        if len(rv[r]) == 2:
            rv2[r] = rv[r]
        elif len(rv[r]) == 3:
            rv2[r] = [rv[r][0], rv[r][1]]
            k = (r[1],r[0])
            rv2[k] = rv[r][2]
        else:
            print("ERROR",rv[r])
    rv3 = {}
    for k in rv2.keys():
        c = rv2[k]
        e = k
        rv3[(c[0],c[1])] = e
    return rv2, rv3


def find_se(level, w, h):
    s = None
    e = None
    for i in range(0,h):
        for j in range(0,w):
            if level[j][i] == "@":
                s = (i,j)
            if level[j][i] == "$":
                e = (i,j)
    return (s,e)

def naive(level, start, end):
    pass

def main(lines):
  (lvl, w, h, lvl2) = get_level(lines)
  pm(lvl)
  print(w,h)

  (start,end) = find_se(lvl2, w, h)
  print("S",start)
  print("E",end)
  path = bfs(lvl2, w, h, start, end)
  print(path)
  print("BFS1",len(path)-1)
  pol, poc = find_portals(lvl, w, h)
  #print("###########")
  #print(pol)
  #print(poc)
  print("###########")
  path2 = bfs2(lvl2, w, h, start, end, pol, poc)
  print(path2)
  print("BFS2",len(path2)-1)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    name = "../input/day20/part1"
  else:
    name = sys.argv[1]
  if len(sys.argv) < 3:
    fuel = 1
  else:
    fuel = int(sys.argv[2])
  with open(name, "r") as fh:
    p = fh.readlines()
    p = [p.rstrip() for p in p]
  main(p)
