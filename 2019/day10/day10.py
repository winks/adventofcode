import math
import sys

def dist(a,b):
   return math.sqrt( (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) )

def sub(a,b):
    return [a[0] - b[0], a[1] - b[1]]

def angle2(a, b):
  return math.atan2(b[1] - a[1], b[0] - a[0])

def part1(a, pairs):
  lookup = []
  for t in pairs:
    u1 = sub(t[1], a)
    x = angle2([0,0], u1)
    md = math.degrees(x)
    md = round(md,10)
    if not md in lookup:
      lookup.append(md)
  return lookup

def part2(a, pairs):
  lookup = []
  for t in pairs:
    u1 = sub(t[1], a)
    x = angle2(a, t[1])
    md = math.degrees(x)
    md = round(md,10)
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
  print("Part 1:",bs,"::",mx)
  print("")

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
  shot = []
  lang = 0
  print("left:",len(aa),"shot:",len(shot))
  print("")

  def m(x):
    rv = ((x[2] - lang)%360) * 1000 + dist(bs, x)
    return rv

  while aa:
    if len(shot) >= 200:
      break
    tgt = min(aa, key=m)
    print("Target:",tgt,"m:", m(tgt),"a:","l:", lang, dist(bs, tgt))
    shot.append(tgt)
    aa.remove(tgt)
    lang = (tgt[2] + 0.001)%360
    print("left:",len(aa),"shot:",len(shot),"last:",tgt,"lang:",lang)
    print("")

  print("Part 1:",bs,"::",mx)
  print("Part 2:",tgt,"::",(tgt[0]*100+tgt[1]))

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
