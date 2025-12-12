import math
import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

pts = []

def dist(a, b):
    #return math.sqrt(pow(a[0]-b[0],2)+pow(a[1]-b[1],2)+pow(a[2]-b[2],2))
    return pow(a[0]-b[0],2)+pow(a[1]-b[1],2)+pow(a[2]-b[2],2)

for line in lines:
    sp = line.split(',')
    p = list(map(lambda x: int(x), sp))
    pts.append(tuple(p))
#print(pts)


mx = 1000
if part1:
    if len(lines) < 30:
        mx = 10
else:
    mx = 499500
    if len(lines) < 30:
        mx = 190

rv1 = 1
dd = {}
conn = []
for p1 in pts:
    for p2 in pts:
        if p1 == p2:
            continue
        d = dist(p1, p2)
        if d not in dd:
            dd[d] = []
        if [p2, p1] not in dd[d]:
            dd[d].append([p1, p2])

di = 0
for d in sorted(dd.keys())[0:mx]:
    di += 1
    if di % 10 == 0:
        print(f"# {di}")
    #print(d, dd[d])
    if len(conn) == 0:
        p = set()
        for x in dd[d]:
            for y in x:
                #print(y)
                p.add(tuple(y))
        conn.append(p)
        #print("CC", conn)
        continue

    xx = dd[d]
    for x2 in xx:
        for xy in xx:
            y1 = tuple(xy[0])
            y2 = tuple(xy[1])
            f = False

            for c in range(0, len(conn)):
                #print("  ", c, conn[c], y1,y2)
                if y1 in conn[c]:
                    if y2 not in conn[c]:
                        conn[c].add(y2)
                        f = True
                        break
                    else:
                        f = True
                elif y2 in conn[c]:
                    if y1 not in conn[c]:
                        conn[c].add(y1)
                        f = True
                        break
                    else:
                        f = True
                #print("  ", c, conn[c], y1,y2, f)
            if not f:
                p = set()
                p.add(y1)
                p.add(y2)
                conn.append(p)
            else:
                #print("D")
                pass
                #i += 1
                #j -= 1
    cnew = []
    cx = sorted(conn, key=lambda x: len(x))
    #print("cx", cx)
    for c1 in cx:
        ff = False
        for c2 in cx:
            if c1 == c2:
                continue
            if len(c1 | c2) < (len(c1) + len(c2)):
                c3 = c2 | c1
                c4 = c2 & c1
                if c3 not in cnew:
                    #print("M",c4)
                    cnew.append(c3)
                ff = True
                break
        if not ff and c1 not in cnew:
            cnew.append(c1)
        #print("x",cnew)
    conn = cnew
    #if di % 10 == 0:
    #    print(f"## {len(cnew)}")
    if not part1 and len(cnew) == 1 and len(cnew[0]) == len(lines):
        print("P2", dd[d][0][0][0] * dd[d][0][1][0])
        sys.exit()
        break
r1 = list(map(lambda x: len(x), conn))
r2 = sorted(r1)
print(len(r2), r2)
for r in r2[-3:]:
    rv1 = rv1 * r
print(rv1)
