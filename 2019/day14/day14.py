import sys
import pprint

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

def calc3(lookup,bases, fuel):
  r = {}
  prod = {}
  for k in lookup.keys():
    r[k] = 0
    prod[k] = 0
  r['FUEL'] = fuel
  r['ORE'] = 1
  pprint.pprint(r)
  def check(r):
    zero = len(r)
    for k in r.keys():
      if r[k] <= 0:
        zero = zero - 1
    return zero
  i = 0
  print("go",check(r),i)
  lo1 = 0
  lo2 = 0
  lo3 = 0
  while check(r) > 1:
    lo1 = lo1 + 1
    print()
    print("rrr1",r)
    i = i + 1
    for k in r.keys():
      lo2 = lo2 + 1
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
        lo3 = lo3 + 1
        print("  kk",kk,parts[kk][0])
        r[kk] = r[kk] + parts[kk][0]
    print("rrr2",r)
  ###
  r['ORE'] = r['ORE'] - 1
  print("=========")
  print("NEED",r)
  print("PROD",prod)
  print("Part 1:",r['ORE'])
  print(lo1)
  print(lo2)
  print(lo3)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    name = "../input/day14/part1"
  else:
    name = sys.argv[1]
  if len(sys.argv) < 3:
    fuel = 1
  else:
    fuel = int(sys.argv[2])
  with open(name, "r") as fh:
    p = fh.readlines()
  lookup, base1 = f(p)
  bases = list(map((lambda x: x[0]), base1))
  pprint.pprint(lookup)
  print("-----------")
  calc3(lookup, bases, fuel)
