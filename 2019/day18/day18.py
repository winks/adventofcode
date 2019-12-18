import collections
import re
import sys
from collections import defaultdict


def pm(lvl):
  for row in lvl:
    print(''.join(row))

def ppkd(d):
  for k in sorted(d.keys()):
    print(k,':',d[k])

def is_out(cell, level):
  [x,y] = cell
  if x < 0 or x >= len(level[0]):
    return True
  if y < 0 or y >= len(level):
    return True
  return False

def is_valid(cell, level):
  [x, y] = cell
  return (not is_out(cell, level)) and level[y][x] != '#'

def neighbors(cell, level):
  rv = []
  [x,y] = cell
  test = [ [x-1,y], [x+1,y], [x,y-1], [x,y+1] ]
  for t in test:
    if is_valid(t, level):
      rv.append(t)
  return rv

def get_sigils(lvl):
  rv = []
  rvd = {}
  rvk = {}
  start = []
  for y, row in enumerate(lvl):
    for x, cell in enumerate(row):
      if cell == '@':
        start = [x,y]
        continue
      if re.match(r'[A-Z]', cell):
        rvd[cell] = [x,y]
        continue
      if re.match(r'[a-z]', cell):
        rvk[cell] = [x,y]
  rv = [rvd, rvk, start]
  return rv

def get_level(lines):
  w = len(lines[0])
  h = len(lines)
  m = []
  m2 = []
  for i in range(0, len(lines)):
    t = []
    for j in range(0, len(lines[i])):
      t.append(lines[i][j])
    m.append(t)
    m2.append(t)
  return (m, w, h, m2)

def get_all_valid(level):
  rv = []
  for y, row in enumerate(level):
    for x, cell in enumerate(row):
      cell = [x,y]
      if is_valid(cell, level):
        rv.append(cell)
  return rv

def bfs(grid, start, end):
    width = len(grid[0])
    height = len(grid)
    start = (start[0], start[1])
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if x == end[0] and y == end[1]:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != '#' and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def naive(level, allkeys, alldoors, start):
  coll_keys = set()
  coll_doors = set()
  steps = -1

  startcell = start
  for k in sorted(allkeys.keys()):
    print("-----------------------")
    print("new target:",k)
    if k.upper() in coll_doors:
      print("already opened door:",k.upper(),"({} s)".format(steps))
      coll_keys.add(k)
      
      continue
    path = bfs(level, startcell, allkeys[k])
    print("  current path:",path)
    rejected_doors = set()
    for p in path:
      cur = level[p[1]][p[0]]
      steps = steps + 1
      print("  current cell:",p,"=",cur)
      if cur in allkeys.keys():
         print("collected key:",cur,"({} s)".format(steps))
         coll_keys.add(cur)
         #p2 = bfs(level, p, )
         startcell = p
         level[p[1]][p[0]] = '.'
         steps = steps - 1
         break
      if cur in alldoors.keys():
        if cur.lower() in allkeys.keys():
          print("opened door:",cur,"({} s)".format(steps))
          coll_doors.add(cur)
          level[p[1]][p[0]] = '.'
        else:
          print("door closed:",cur)
          rejected_doors.add(cur)
          steps = steps - 1
          startcell = p
          break
  print("steps:",steps+1)
  if len(rejected_doors) > 0:
    for rd in rejected_doors:
      print("rejected:",rd)

def main(lines):
  (lvl, w, h, lvl2) = get_level(lines)
  pm(lvl)
  print(w, "x", h)
  (ad,ak,start) = get_sigils(lvl)
  ppkd(ad)
  ppkd(ak)
  print("start", start)
  gv = get_all_valid(lvl)
  print("all_valid",gv)
  #lookup = {}
  #gvx = gv.copy()
  #
  #for k in ak:
  #  aa = bfs(lvl2, start, ak[k])
  #  print(aa)
  #for d in ad:
  #  aa = bfs(lvl2, start, ad[d])
  #  print(aa)
  naive(lvl2, ak, ad, start)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    name = "../input/day18/part1"
  else:
    name = sys.argv[1]
  if len(sys.argv) < 3:
    fuel = 1
  else:
    fuel = int(sys.argv[2])
  with open(name, "r") as fh:
    p = fh.readlines()
  p = [p.strip() for p in p]
  main(p)
