import sys
import timeit

fname = '../input/day13/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    ts = int(lines[0])
    tt = list(lines[1].split(','))
    tt = list(map(int, filter(lambda s: s != 'x', tt)))

    ts0 = ts
    while True:
        for t in tt:
            if ts % t == 0:
                return (t, ts-ts0)
        ts += 1

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
    (ts, mins) = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(ts * mins)
else:
    #num = ppart2(["0", "7,13,x,x,59,x,31,19"])
    #end = timeit.default_timer()
    #print("#", (end - start) * 1000)

    #print(num, num == 1068781)
    #num = ppart2(["0", "67,7,59,61"])
    #print(num, num == 754018)
    #num = ppart2(["0", "67,7,x,59,61"])
    #print(num, num == 1261476)
    #num = ppart2(["0", "67,x,7,59,61"])
    #print(num, num == 779210)
    #num = ppart2(["0", "1789,37,47,1889"])
    #print(num, num == 1202161486)
    #num = ppart2(["0", "17,x,13,19"])
    #print(num, num == 3417)

    num = ppart2(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
