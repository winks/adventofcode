import sys
import timeit
from itertools import permutations

fname = '../input/day16/input.txt'
#fname = '../input/day16/test2'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    rules = []
    t_you = []
    t_near = []
    yours = False
    nearby = False
    for line in lines:
        if len(line) == 0:
            continue
        if line[0:6] == 'your t':
            yours = True
            continue
        elif line[0:8] == 'nearby t':
            nearby = True
            continue
        elif yours:
            t_you = tuple(map(int, line.split(',')))
            yours = False
            continue
        elif nearby:
            t_near.append(tuple(map(int, line.split(','))))
            continue

        pa = line.split(':')
        px = pa[1].split(' or ')
        rules.append((pa[0], tuple(map(int, px[0].strip().split('-'))), tuple(map(int, px[1].strip().split('-')))))
    print(rules)
    print(t_you)
    print(t_near)

    invalid = []
    invalid_tickets = []
    for near in t_near:
        print(near)
        valid = 0
        tmp = {}
        for n in near:
            for i in range(0, len(rules)):
                rule = rules[i]
                if (rule[1][0] <= n <= rule[1][1]) or (rule[2][0] <= n <= rule[2][1]):
                    valid += 1
                else:
                    if n not in tmp:
                        tmp[n] = 1
                    else:
                        tmp[n] += 1
        print(valid, tmp)
        #tmp = filter(lambda )
        for k in tmp.keys():
            if tmp[k] == len(rules):
                invalid.append(k)
                invalid_tickets.append(near)
                break
    print(invalid)
    r = 0
    for i in invalid:
        r += i
    return (r, invalid_tickets, rules, t_you, t_near)

    #mut = permutations(map(lambda s: s[0], rules))
    #print(list(mut))


def ppart2(lines):
    tt = lines[0]
    tt = list(map(int, tt.split(',')))

start = timeit.default_timer()
if part1:
    (num,_,_,_,_) = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    (_,inv,rules,t_you,t_near) = ppart1(lines)
    num = ppart2(inv, rules, t_you, t_near)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
