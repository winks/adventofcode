import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def a(line, start):
    acc = {}
    tmp = ""
    for x in range(start, 0, -1):
        posx = line.find(f"{x}")
        if posx + 1 >= len(line) and len(tmp) < 2:
            tmp = ""
            continue

        for y in range(start, 0, -1):
            posy = line.find(f"{y}", posx+1)
            if posy == posx or posx < 0 or posy < 0:
                continue
            #print(f"# {x},{y} @ {posx} {posy}")
            if posx >= 0 and posy >= 0:
                tmp = f"{line[posx]}{line[posy]}"
            if len(tmp) == 2:
                acc[tmp] = True
                #print(acc.keys())
                tmp = tmp[0]
                #continue
    #print(acc.keys())
    acc = map(lambda a: int(a), acc.keys())
    return sorted(acc)[-1]

def b(bank, k):
    pos = 0
    rv = []
    for rem in range(k, 0, -1):
        end = len(bank) - rem + 1
        top = max(bank[pos:end])
        b2 = bank[pos:end]
        pos = bank.index(top, pos, end) + 1
        rv.append(top)
        print(b2, top, pos, end)
    return int(''.join(map(lambda x: str(x), rv)))

if part1:
    rv1 = 0
    for line in lines:
        #print(line, len(line))
        m = a(line, 9)
        #print(m)
        rv1 += int(m)
    print(rv1)
else:
    rv2 = 0
    for line in lines:
        bank = [int(n) for n in line]
        #bx = b(bank, 12)
        bx = b(bank, 2)
        rv2 += bx
    print(rv2)
