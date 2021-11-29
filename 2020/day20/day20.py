import sys
import timeit
from copy import deepcopy
import math

fname = '../input/day20/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def tiler2(tmp):
    tn = tmp[0]
    ts = tmp[-1]
    te = ""
    tw = ""
    for row in tmp:
        tw += row[0]
        te += row[-1]
    return [tn, te, ts, tw]

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
    return rv

def get_tiles(lines, full=False):
    cur = 0
    tiles = {}
    tmp = []
    for line in lines:
        if line[0:5] == "Tile ":
            last = cur
            cur = int(line[5:].replace(':',''))
            if len(tmp) > 0:
                tile = tiler2(tmp)
                if full:
                    tile.append(tmp)
                tiles[last] = tile
            tmp = []
        elif len(line) > 0:
            tmp.append(line)

    tile = tiler2(tmp)
    if full:
        tile.append(tmp)
    tiles[cur] = tile
    return tiles

def get_combos(tiles):
    allx = {}
    for k in tiles.keys():
        tile = tiles[k]
        combos = rot(tile)
        combos.extend(flip(combos))
        allx[k] = combos
    return allx

def get_parts(allx):
    meh = {}
    for k in allx.keys():
        for kk in allx[k]:
            for kkk in kk:
                if kkk not in meh:
                    meh[kkk] = set()
                meh[kkk].add(k)
    meh2 = {}
    for k in meh.keys():
        if k[::-1] not in meh2:
            meh2[k] = meh[k]
    cnt = {}
    for k in allx.keys():
        if k not in cnt:
            cnt[k] = 0
        for j in meh2.keys():
            if len(meh2[j]) == 2 and k in meh2[j]:
                cnt[k] += 1
    return cnt

def rot_full(tmp, num):
    rv = []
    n = len(tmp)
    row = []
    for j in range(0, n):
        row.append("o")
    for i in range(0, n):
        rv.append(row)

    for i in range(0, n):
        for j in range(0, n):
            if num == 1:
                pass
                #rv[] = tmp[i][j]


    return rv

def ppart1(lines):
    tiles = get_tiles(lines)
    allx = get_combos(tiles)
    cnt = get_parts(allx)

    corners = list(filter(lambda s: cnt[s] == 2, cnt.keys()))
    #print("# corners:", len(corners),"#", corners)
    #sides = list(filter(lambda s: cnt[s] == 3, cnt.keys()))
    #print("# sides  :", len(sides),"#", sides)
    #rest = list(set(allx.keys()) - set(corners) - set(sides))
    #print("# rest   :", len(rest),"#", rest)

    rv = 1
    for c in corners:
        rv *= c
    return rv

def ppart2(lines):
    tiles = get_tiles(lines)
    allx = get_combos(tiles)
    cnt = get_parts(allx)

    corners = list(filter(lambda s: cnt[s] == 2, cnt.keys()))
    sides = list(filter(lambda s: cnt[s] == 3, cnt.keys()))

    tiles = get_tiles(lines, full=True)
    for t in tiles.keys():
        if t in corners:
            print(t, tiles[t])

    cur = corners.pop()


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
