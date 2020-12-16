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

def ppart22(inv, rules, t_you, t_near):
    near2 = []
    for near in t_near:
        if near not in inv:
            near2.append(near)
    print('----1')
    print(near2)
    print('----2')
    print(rules)
    print('----3')
    #mut = list(permutations(map(lambda s: s[0], rules)))
    #print(mut)
    print('----4')

    rules2 = {}
    for i in range(0, len(rules)):
        name = rules[i][0]
        rules2[name] = (rules[i][1], rules[i][2])

    ok_m = []
    #for m in list(mut):
    for m in permutations(map(lambda s: s[0], rules)):
        valid_m = 0
        print(":",m)
        for near in near2:
            print(near)
            valid = 0
            for i in range(0, len(near)):
                rule = rules2[m[i]]
                print(rule, i)
                if (rule[0][0] <= near[i] <= rule[0][1]) or (rule[1][0] <= near[i] <= rule[1][1]):
                    valid += 1
                else:
                    break
            if valid == len(near):
                valid_m += 1
            else:
                break
        if valid_m == len(m):
            ok_m.append(m)
        print('--')
    print('-----')
    print(ok_m)
    #if len(ok_m) > 1:


def ppart2(inv, rules, t_you, t_near):
    near2 = []
    for near in t_near:
        if near not in inv:
            near2.append(near)
    print('----1')
    print(near2)
    print('----2')
    print(rules)
    print('----3')
    #mut = list(permutations(map(lambda s: s[0], rules)))
    #print(mut)
    rule_names = list(map(lambda s: s[0], rules))
    #print(len(mut))
    print(rule_names)
    rules2 = {}
    for i in range(0, len(rules)):
        name = rules[i][0]
        rules2[name] = (rules[i][1], rules[i][2])
    print(rules2)
    print('----4')

    ok = []

    def ck(ticket, rule):
        #print(ticket, rule)
        r = []
        for i in range(0, len(ticket)):
            if (rule[0][0] <= ticket[i] <= rule[0][1]) or (rule[1][0] <= ticket[i] <= rule[1][1]):
                #r.append((i, ticket))
                ##r.append(i)
                pass
            else:
                #r.append((None, None))
                ##r.append(None)
                r.append(i)
        return r

    banlist = {}
    near2.append(t_you)
    for rule_name in rule_names:
        for t in range(0, len(near2)):
            ticket = near2[t]
            v = ck(ticket, rules2[rule_name])
            print(ticket, rule_name, v)
            #if (None, None) in v:
            ##if None in v:
            if len(v) > 0:
                if rule_name not in banlist:
                    banlist[rule_name] = []
                banlist[rule_name].append(v[0])
    print('--------------')
    print(banlist)
    for r in banlist.keys():
        print(r, len(banlist[r]), len(near2))

    fixed = []
    idx = len(t_you) - 1
    while idx > 1:
        print("#", idx)
        for k in banlist.keys():
            print(',',banlist[k])
            if len(banlist[k]) == idx:
                a = set(list(range(0, len(t_you))))
                b = set(banlist[k])
                fixed.append(( a - b , k))
            else:
                print("!!!",idx)
        idx -= 1
    print('###')
    print(fixed)
    print('###')
    fixed2 = [fixed[0]]
    last = None
    acc = set().union(fixed[0][0])
    for f in fixed:
        if not last:
            last = fixed[0]
            continue
        if len(f[0]) > 1:
            ff = f[0] - acc
            for x in f[0]:
                acc.add(x)
            fixed2.append((ff, f[1]))
    print('###')
    print(acc, len(fixed2))
    print(fixed2)

    rv = []
    for i in range(0, len(t_you)):
        for f in fixed2:
            #print('_',f)
            if list(f[0])[0] == i:
                print(',',i,f[1]," =",t_you[i])
                if f[1][0:5] == 'depar':
                    rv.append(t_you[i])
    print(rv)
    x = 1
    for y in rv:
        x *= y
    return x


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
