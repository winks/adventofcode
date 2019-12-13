from itertools import permutations
from itertools import combinations
import math
import sys

def dist(a,b):
   return math.sqrt( (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) )

def rev(a):
    return [0 - a[0], 0 - a[1]]

def add(a,b):
    return [a[0] + b[0], a[1] + b[1]]

def sub(a,b):
    return [a[0] - b[0], a[1] - b[1]]

def scale(v, f=1):
    return [v[0] * f, v[1] * f]

def count(x, pairs):
  y = map(str, x)
  z = set(y)
  return len(pairs) - len(z)

def getvec(x,y,x1,y1):
  a = 0
  b = 0
  if x > x1:
    a = x - x1
  else:
    a = x1 - x
  if y > y1:
    b = y - y1
  else:
    b = y1 - y
  return [a,b]

def crossp(a, b):
   return a[0] * b[1] - b[0] * a[1];

def angle2(a, b):
  return math.atan2(b[1] - a[1], b[0] - a[0])

def uni4(a, pairs):
  lookup = []
  for t in pairs:
    u1 = sub(t[1], a)
    x = angle2([0,0], u1)
    md = math.degrees(x)
    md = round(md,10)
    print(a,t[0],t[1], md)
    if not md in lookup:
      lookup.append(md)
  return lookup

def los(m):
  rv = {}
  for x in range(0, len(m[0])):
    for y in range(0, len(m)):
      if m[y][x] == ".":
        continue
      print("-------------------")
      print("#POINT",x,y)
      ck = []
      for x1 in range(0, len(m[0])):
        for y1 in range(0, len(m)):
          if m[y1][x1] == ".":
            continue
          if x == x1 and y == y1:
            continue
          ck.append([[x,y],[x1,y1]])
      pts = [b for [a,b] in ck]
      pts.insert(0, ck[0][0])
      print("--",len(pts),"points",pts)
      print("--",len(ck),"pairs",ck)
      angles = uni4([x,y], ck)
      print(sorted(angles))
      print("")
      rv[str([x,y])] = len(angles)
  mx = 0
  bs = ''
  for k in rv.keys():
    print(k,":",rv[k])
    if rv[k] > mx:
      bs = k
      mx = rv[k]
  print("")
  print(bs,rv[bs])

if __name__ == "__main__":
  if len(sys.argv) < 2:
    name = "../input/day10/part1"
  else:
    name = sys.argv[1]
  with open(name, "r") as fh:
    lines = fh.readlines()
    am = []
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()
        if not i in am:
            am.append([])
        for c in lines[i]:
            am[i].append(c)
  print(lines, len(lines[0]), "x", len(lines))
  los(am)
