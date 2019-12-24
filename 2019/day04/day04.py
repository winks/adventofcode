import sys

def equalify(n):
    s = str(n)
    for i in range(0, len(s)):
      if i == 0:
        continue
      dthis = int(s[i])
      dlast = int(s[i-1])
      if dthis < dlast:
        s = "{}{}".format(s[0:i], (str(dlast) * len(s[i:])))
        return int(s)
    return int(s)

def check1(n):
  if n < 100000:
    return False
  if n > 999999:
    return False
  s = str(n)
  ok = 0
  for i in range(0, len(s)):
    if i == 0:
      continue
    if s[i] < s[i-1]:
      return False
    if s[i] == s[i-1]:
      ok = ok + 1
  if ok > 0:
    return True
  return False

def check2(n):
  if n < 100000:
    return False
  if n > 999999:
    return False
  s = str(n)
  ok = 0
  last = ' '
  cnt = 1
  for i in range(0, len(s)):
    cur = s[i]

    if cur == last:
      cnt = cnt + 1
    else:
      cnt = 1

    if i == 0:
      last = cur
      continue
    else:
      if cnt == 2:
        if i < len(s)-1 and s[i+1] != cur:
          ok = ok + 1
        elif i == len(s)-1:
          ok = ok +1
        last = cur
        continue
      else:
        last = cur
        continue
    if i == len(s)-1:
      return ok > 0 and cnt <= 2

  if ok > 0:
    return True
  return False

def f1(a, b):
    a0 = a
    b0 = b
    i = 0
    counter = 0
    lastok = 0
    while (a <= b):
      r = check1(a)
      if r and a > lastok:
        counter = counter + 1
        lastok = a
        a = a + 1
      else:
        a2 = equalify(a)
        if a2 > b:
          break
        r = check1(a2)
        if r and a2 > lastok:
          counter = counter + 1
          lastok = a2
        a = a2 + 1
      i = i + 1

    print("max   :", (b0-a0))
    print("i     :", i)
    print("result:", counter)

def f2(a, b):
    a0 = a
    b0 = b
    i = 0
    counter = 0
    lastok = 0
    while (a <= b):
      a2 = equalify(a)
      if a2 > b:
        break
      r = check2(a2)
      if r and a2 > lastok:
        counter = counter + 1
        lastok = a2
      a = a2 + 1
      i = i + 1

    print("max   :", (b0-a0))
    print("i     :", i)
    print("result:", counter)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    name = "../input/day04/part1"
  else:
    name = sys.argv[1]
  with open(name, "r") as fh:
    p = fh.readlines()[0].strip().split("-")

  f1(int(p[0]), int(p[1]))
  f2(int(p[0]), int(p[1]))
