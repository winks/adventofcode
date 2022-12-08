import sys
import re

fname = sys.argv[1]

with open(fname) as fh:
    lines = fh.readlines()

is_ls = False
root = {
    'name': "/",
    'is_dir': True,
    'size': 0,
    'children': {},
    'parent': None,
}
last = root
for line in lines:
    line = line.strip()

    if line == "$ ls":
        is_ls = True
        #print("LS")
    elif line[0:5] == "$ cd ":
        is_ls = False
        cur = line[5:]
        #print("CD [{}]".format(cur))
        if cur == "/":
            continue
        elif cur == "..":
            last = last['parent']
        else:
            last = last['children'][cur]
    elif is_ls:
        if line[0:4] == "dir ":
            n = line[4:]
            d = {'name': n, 'size': 0, 'is_dir': True, 'children': {}, 'parent': last}
            #print("DIR [{} {}]".format(0, n))
            last['children'][n] = d
        else:
            p = line.split(" ")
            sz = int(p[0])
            n = p[1]
            d = {'name':n, 'size': sz, 'is_dir': False, 'children': {}, 'parent': last}
            #print("FIL [{} {}]".format(sz, n))
            last['children'][n] = d

def count(x):
    sz = 0
    subs = set()
    all = set()
    max = 100000
    for cn in x['children'].keys():
        c = x['children'][cn]
        if c['is_dir']:
            sc, ss, sa = count(c)
            sz += sc
            for s in ss:
                subs.add(s)
                #all.add(s)
            if sc < max:
                subs.add((cn, sc))
            for a in sa:
                all.add(a)
        else:
            st = c['size']
            sz += st
        #print(" XX", cn, subs)
    #print("size {} {}".format(x['name'], sz))
    if sz < max:
        subs.add((x['name'], sz))
    all.add((x['name'], sz))
    return sz, subs, all

s1, s2, s3 = count(root)
#print(s1, s2)
p1 = 0
p2 = 0
for s in s2:
    p1 += s[1]

sp_avail = 70000000
sp_needed = 30000000

sp_used = s1

#print(len(s3), s3)
#print("{} / {} :: {}".format(sp_used, sp_avail, sp_needed))

cand = []
for s in s3:
    if sp_used - s[1] <= (sp_avail - sp_needed):
        cand.append(s[1])
        continue
    #print("  {} - {}\t = {}".format(sp_used, s[1], sp_used - s[1]))
    
#print(cand)
p2 = min(cand)

print("p1: {}".format(p1))
print("p2: {}".format(p2))