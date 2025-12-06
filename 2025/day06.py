import re
import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.rstrip("\n"), lines))

if part1:
    rv1 = 0
    m = []
    for line in lines:
        line = re.sub(r"\s+", ' ', line)
        p = line.strip().split(' ')
        #print(p)
        if line[0] == "+" or line[0] == "*":
            pass
        else:
            p = list(map(lambda a: int(a), p))
            #print(p)
        m.append(p)

    #print(m)
    m2 = []
    for i in range(0, len(m[0])):
        tmp = []
        for j in range(0, len(m)):
            tmp.append(m[j][i])
        m2.append(tmp)
    #print(m2)

    for i in m2:
        op = i[-1]
        del i[-1]
        if op == '+':
            acc = 0
            f = lambda acc, x: acc +x
            a = [acc := f(acc, x) for x in i]
            rv1 += acc
        else:
            acc = 1
            a = [acc := acc * x for x in i]
            rv1 += acc

    print(rv1)
else:
    ops = lines[-1]
    #print(ops)
    idxs = []
    for i in range(0, len(ops)):
        if ops[i] == '+' or ops[i] == '*':
            idxs.append(i)
    #print(idxs)
    rv2 = 0
    m = []

    for line in lines:
        tmp = []
        for idx in range(0, len(idxs)):
            if idx == 0:
                continue
            s = line[idxs[idx-1]:idxs[idx]-1]
            tmp.append(s)
            if idx == len(idxs)-1:
                s = line[idxs[idx]:]
                tmp.append(s)
        m.append(tmp)
    #print(m)
    m2 = []
    for i in range(0, len(m[0])):
        tmp = []
        for j in range(0, len(m)):
            tmp.append(m[j][i])
        m2.append(tmp)
    #print(m2)

    for i in range(0, len(m2)):
        op = m2[i][-1].strip()
        del m2[i][-1]
        mx = len(m2[i][0])
        for j in m2[i]:
            mx = max(mx, len(j))
        #print(mx)
        col = 0
        tm = []
        for ii in range(mx-1, -1, -1):
            tt = ''
            for v in m2[i]:
                t = '0'
                try:
                    t = v[ii]
                except IndexError:
                    pass
                #print(ii,v,t)
                tt += t
            #print(tt, int(tt))
            tm.append(int(tt))

        if op == '+':
            acc = 0
            a = [acc := acc + x for x in tm]
            rv2 += acc
        else:
            acc = 1
            a = [acc := acc * x for x in tm]
            rv2 += acc
        #print(rv2)

    print(rv2)
