import collections
import re
import sys
from collections import defaultdict
from pprint import pprint

def pm(lvl):
    for row in lvl:
        print(''.join(row))

def get_level(lines):
    w = 0
    h = len(lines)
    for i in range(0, len(lines)):
        if len(lines[i]) > w:
            w = len(lines[i])
    m = []
    m2 = []
    for i in range(0, w):
        t = []
        for j in range(0, h):
            mw = len(lines[i])
            if (j >= mw and mw < w):
                t.append("_")
            else:
                t.append(lines[i][j])
        m.append(t)
        m2.append(t)
    return (m, w, h, m2)

def neighbors(cell, level):
    rv = []
    [x,y] = cell
    test = [ [x-1,y], [x+1,y], [x,y-1], [x,y+1] ]
    for t in test:
        rv.append(t)
    return rv

def find_portals(level, w, h):
    rv = {}
    def m(s):
        return re.match(r"[A-Z]", s)
    for x in range(1, w-1):
        for y in range(1,h-1):
            c = level[x][y]
            ne = neighbors((x,y), level)
            if m(c):
                found = False
                c1 = None
                
                for n in ne:
                    if level[n[0]][n[1]] == '.':
                        found = True
                        c1 = n
                if found:
                    sec = None
                    c2 = None
                    for n in ne:
                        if m(level[n[0]][n[1]]):
                            sec = level[n[0]][n[1]]
                            c2 = n
                    if sec:
                        if (c,sec) in rv:
                            rv[(c,sec)].append(c1)
                        else:
                            rv[(c,sec)] = c1
    #print(rv)
    #print("llllllllllllllllllllllllllllllllll")
    rv2 = {}
    for r in rv:
        if len(rv[r]) == 2:
            rv2[r] = rv[r]
        elif len(rv[r]) == 3:
            rv2[r] = [rv[r][0], rv[r][1]]
            k = (r[1],r[0])
            rv2[k] = rv[r][2]
        else:
            print("ERROR",rv[r])
    rv3 = {}
    for k in rv2.keys():
        c = rv2[k]
        e = k
        rv3[(c[0],c[1])] = e
    return rv2, rv3

def is_inner(grid,w,h,x,y):
    if x < 3 or y < 3:
        return False
    if x + 3 > w or y + 3 > h:
        return False
    if x > 33 or y > 40:
        return False
    return True

def find_portals3(level0, w, h, layer, level1x):
    rv = {}
    if layer == 0:
        level = level0
    else:
        level = level1x
    def m(s):
        return re.match(r"[A-Z]", s)
    for x in range(1, w-1):
        for y in range(1,h-1):
            c = level[x][y]
            ne = neighbors((x,y), level)

            if m(c):
                found = False
                c1 = None
                
                for n in ne:
                    if level[n[0]][n[1]] == '.':
                        found = True
                        if is_inner(level, w, h, n[0], n[1]):
                            if layer == 0:
                                lx = 1
                            else:
                                lx = layer +1
                            c1 = [n[0],n[1],layer+1]
                        else:
                            c1 = [n[0],n[1],layer-1]
                if found:
                    sec = None
                    c2 = None
                    for n in ne:
                        if m(level[n[0]][n[1]]):
                            sec = level[n[0]][n[1]]
                            c2 = (n[0],n[1],layer)
                    if sec:
                        if (c,sec,layer) in rv:
                            #print(rv[(c,sec,layer)])
                            #print(c1)
                            rv[(c,sec, layer)].append(c1)
                        else:
                            rv[(c,sec, layer)] = c1
    #pprint(rv)
    #print("llllllllllllllllllllllllllllllllll")
    if layer == 0:
        rv3 = {}
        for k in rv.keys():
            c = rv[k]
            e = k
            rv3[(c[0],c[1],layer+1)] = e
        #pprint(rv3)
        rv1 = {}
        for k in rv.keys():
            rv1[(k[1],k[0],k[2])] = rv[k]
        #pprint(rv1)
        #for k in rv1:
        #    rv[k] = rv1[k]
        return rv, rv3
    rv2 = {}
    for r in rv:
        if len(rv[r]) == 3:
            rv2[r] = rv[r]
        elif len(rv[r]) == 4:
            rv2[r] = [rv[r][0], rv[r][1], rv[r][2]]
            k = (r[1],r[0], layer)
            rv2[k] = rv[r][3]
        else:
            print("ERROR",rv[r])
    rv3 = {}
    #pprint(rv2)
    for k in rv2.keys():
        c = rv2[k]
        e = k
        rv3[(c[0],c[1],layer)] = e
    return rv2, rv3

def bfs(grid, width, height, start, end):
    start = (start[0], start[1])
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if x == end[0] and y == end[1]:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != '#' and grid[y2][x2] != "B" and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def bfs2(grid, width, height, start, end, polookup, pocoords):
    start = (start[0], start[1])
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if x == end[0] and y == end[1]:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            seen2 = set()
            cell = grid[y2][x2]
            if 0 <= x2 < width and 0 <= y2 < height and cell != '#' and not re.match(r"[A-Z]", cell) and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                #print("XX", x2,y2)
                seen2.add((x2, y2))
            poc = (y2, x2)
            if poc in pocoords:
                pol = pocoords[poc]
                #print("Found portal",poc,"=",pol)
                #print("P",path)
                #print("S1",seen)
                #print("S2",seen2)
                #print("Q",queue)
                #print("===")
                if cell == pol[0]:
                    other_end = polookup[pol]
                else:
                    other_end = polookup[(pol[1],pol[0])]
                #print("TO", other_end)
                nn = path + [(other_end[1], other_end[0])]
                nn.insert(0, (0,0))
                #print("NN",nn)
                queue.append(nn)
                seen2.add((x2, y2))
            for s in seen2:
                seen.add(s)

def bfs3(grid0, grid1, width, height, start, end, numlayers=10):
    polookup = []
    pocoords = []
    (polookup0, pocoords0) = find_portals3(grid0, width, height, 0, grid1)
    pprint(polookup0)
    pprint(pocoords0)
    polookup.append(polookup0)
    pocoords.append(pocoords0)
    print("#######EOF 0")
    
    for i in range(1,numlayers+1):
        (polookup1, pocoords1) = find_portals3(grid0, width, height, i, grid1)
        pprint(polookup1)
        pprint(pocoords1)
        polookup.append(polookup1)
        pocoords.append(pocoords1)
        #pprint(polookup[1])
        #pprint(pocoords[1])
        print("#######EOF",i)

    start = (start[0], start[1], 0)
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        print("P",path)
        x, y, z = path[-1]
        if x == end[0] and y == end[1] and z == 0:
            return path
        for x2, y2, z2 in ((x+1,y,z), (x-1,y,z), (x,y+1,z), (x,y-1,z)):
            #seen2 = set()
            #print("XXX",y2,x2)
            if 0 <= x2 < width and 0 <= y2 < height:
                cell = grid0[y2][x2]
                if cell != '#' and not re.match(r"[A-Z]", cell) and (x2, y2, z2) not in seen:
                    queue.append(path + [(x2, y2, z2)])
                    #print("XX", x2,y2)
                    seen.add((x2, y2, z2))
            #poc = (y2, x2, z2)
            #if poc in pocoords[z2]:
            #    pol = pocoords[z2][poc]
            #    print("Found portal",z2,poc,"=",pol)
            #    #print("P",path)
            #    #print("S1",seen)
            #    #print("S2",seen2)
            #    #print("Q",queue)
            #    #print("===")
            #    if cell == pol[0]:
            #        other_end = polookup[z2][pol]
            #    else:
            #        try:
            #            other_end = polookup[z2][(pol[1],pol[0],z2)]
            #        except KeyError:
            #            other_end = polookup[z2][(pol[0],pol[1],z2)]
            #    print("TO", other_end)
            #    nn = path + [(other_end[1], other_end[0], z2)]
            #    nn.insert(0, (0,0,0))
            #    
            #    #print("NN",nn)
            #    queue.append(nn)
            #    
            #    seen2.add((x2, y2, z2))
            #    #seen2.add((x2, y2, z2+1))
            pocdown = (y2, x2, z2-1)
            if z2-1 >=0 and pocdown in pocoords[z2-1]:
                pol = pocoords[z2-1][pocdown]
                print("Found portal",z2,">",z2-1,pocdown,"=",pol)
                #if cell == pol[0]:
                #    other_end = polookup[z2][pol]
                #else:
                #    other_end = polookup[z2][(pol[1],pol[0],z2)]
                other_end = polookup[z2][(pol[1],pol[0],z2)]
                other_end[2] = z2-1
                print("TO", other_end)
                nn2 = path + [(other_end[1], other_end[0], z2-1)]
                #nn2.insert(0, (0, 0, 0))
                queue.append(nn2)
            pocup = (y2, x2, z2+1)
            #print("POCUP",pocup)
            if z2+1 <= numlayers and pocup in pocoords[z2+1]:
                pol = pocoords[z2+1][pocup]
                print("Found portal",z2,">",z2+1,pocup,"=",pol)
                # pocup  28 17 2
                # pol X F 2
                # want 21 2 2
                other_end = polookup[z2][(pol[1],pol[0],z2)]
                #if cell == pol[0]:
                #    other_end = polookup[z2][pol]
                #else:
                #    other_end = polookup[z2][(pol[1],pol[0],z2)]
                other_end[2] = z2+1
                print("TO", other_end)
                nn2 = path + [(other_end[1], other_end[0], z2+1)]
                #nn2.insert(0, (0, 0, 0))
                queue.append(nn2)
            
            #for s in seen2:
            #    seen.add(s)

    #return
    #    for x2, y2, z2 in ((x+1,y,z+1), (x-1,y,z+1), (x,y+1,z+1), (x,y-1,z+1)):
    #        if z2 > 1:
    #            continue
    #        if z2 < 1:
    #            continue
    #        seen2 = set()
    #        cell = grid1[y2][x2]
    #        if 0 <= x2 < width and 0 <= y2 < height and cell != '#' and not re.match(r"[A-Z]", cell) and (x2, y2, z2) not in seen:
    #            queue.append(path + [(x2, y2, z2)])
    #            #print("XX", x2,y2)
    #            seen2.add((x2, y2, z2))
    #        if poc in pocoords[z2]:
    #            pol = pocoords[z2][poc]
    #            #print("Found portal",poc,"=",pol)
    #            #print("P",path)
    #            #print("S1",seen)
    #            #print("S2",seen2)
    #            #print("Q",queue)
    #            #print("===")
    #            if cell == pol[0]:
    #                other_end = polookup[z2][pol]
    #            else:
    #                try:
    #                    other_end = polookup[z2][(pol[1],pol[0],z2)]
    #                except KeyError:
    #                    other_end = polookup[z2][(pol[0],pol[1],z2)]
    #            #print("TO", other_end)
    #            nn = path + [(other_end[1], other_end[0]), z2]
    #            nn.insert(0, (0,0,0))
    #            #print("NN",nn)
    #            queue.append(nn)
    #            seen2.add((x2, y2, z2))
    #        for s in seen2:
    #            seen.add(s)




def find_se(level, w, h):
    s = None
    e = None
    for i in range(0,h):
        for j in range(0,w):
            if level[j][i] == "@":
                s = (i,j)
            if level[j][i] == "$":
                e = (i,j)
    return (s,e)

def naive(level, start, end):
    pass

def main(lines, lines2):
  (lvl, w, h, lvl2) = get_level(lines)
  pm(lvl)
  print(w,h)

  (start,end) = find_se(lvl2, w, h)
  print("S",start)
  print("E",end)
  path = bfs(lvl2, w, h, start, end)
  print(path)
  print("BFS1",len(path)-1)
  pol, poc = find_portals(lvl, w, h)
  #print("###########")
  #print(pol)
  #print(poc)
  print("###########")
  path2 = bfs2(lvl2, w, h, start, end, pol, poc)
  print(path2)
  print("BFS2",len(path2)-1)

def main2(lines, lines2):
    (_, w, h, lvl0) = get_level(lines)
    (_, _, _, lvl1) = get_level(lines2)
    (start,end) = find_se(lvl0, w, h)
    print("S",start)
    print("E",end)
    print("wh",w,h)
    path = bfs3(lvl0, lvl1, w, h, start, end)
    print(path)
    print("BFS3",len(path)-1)


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: {} /path/to/file".format(sys.argv[0]))
    sys.exit()
  else:
    name = sys.argv[1]
  if len(sys.argv) < 3:
    run = main
    name2 = None
    p2 = None
  else:
    run = main2
    name2 = sys.argv[2]
  with open(name, "r") as fh:
    p = fh.readlines()
    p = [p.rstrip() for p in p]
  if name2:
      with open(name2, "r") as fh:
        p2 = fh.readlines()
        p2 = [p2.rstrip() for p2 in p2]
  run(p, p2)
