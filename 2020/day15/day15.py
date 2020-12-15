import sys
import timeit

fname = '../input/day15/input.txt'
#fname = '../input/day15/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines, end=2020):
    tt = lines[0]
    tt = list(map(int, tt.split(',')))
    tt.insert(0, 0)
    #print(tt[1:])
    r = {}
    i = 1
    while True and i <= end:
        if i < len(tt):
            lst = tt[i]
            r[lst] = [i]
            i += 1
            continue
        if lst in r:
            if lst not in r or len(r[lst]) == 0:
                r[lst] = []
            elif len(r[lst]) == 1:
                cur = 0
                r[cur].append(i)
            else:
                cur = r[lst][-1] - r[lst][-2]
                if cur not in r:
                    r[cur] = []
                r[cur].append(i)
                r[cur] = r[cur][-2:]
        #print(i,':',lst,cur,r,"==",cur)
        lst = cur
        i += 1
        if i % 1000000 == 0:
            print(i)
    return cur

start = timeit.default_timer()
if part1:
    num = ppart1(lines, 2020)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    num = ppart1(lines, 30000000)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
