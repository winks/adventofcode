import sys
import re

fname = sys.argv[1]
with open(fname) as fh:
    lines = fh.readlines()
md = {}
mn = {}

for line in lines:
    line = line.strip()
    pa = line.split(": ")
    name = pa[0]
    term = pa[1].split(" ")
    if len(term) < 2:
        v = int(term[0])
        md[name] = {'ok': True, 'num': v}
    else:
        mn[name] = {'ok': False, 'num': 0,
            'op': term[1], 'lo': term[0], 'ro': term[2]}

def resolve(op, le, ri):
    rv = 0
    if op == '+':
        rv = le + ri
    elif op == '-':
        rv = le - ri
    elif op == '*':
        rv = le * ri
    elif op == '/':
        rv = le / ri
    return rv

md20 = {}
mn20 = {}
for m in md.keys():
    md20[m] = md[m]
for m in mn.keys():
    mn20[m] = mn[m]

running = True
while len(mn) > 0 and running:
    kk = [i for i in mn.keys()]
    #print("{}/{} done".format(len(md), len(md)+len(mn)))
    for k in kk:
        v = mn[k]
        le = v['lo']
        ri = v['ro']
        if le in md and ri in md:
            #print("found", le, md[le], ri, md[ri])
            res = resolve(v['op'], md[le]['num'], md[ri]['num'])
            #print(v['op'], md[le]['num'], md[ri]['num'],"=", res)
            if k == 'root':
                print("p1:", int(res))
                running = False
            del mn[k]
            md[k] = {'ok': True, 'num': res}

# as determined by a healthy dose of manual binary searching
# uncomment lines 96+97 and run the loop like range(1000000, 10000000, 1000000)
# this makes bruteforcing viable if you only need to search 100k values
loop_s = 1    if len(md20) < 10 else 3582317956000
loop_e = 1000 if len(md20) < 10 else 3582317957000

for ii in range(loop_s, loop_e):
    if ii % 1000 == 0:
        print("ii:", ii)
    md2 = {}
    mn2 = {}
    for m in md20.keys():
        if m == 'humn':
            v = md20[m]
            v['num'] = ii
            md2[m] = v
        else:
            md2[m] = md20[m]
    for m in mn20.keys():
        mn2[m] = mn20[m]
    #print(len(md2),"/",len(mn2)+len(md2))

    running = True
    ignored = False
    while len(mn2) > 0 and running and not ignored:
        #print(len(md2),"/",len(mn2)+len(md2))
        kk = [i for i in mn2.keys()]
        for k in kk:
            v = mn2[k]
            le = v['lo']
            ri = v['ro']
            #print(k)
            if k == 'humn':
                #print('humn')
                continue
            elif k == 'root':
                if le in md2 and ri in md2:
                    #print("test", md2[le]['num'], md2[ri]['num'], md2[le]['num'] > md2[ri]['num'])
                    #ignored = True                    
                    if int(md2[le]['num']) == int(md2[ri]['num']):
                        print("p2:", ii)
                        sys.exit()
                        running = False
                    elif len(mn2) == 1:
                        ignored = False
            
            if le in md2 and ri in md2:
                res = resolve(v['op'], md2[le]['num'], md2[ri]['num'])
                #print("resolved", k, v['op'], md2[le]['num'], md2[ri]['num'],"=", res)
                md2[k] = {'ok': True, 'num': int(res)}
                del mn2[k]
                #running = False

#print(mn2)
#print("---")
#for m in md2.keys():
#    print(m, md2[m])
#print("---")
#for m in mn2.keys():
#    print(m, mn2[m])
