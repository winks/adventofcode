import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def pp(maze):
    for y in range(0, len(maze)):
        print(''.join(maze[y]))

maze = []
m_x = 0
m_y = 0
pts = []
for line in lines:
    p = line.split(',')
    (x,y) = list(map(lambda x: int(x), p))
    m_x = max(x, m_x)
    m_y = max(y, m_y)
    pts.append((x, y))
print(f"# points: {len(pts)}")

def cp(maze):
    m = []
    for y in range(0, len(maze)):
        t = []
        for x in range(0, len(maze[0])):
            t.append(maze[y][x])
        m.append(t)
    return m

def cx(ps):
    xs = list(map(lambda a: a[0], ps))
    ys = list(map(lambda a: a[1], ps))
    mi_x = min(xs)
    ma_x = max(xs)
    mi_y = min(ys)
    ma_y = max(ys)
    return [mi_x, ma_x, mi_y, ma_y]

def ck(mi_x, ma_x, mi_y, ma_y, v_h, v_v):
    for v in v_v:
        if mi_x < v[0][0] and v[0][0] < ma_x:
            lo = min(v[0][1], v[1][1])
            hi = max(v[0][1], v[1][1])
            if max(lo, mi_y) < min(hi, ma_y):
                return True
    for v in v_h:
        if mi_y < v[0][1] and v[0][1] < ma_y:
            lo = min(v[0][0], v[1][0])
            hi = max(v[0][0], v[1][0])
            if max(lo, mi_x) < min(hi, ma_x):
                return True
    return False

if part1:
    mx = 0
    for p1 in pts:
        for p2 in pts:
            if p1 == p2:
                continue
            a = abs(p1[0]-p2[0])+1
            b = abs(p1[1]-p2[1])+1
            d = a * b
            if d > mx:
                #print(d)
                mx = d
    print(mx)
else:
    pg = []
    pl = None
    pts2 = pts + [pts[0]]
    for pi in range(0, len(pts2)):
        pc = pts2[pi]
        if pi == 0:
            pl = pc
            continue
        if pc[0] == pl[0]:
            if pc[1] > pl[1]:
                for i in range(pl[1]+1, pc[1]):
                    pg.append((pc[0], i))
            else:
                for i in range(pc[1]+1, pl[1]):
                    pg.append((pc[0], i))
        elif pc[1] == pl[1]:
            if pc[0] > pl[0]:
                for i in range(pl[0]+1, pc[0]):
                    pg.append((i, pc[1]))
            else:
                for i in range(pc[0]+1, pl[0]):
                    pg.append((i, pc[1]))
        pl = pc
    print(f"# edge points: {len(pg)}")
    if len(lines) < 20:
        for y in range(0, m_y+2):
            row = []
            for x in range(0, m_x+2):
                if (x,y) in pts:
                    row.append('#')
                elif (x,y) in pg:
                    row.append('X')
                else:
                    row.append('.')
            maze.append(row)
        pp(maze)
    mx = 0
    pta = pts + pg
    print(f"# outline: {len(pta)}")

    la = pts2[0]
    out_h = []
    out_v = []
    for p1 in pts2:
        if p1 == la:
            continue
        #line = draw(p1, la)
        if p1[0] == la[0]:
            out_v.append((p1, la))
        else:
            out_h.append((p1, la))
        la = p1
    #print(len(outer),outer)
    print(f"outer_h: {len(out_h)}")
    print(f"outer_v: {len(out_v)}")
    i = 0
    for p1p in range(0, len(pts)):
        for p2p in range(p1p, len(pts)):
            p1 = pts[p1p]
            p2 = pts[p2p]
            if p1 == p2:
                continue
            a = abs(p1[0]-p2[0])+1
            b = abs(p1[1]-p2[1])+1
            d = a * b
            if d < mx:
                continue
            cxx = cx([p1, p2])
            if ck(cxx[0], cxx[1], cxx[2], cxx[3], out_h, out_v):
                continue
            mx = d
            #print("d ",d)
    print(mx)

