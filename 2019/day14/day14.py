import sys
import pprint
from functools import reduce
import collections
from itertools import permutations

def gettoplevel(lookup):
  return list(lookup['FUEL'].keys())

def f(lines):
  lookup1 = {}
  lookup2 = []
  for line in lines:
    p = line.strip().split(' => ')
    end = p[1].split(' ')
    left = p[0].split(', ')
    if not end[1] in lookup1:
        lookup1[end[1]] = {}
    for ll in left:
      ll = ll.split(' ')
      lookup1[end[1]][ll[1]] = [int(ll[0]), int(end[0])]
    if len(left) == 1:
      left = left[0].split(' ')
      if left[1] == 'ORE':
        lookup2.append([end[1],int(left[0]),int(end[0])])

  return lookup1, lookup2

def hsum(v):
  print(v)
  #m = reduce((lambda x, y: x[0] + y[0]), v)
  #n = reduce((lambda x, y: x[1] + y[1]), v)
  m = 0
  n = 0
  for k in v:
    m = m + k[0]
    n = n + k[1]
  return [m,n]

def fin(v):
  t = 0
  for k in v.keys():
    for vx in v[k]:
      t = t + vx[0]
  return t

def calc(lo, kx=None, num=1, total=None):
  if not total:
    total = {}
  print("-- CALC ----------",kx, num)
  st = lo[kx]
  sub = 0
  if 'ORE' in lo[kx]:
    p = []
    for o in lo[kx]['ORE']:
      p.append(o)
    print("ORE!",p)
    p.insert(0, kx)
    return p, 0
  else:
    #tmp2 = []
    tmp2 = {}
    for k in st.keys():
      print(">",kx,",",k,",",st[k])
      tmp, rv = calc(lo, k, st[k][0], total)
      print("<",kx,",",k,",",st[k],"|",tmp,"#",total)
      print("")
      if rv == 0:
        print("branch",tmp)
        if not tmp[0] in total:
          total[tmp[0]] = []
        #if not tmp[0] in tmp2:
        #  tmp2[tmp[0]] = []
        t = 0
        hs = hsum(total[tmp[0]])
        #hs = hsum(tmp2[tmp[0]])
        print(hs)
        while t < st[k][0] and hs[0] - hs[1] < st[k][0]:
          t = t + tmp[2]
        print(t,st[k])
        if t > 0:
          total[tmp[0]].append([t,st[k][0]])
          #tmp2[tmp[0]].append([t,st[k][0]])
      else:
        print("tto", total)
        print("hm", tmp)
        kkk = None
        for kkk in tmp.keys():
          if not kkk in tmp2:
            tmp2[kkk] = []
          for kkv in tmp[kkk]:
            tmp2[kkk].append(kkv)
        print("hm2", kkk, len(tmp2),tmp2)
      #  tmp[0] = st[k][0]
      #print("<",kx,",",k, st[k],tmp)
      print("<<",kx,",",k, st[k],"|",tmp,"#",total)
      #tmp2.append([[k,st[k]],tmp])
    print("else: tmp2")
    pprint.pprint(tmp2)
    print("TOTAL",total)
    return total, 1

def calc2(lo, lo2, kx=None, num=1, total=None):
  if not total:
    total = {}
  print("-- CALC2 ----------",kx, num)
  found = None
  for e in lookup2:
    if e[0] == kx:
      found = e
  print("f",found)
  st = lo[kx]
  rv = []
  if found:
    return found
  else:
    z = []
    z2 = []
    for k in st.keys():
      print("e:",k,st[k][0])
      n2 = st[k][0]
      y = calc2(lookup, lookup2, k, n2, {})
      if isinstance(y, collections.Mapping) or isinstance(y[0], collections.Mapping):
        rv.append(y)
        continue
      else:
        print("y",y,k,rv)
        sub = 0
        for i in range(0,n2):
          z.append(y)
        ore = 0
        needed = n2
        made = 0
        done = needed
        factor, batch = y[1],y[2]
        print("need",needed,"batch",batch)
        while made < needed:
          print("p",made,needed)
          ore = ore + factor
          made = made + batch
        print("made",made,"of",n2,k,"for",ore,"ore")
        rest = made - n2
        print("rest",rest)
        z2.append({'mat':k,'made':made,'ore':ore,'rest':rest,'top':kx})
    #print("z",kx,num,z)
    print("zz2",kx,num,z2)
    print()
    #for i in range(0, num):
    #  for zz in z:
    #    rv.append(zz)
    if kx == 'FUEL':
      return rv
    return z2

def gettoplevel2(x):
  r = {}
  for e1 in x:
    for e in e1:
      if not e['mat'] in r:
        r[e['mat']] = []
      r[e['mat']].append(e)

  tops = []
  for k in r.keys():
    for k2 in r[k]:
      if k2['top'] not in tops:
        tops.append(k2['top'])

  return lookup['FUEL'].keys()


def fin2(x, lookup, tops):
  r = {}
  for e1 in x:
    for e in e1:
      if not e['mat'] in r:
        r[e['mat']] = []
      r[e['mat']].append(e)

  rv = []
  for k in r.keys():
    print(k, len(r[k]),r[k])
  tu = {
    'ore': 0,
    'rest': {},
    'prod': {}
  }

  for top in tops:
    needed = lookup['FUEL'][top][0]
    print("needed1",top,needed)
    tmp = []
    for k in r.keys():
      for k2 in r[k]:
        if k2['top'] == top:
          for i in range(0, needed):
            tmp.append(k2)
    #x = {
    #  'ore': 0,
    #  'rest': []
    #}
    for t in tmp:
      print("tmp",t)
      mat = t['mat']
      if not mat in tu['rest']:
        tu['rest'][mat] = 0
      if not mat in tu['prod']:
        tu['prod'][mat] = 0
      actual = t['made'] - t['rest']
      if actual <= tu['rest'][mat]:
        tu['rest'][mat] = tu['rest'][mat] - actual
        print("took",actual,"of",mat,"from stock")
        continue
      tu['ore'] = tu['ore'] + t['ore']
      tu['prod'][mat] = tu['prod'][mat] + t['made']
      if t['rest'] > 0:
        for i in range(0,t['rest']):
          tu['rest'][mat] = tu['rest'][mat] + 1
    print("now",top,tu)
    #tu = x
  return tu

def c3(lookup, current_level):
  rv = []
  for k in current_level:
    if k == 'ORE':
      return [0]
    need = list(lookup[k].keys())
    print("-",k,need)
    acc = c3(lookup, need)
    print("got",acc)
    if len(acc) == 1 and acc[0] == 0:
      rate = lookup[k]['ORE']
      xx = [k,rate]
      print(xx)
      rv.append(xx)
      continue
    rv.append(acc)
  return rv

def calc3(lookup,bases,toplevel):
  r = {}
  prod = {}
  for k in lookup.keys():
    r[k] = 0
    prod[k] = 0
  r['FUEL'] = 1
  r['ORE'] = 1
  pprint.pprint(r)
  def check(r):
    zero = len(r)
    for k in r.keys():
      if r[k] <= 0:
        zero = zero - 1
    return zero
  #a = c3(lookup,toplevel)
  i = 0
  print("go",check(r),i)
  while check(r) > 1 or i < 1000:
    print()
    print("rrr1",r)
    i = i + 1
    for k in r.keys():
      if r[k] <= 0 or k == 'ORE':
        continue
      if k in bases:
        costs = lookup[k]['ORE']
        # check 1 or 0
        if r[k] >= costs[1]:
          print("  now2",k,costs)
          r[k] = r[k] - costs[1]
          prod[k] = prod[k] + costs[1]
          r['ORE'] = r['ORE'] + costs[0]
          continue
        #nib =0
        #for k in r.keys():
        #  if r[k] > 0:
        #    if not k in bases:
        #      nib = nib + 1
        #if nib > 0:
        #  continue
      parts = lookup[k]
      # check
      tmpkeys = list(parts.keys())
      costs = lookup[k][tmpkeys[0]][1]
      print("  now1",parts)
      print(" ",k, costs)
      r[k] = r[k] - costs
      prod[k] = prod[k] + costs
      for kk in tmpkeys:
        print("  kk",kk,parts[kk][0])
        r[kk] = r[kk] + parts[kk][0]
    print("rrr2",r)
  print("NEED",r)
  print("PROD",prod)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    name = "../input/day14/part1"
  else:
    name = sys.argv[1]
  with open(name, "r") as fh:
    p = fh.readlines()
  lookup, base1 = f(p)
  toplevel = gettoplevel(lookup)
  bases = list(map((lambda x: x[0]), base1))
  pprint.pprint(lookup)
  #pprint.pprint(bases)
  #print("tops",toplevel)
  #print("base",bases)
  print("-----------")
  #x,y = calc2(lookup, lookup2, 'FUEL', 1)
  #x = calc2(lookup, lookup2, 'FUEL', 1)
  x = calc3(lookup, bases, toplevel)
  print("-----------")
  #pprint.pprint(x)
  #print(fin(x))
  #print("-----------")
  #print("tops",tops)
  #print("============")
  #print("XXX",fin2(x, lookup, tops))
  #t2 = permutations(tops)
  #for perm in t2:
  #  print("XXX",perm)
  #  print("XXX",fin2(x, lookup, perm))

