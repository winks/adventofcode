import sys
import timeit

fname = '../input/day13/input.txt'
#fname = '../input/day13/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    ts = int(lines[0])
    #print(ts,lines[1].split(','))
    tt = list(lines[1].split(','))
    print(ts, tt, len(tt))
    tt = list(map(int, filter(lambda s: s != 'x', tt)))
    print(ts, tt)

    ts0 = ts
    while True:
        for t in tt:
            #print("#",ts)
            if ts % t == 0:
                return (t, ts-ts0)
        ts += 1

def ppart2(lines):
    tt = list(lines[1].split(','))
    print(tt, len(tt))
    #tt = list(map(int, filter(lambda s: s != 'x', tt)))
    #tt = list(map(int, tt))
    print(tt, len(tt))
    tt = [17, 13, 19]
    ts = 3400
    tt = [67,7,59,61]
    ts = 754018 - 3*67
    tt = [1789,37,47,1889]
    ts = 1202161486 - 2*1789
    ts = 0
    #tt = [67,'x',7,59,61]
    print(tt, len(tt))
    

    # x / t[0] == 0
    # x % t[1] == len-1
    # x % t[2] == len-2

    # 754018 % 67 = 0
    # 754018 % 7 = 6
    # 754018 % 59 = 0
    # 754018 % 61 = 0

    n = len(tt)
    
    while True:
        print("ts", ts)
        ok = True
        for i in range(0, len(tt)):
            if not ok:
                continue
            if i > 0 and ts % tt[i] != tt[i] - i:
                print("nm:", ts, i, tt[i])
                ok = False
            print(ts)
        if ok:
            return ts
        ts += tt[0]
        
    return 0


start = timeit.default_timer()
if part1:
    (ts, mins) = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(ts * mins)
else:
    num = ppart2(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
