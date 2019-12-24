import math
import sys
from copy import deepcopy


def pp(m):
  for y in range(0, len(m)):
    for x in range(0, len(m[0])):
      print(m[y][x], end='')
    print()

def pp2(mm):
  for lv in sorted(mm.keys()):
    print("=== Level",lv)
    for y in range(0, len(mm[0])):
      for x in range(0, len(mm[0][0])):
        print(mm[lv][y][x], end='')
      print()

def nm():
  m0 = []
  for y in range(0, 5):
    m0.append(['.','.','.','.','.',])
  return m0

def bio(m):
  p = 0
  rv = 0
  for y in range(0, len(m)):
    for x in range(0, len(m[0])):
      if m[y][x] == '#':
        rv = rv + math.pow(2, p)
      p = p + 1
  return rv

def getnec(t, m):
  sz = len(m)
  c = 0
  (x,y) = t
  for (x1,y1) in [(x,y-1), (x+1,y), (x,y+1), (x-1,y)]:
    if x1 < 0 or x1 >= sz:
      continue
    if y1 < 0 or y1 >= sz:
      continue
    if m[y1][x1] == '#':
      c = c + 1
  return c

def tick(m):
  m2 = nm()
  for y in range(0, len(m)):
    for x in range(0, len(m[0])):
      t = (x,y)
      c = m[y][x]
      n = getnec(t, m)
      if c == '#':
        if n != 1:
          m2[y][x] = '.'
        else:
          m2[y][x] = m[y][x]
      elif c == '.':
        if 1 <= n <= 2:
          m2[y][x] = '#'
        else:
          m2[y][x] = m[y][x]
  return m2

def bio2(mm):
  c = 0
  for k in mm:
    for y in mm[k]:
      for x in y:
        if x == '#':
          c = c + 1
  return c

def getnec2(t, mm, lv):
  sz = len(mm[lv])
  c = 0
  (x,y) = t
  for (x1,y1) in [(x,y-1), (x+1,y), (x,y+1), (x-1,y)]:
    if x1 < 0 or x1 >= sz:
      ko = lv - 1
      #print("zoom out to",ko," ",x,y,"  ",x1,y1," ",c)
      if x1 < 0:
        idx = 1
      else:
        idx = 3
      if mm[ko][2][idx] == '#':
        c = c + 1
      #print("zoom in        ",x,y,"  ",x1,y1," ",c)
    elif y1 < 0 or y1 >= sz:
      ko = lv - 1
      #print("zoom out to",ko," ",x,y,"  ",x1,y1," ",c)
      if y1 < 0:
        idx = 1
      else:
        idx = 3
      if mm[ko][idx][2] == '#':
        c = c + 1
      #print("zoom in        ",x,y,"  ",x1,y1," ",c)
    elif x1 == 2 and y1 == 2:
      #print("Zoom in  to",lv+1," ",x,y,"  ",x1,y1," ",c)
      if x == 1:
        rx = 0
      elif x == 3:
        rx = 4
      if x == 1 or x == 3:
        for i in range(0,5):
          if mm[lv+1][i][rx] == '#':
            c = c + 1
      if y == 1:
        ry = 0
      elif y == 3:
        ry = 4
      if y == 1 or y == 3:
        for i in range(0,5):
          if mm[lv+1][ry][i] == '#':
            c = c + 1
      #print("Zoom out       ",x,y,"  ",x1,y1," ",c)
    else:
      if mm[lv][y1][x1] == '#':
        c = c + 1
  return c

def tick2(mm, num):
  for i in range(0, num+3):
    if not i in mm:
      mm[i] = nm()
    if not -i in mm:
      mm[-i] = nm()
  mm2 = deepcopy(mm)
  both = range(-1-num,num+2)
  for i in both:
    m2 = nm()
    for y in range(0, len(mm[0])):
      for x in range(0, len(mm[0][0])):
        t = (x,y)
        c = mm[i][y][x]
        n = getnec2(t, mm, i)
        if c == '#':
          if n != 1:
            m2[y][x] = '.'
          else:
            m2[y][x] = mm[i][y][x]
        elif c == '.':
          if 1 <= n <= 2:
            m2[y][x] = '#'
          else:
            m2[y][x] = mm[i][y][x]
    mm2[i] = m2
    mm2[i][2][2] = '?'
  return mm2

def part2(m, ticks):
  print("=== Part 2")
  # -1 = outer
  #  1 = inner
  m[2][2] = '?'
  pp(m)
  mm = {0: m}
  i = 0
  while i < ticks:
    mm = tick2(mm, i)
    pp2(mm)
    i = i + 1
  return bio2(mm)

def part1(m):
  print("=== Part 1")
  rx = [m]
  pp(m)
  i = 0
  while True:
    m = tick(m)
    if m in rx:
      #pp(m)
      return round(bio(m))
    rx.append(m)
    i = i + 1

if __name__ == "__main__":
  if len(sys.argv) < 2:
    name = "../input/day24/part1"
  else:
    name = sys.argv[1]
  ticks = 10
  if len(sys.argv) > 2:
    ticks = int(sys.argv[2])
  with open(name, "r") as fh:
    lines = fh.readlines()
    am = []
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()
        if not i in am:
            am.append([])
        for c in lines[i]:
            am[i].append(c)
  p1 = part1(am)
  p2 = part2(am, ticks)
  print("Part 1",p1)
  print("Part 2",p2)
