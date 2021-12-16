import math
import sys

def h(p1, p2):
    dy = (p1[0] - p2[0])
    dx = (p1[1] - p2[1])
    return abs(math.sqrt(abs((dx*dx) - (dy*dy))))
    #return math.floor(abs(math.sqrt(abs((dx*dx) - (dy*dy)))))

def get_path(pts, p1, p2):
    rv = [p1]
    nxt = p1
    while nxt in pts:
        nxt = pts[nxt]
        rv.insert(0, nxt)
        if p1[:2] == p2[:2]:
            return rv
    return rv

def get_ne(p, pts, my, mx):
    rv = []
    dd = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for d in dd:
        y = p[0]+d[0]
        x = p[1]+d[1]
        if -1 < y < my and -1 < x < mx:
            if my > len(pts):
                v = cave2(y, x, pts)
            else:
                v = pts[y][x]
            rv.append((y, x, v))
    return rv

def pp(cave):
    for c in cave:
        print(c)

def qadd(p, cost, pts):
    if cost not in pts:
        pts[cost] = []
    pts[cost].append(p)
    return pts

def  qget(pts, max_cost):
    for k in range(1, max_cost + 1):
        if k in pts and len(pts[k]) > 0:
            p = pts[k].pop()
            if len(pts[k]) < 1:
                del pts[k]
            return (p, pts)
    return None

def cave2(y, x, cave):
    my = len(cave)
    mx = len(cave[0])
    v = cave[y % my][x % mx] + math.floor(y / my) + math.floor(x / mx)
    if v > 9:
        v -= 9
    return v

def solve(fname, p1 = True):
    f = open(fname, "r").read()
    cave = [[int(c) for c in line] for line in f.split("\n")]
    if len(cave[-1]) < 1:
        cave.pop()

    my = len(cave)
    mx = len(cave[0])
    p_end = (my-1, mx-1,  cave[my-1][mx-1])
    if not p1:
        my = my * 5
        mx = mx * 5
        p_end = (my-1, mx-1,  cave2(my-1, mx-1, cave))
    p_start = (0, 0, cave[0][0])
    #print(p_start, p_end, my, mx)
    max_cost = p_start[2]
    xopen = {max_cost : [p_start]}
    xfrom = {}
    gscore = {p_start : 0}
    #fscore = {p_start : h(p_start, p_end)}

    while len(xopen) > 0:
        (cur, xopen) = qget(xopen, max_cost)
        if cur[:2] == p_end[:2]:
            w = get_path(xfrom, cur, p_start)
            return sum([x[2] for x in w]) - p_start[2]
        ne = get_ne(cur, cave, my, mx)
        for v in ne:
            gs = gscore[cur] + v[2]
            if v not in gscore or gs < gscore[v] :
                xfrom[v] = cur
                gscore[v] = gs
                #fscore[v] = gs + h(v, p_end)
                if v not in xopen:
                    qadd(v, gs, xopen)
                    #qadd(v, fscore[v], xopen)
                    if gs > max_cost:
                        max_cost = gs
                    #if fscore[v] > max_cost:
                    #    max_cost = fscore[v]

print(solve(sys.argv[1]))
print(solve(sys.argv[1], False))