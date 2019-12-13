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

def part1(a, pairs):
  lookup = []
  for t in pairs:
    u1 = sub(t[1], a)
    x = angle2([0,0], u1)
    md = math.degrees(x)
    md = round(md,10)
    #print(a,t[0],t[1], md)
    if not md in lookup:
      lookup.append(md)
  return lookup

def part2(a, pairs):
  lookup = []
  for t in pairs:
    u1 = sub(t[1], a)
    x = angle2([0,0], u1)
    x = angle2(a, t[1])
    md = math.degrees(x)
    md = round(md,10)
    #print(a,t[0],t[1], md)
    lookup.append([t[1][0],t[1][1],md])
  return lookup

def los(m):
  rv = []
  for x in range(0, len(m[0])):
    for y in range(0, len(m)):
      if m[y][x] == ".":
        continue
      #print("-------------------")
      #print("#POINT",x,y)
      ck = []
      for x1 in range(0, len(m[0])):
        for y1 in range(0, len(m)):
          if m[y1][x1] == ".":
            continue
          if x == x1 and y == y1:
            continue
          ck.append([[x,y],[x1,y1]])
      angles = part1([x,y], ck)
      #print(sorted(angles))
      #print("")
      rv.append([x,y,len(angles)])
  mx = 0
  bs = ''
  for r in rv:
    #print("[",r[0],",",r[1],"]:",r[2])
    if r[2] > mx:
      bs = r[:2]
      mx = r[2]
  print("")
  print("best",bs,mx)

  #part2
  ck = []
  for x1 in range(0, len(m[0])):
    for y1 in range(0, len(m)):
      if m[y1][x1] == ".":
        continue
      if x == x1 and y == y1:
        continue
      ck.append([[x,y],[x1,y1]])
  aa = part2(bs, ck)
  for i in range(0, len(aa)):
     aa[i] = [aa[i][0],aa[i][1],(aa[i][2]+90+360)%360]
  for a in aa:
    print(a, (a[2] * 10000 + dist(bs,a)))
  print("-----")
  shot = []
  lang = 0
  print("aa:",len(aa),"shot:",len(shot))
  print("-----")

  while aa:
    def m(x):
      return ((x[2] - lang)%360) * 100000 + dist(bs, x)
    tgt = min(aa, key=m)
    print(tgt, m(tgt))
    shot.append(tgt)
    aa.remove(tgt)
    lang = (tgt[2] + 0.001)%360
    print("aa:",len(aa),"shot:",len(shot),"last:",tgt,"lang:",lang)
    print("")

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
