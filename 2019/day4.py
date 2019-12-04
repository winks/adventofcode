def equalify(n):
    s = str(n)
    for i in range(0, len(s)):
      if i == 0:
        continue
      dthis = int(s[i])
      dlast = int(s[i-1])
      if dthis < dlast:
        s = "{}{}".format(s[0:i], (str(dlast) * len(s[i:])))
        print("  adj",s)
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
      #print("###",s[i], s[i-1], i, s)
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
    #print("\n#i",i,"last",last,"cur",cur,"cnt",cnt,"ok",ok)

    if i == 0:
      last = cur
      continue
    else:
      if cnt == 2:
        if i < len(s)-1 and s[i+1] != cur:
          ok = ok + 1
        elif i == len(s)-1:
          ok = ok +1
        #print("#i",i,"last",last,"cur",cur,"cnt",cnt,"ok",ok)
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
      print("  #", a, lastok)
      r = check1(a)
      if r and a > lastok:
        print("##", a)
        counter = counter + 1
        lastok = a
        a = a + 1
      else:
        a2 = equalify(a)
        if a2 > b:
          break
        #print(a)
        r = check1(a2)
        if r and a2 > lastok:
          #print("###", a2, lastok)
          print("##", a2)
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
      print("  #", a, lastok)
      r = check2(a)
      a2 = equalify(a)
      if a2 > b:
        break
      #print(a)
      r = check2(a2)
      if r and a2 > lastok:
        #print("###", a2, lastok)
        print("##", a2)
        counter = counter + 1
        lastok = a2
      a = a2 + 1
      i = i + 1

    print("max   :", (b0-a0))
    print("i     :", i)
    print("result:", counter)

f1(206938,679128)
f2(206938,679128)
