import sys

def parse(lines):
  #print(lines)
  parsed = []
  for line in lines:
    line = line.strip()
    if len(line) < 3:
      continue
    p = line.split(")")
    #print(p)
    parsed.append(p)
  return parsed

def sortit(px,par):
  rv = []
  def isleaf(k, par):
    for v in par.keys():
      if par[v] == k:
        #print("#IL", k,v)
        return False
    return True

  def walk(chl, par, acc=None):
    if chl == "COM":
      acc.insert(0, chl)
      return acc
    acc.insert(0, chl)
    return walk(par[chl], par, acc)

  for chl in par.keys():
    pnt = par[chl]
    il = isleaf(chl, par)
    #print("#now",chl,pnt, il)
    if not il:
      continue
    x = walk(chl, par, [])
    #print("#now2",x)
    rv.append(x)
  return rv

def cnt(lst, c=0):
  done = []
  for a in lst:
    for i in range(0, len(a)):
      if a[i] in done:
        continue
      else:
       c = c + i
       done.append(a[i])
    #print("## cnt",a," ",c)
  return c

def revmap(pa):
  rv = {}
  for p in pa:
    if p[1] not in rv:
      rv[p[1]] = p[0]
  return rv

def filtr(ll):
  rv = []
  for l in ll:
    if 'YOU' in l or 'SAN' in l:
      rv.append(l)
  return rv

def cmp(a1, a2):
  tmp = a2.copy()
  cm = []
  for a in a1:
    if tmp[0] == a:
      x = tmp.pop(0)
      cm.append(x)
  result = (len(a1) + len(a2) - len(cm) -len(cm) -2)
  return result

def main():
  if len(sys.argv) < 2:
    sys.exit(1)
  name = sys.argv[1]
  parsed = []
  with open(name, "r") as fh:
    lines = fh.readlines()
    parsed = parse(lines)
  #print(parsed)
  #print("")
  lookup = revmap(parsed)
  s = sortit(parsed, lookup)
  #print("paths:", s)
  #print("num_paths:", len(s))
  #print("")
  print("Part 1: Orbits:", cnt(s))
  x = filtr(s)
  if len(x) == 2:
    y = cmp(x[0],x[1])
    print("Part 1: Hops  :", y)

if __name__ == '__main__':
  main()
