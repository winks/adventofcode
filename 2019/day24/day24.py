import math
import sys


def bio(m):
  p = 0
  rv = 0
  for y in range(0, len(m)):
    for x in range(0, len(m[0])):
      if m[y][x] == '#':
        rv = rv + math.pow(2, p)
      p = p + 1
  return rv

def pp(m):
  for y in range(0, len(m)):
    for x in range(0, len(m[0])):
      print(m[y][x], end='')
    print()

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
    #print("_",x,y," ",x1,y1," ",c)
  return c

def tick(m):
  m2 = []
  for y in range(0, len(m)):
    m2.append([1,1,1,1,1])
  for y in range(0, len(m)):
    for x in range(0, len(m[0])):
      t = (x,y)
      c = m[y][x]
      n = getnec(t, m)
      #print(x,y," ",c,n)
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
    #print("eol")
  return m2

def part1(m):
  print("- start:")
  rx = [m]
  pp(m)
  i = 0
  while True:
    m = tick(m)
    if m in rx:
      print(i)
      pp(m)
      print(round(bio(m)))
      break
    rx.append(m)
    i = i + 1
    #print("--- 1")
  #pp(m)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    name = "../input/day24/part1"
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
  part1(am)
