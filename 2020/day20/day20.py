import sys
import timeit

fname = '../input/day20/input.txt'
#fname = '../input/day20/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def tiler2(tmp):
    tn = tmp[0]
    ts = tmp[-1] #[::-1]
    te = ""
    tw = ""
    for row in tmp:
        tw += row[0]
        te += row[-1]
    return [tn, te, ts, tw] #[::-1]]

def rot(tile):
    r1 = tile.copy()
    last = r1.pop()
    r1.insert(0, last)
    r2 = r1.copy()
    last = r2.pop()
    r2.insert(0, last)
    r3 = r2.copy()
    last = r3.pop()
    r3.insert(0, last)
    return [tile, r1, r2, r3]

def flip(tiles):
    rv = []
    for tile in tiles:
        tile[0] = tile[0][::-1]
        tile[2] = tile[2][::-1]
        tile[1], tile[3] = tile[3], tile[1]
        rv.append(tile)
    """
    for tile in tiles:
        for side in range(0, len(tile)):
            tile[side] = tile[side][::-1]
        tile[1], tile[3] = tile[3], tile[1]
        rv.append(tile)
    """
    return rv

def neigh(x, y, w, h):
    rv = []
    direc = ((-1, 0), (0, -1), (0, 1), (1, 0))
    for d in direc:
        if not (0 <= x + d[0] < w) or not (0 <= y + d[1] < h):
            continue
        rv.append((x + d[0], y + d[1]))
    return rv

def pp(combos):
    for c in combos:
        for tile in c:
            print(tile)
        print()

def ppart1(lines):
    cur = 0
    tiles = {}
    tmp = []
    #print(hash(lines[1]))
    #print(rev(hash(lines[1])))
    for line in lines:
        if line[0:5] == "Tile ":
            last = cur
            cur = int(line[5:].replace(':',''))
            if len(tmp) > 0:
                ##print(last, len(tmp))
                tile = tiler2(tmp)
                tiles[last] = tile
                
            tmp = []
        elif len(line) > 0:
            tmp.append(line)
    
    tile = tiler2(tmp)
    tiles[cur] = tile
    ##print(cur, len(tmp))
    #print(len(tiles))
    #print(tiles[2311])
    #print(rot(tiles[2311]))
    ##print(flip(rot(tiles[2311])))

    allx = {}
    for k in tiles.keys():
        tile = tiles[k]
        combos = rot(tile)
        combos.extend(flip(combos))
        #print(len(combos))
        allx[k] = combos

    """
    gridsize = 3
    grid = [[0,0,0],[0,0,0],[0,0,0]]
    grid[0][0] = 1951
    cur = (0, 0)
    curtile = allx[1951]
    #print(curtile)
    #pp(curtile)
    for k in allx.keys():
        if k != 1951:
            continue
        nex = neigh(0, 0, gridsize, gridsize)
        print(cur, nex)
        for ne in nex:
            print(cur, ne)

            if ne[0] - cur[0] == 0 and ne[1] - cur[1] == 1:
                print("right")
                #print(curtile)
                for j in allx.keys():
                    if j == 1951:
                        continue
                    for curt in curtile:
                        #print(curt)
                        for combos in allx[j]:
                            if combos[3] == curt[1]:
                                print(j, combos[3], curt[1])
                                #return
            if ne[0] - cur[0] == 1 and ne[1] - cur[1] == 0:
                print("down")
                for j in allx.keys():
                    if j == 1951:
                        continue
                    for curt in curtile:
                        #print(',', curt[2], curt[2] == "#.##...##.")
                        for combos in allx[j]:
                            if combos[0] == curt[2]:
                                print(j, combos[0], curt[2])
                                print(j)
                                #return
            if ne[0] - cur[0] == -1 and ne[1] - cur[1] == 0:
                print("up")
            if ne[0] - cur[0] == 0 and ne[1] - cur[1] == -1:
                print("left")
    """

    #gridsize = 3
    """
    for k in allx.keys():
        for j in allx.keys():
            if j == k:
                continue
            #nex = neigh(0, 0, gridsize, gridsize)
            print("# k",k,"j",j)
            cand = []
            seen = []
            for kk in allx[k]:
                for jj in allx[j]:
                    if kk[1] == jj[3]:
                        print("l",k,"r",j)
                        cand.append((k, j))
    """

    meh = {}
    for k in allx.keys():
        #print(k, allx[k])
        for kk in allx[k]:
            for kkk in kk:
                if kkk not in meh:
                    meh[kkk] = set()
                meh[kkk].add(k)
    #print(len(meh.keys()))
    #for k in meh.keys():
    #    print(k, meh[k])
    meh2 = {}
    for k in meh.keys():
        if k[::-1] not in meh2:
            meh2[k] = meh[k]
    #print(len(meh2.keys()))
    #for k in meh2.keys():
    #    print(k, meh2[k])

    cnt = {}
    for k in allx.keys():
        if k not in cnt:
            cnt[k] = 0
        for j in meh2.keys():
            if len(meh2[j]) == 2 and k in meh2[j]:
                cnt[k] += 1
    #print(cnt)
    corners = list(filter(lambda s: cnt[s] == 2, cnt.keys()))
    print("# corners:", len(corners),"#", corners)
    sides = list(filter(lambda s: cnt[s] == 3, cnt.keys()))
    print("# sides  :", len(sides),"#", sides)
    rest = set(allx.keys())
    rest = list(rest - set(corners) - set(sides))
    print("# rest   :", len(rest),"#", rest)

    rv = 1
    for c in corners:
        rv *= c
    return rv




def ppart2(lines):
    def conv(s):
        if s == 'x':
            return 0
        return int(s)
    
    tt0 = list(map(conv,lines[1].split(',')))
    indi = []
    i = 0
    for x in tt0:
        if x > 0:
            indi.append((i, x))
        i += 1

    ts = 13561262363414 * 41 # 556...
    ts = 2439024390243 * 41 # 1000...
    ts0 = ts
    rx = indi[0][1] * indi[1][1]
    while True:
        if ts % indi[0][1] == 0:
            if (ts + indi[1][0]) % indi[1][1] == 0:
                ts0 = ts
                break
        ts += indi[0][1]

    while True:
        ts += rx
        ok = True
        for i in indi[2:]:
            if (ts + i[0]) % i[1] != 0:
                ok = False
                break
        if ok:
            return ts
    return 0


start = timeit.default_timer()
if part1:
    num = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:

    num = ppart2(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)

"""

def hash(line):
    rv = ""
    cur = line[0]
    #print("---", line)
    for i in range(1, len(line)):
        #print(i, cur,rv)
        if line[i] != cur[0]:
            rv += str(len(cur)) + cur[0]
            cur = line[i]
        else:
            cur += line[i]
    return rv

def rev(hash):
    rv = ""
    for i in range(0, len(hash)):
        if i % 2 == 0:
            rv = hash[i] + hash[i+1] + rv
            i +=1
    return rv

def tiler(tmp):
    tn = hash(tmp[0])
    ts = hash(tmp[-1])
    te = ""
    tw = ""
    for row in tmp:
        tw += row[0]
        te += row[-1]
    te = hash(te)
    tw = hash(tw)
    return [tn, te, ts, tw]
"""