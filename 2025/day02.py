import re
import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

rv1 = 0
rv2 = 0

if part1:
    for line in lines:
        parts = line.split(',')
        for pp in parts:
            p = pp.split('-')
            #print(p)
            for i in range(int(p[0]), int(p[1])+1):
                #print(i, end='')
                s = "{}".format(i)
                if re.match(r"^(\d+)\1$", s):
                    rv1 += i
                    #print(i)

else:
    h = {}
    for line in lines:
        parts = line.split(',')
        for pp in parts:
            p = pp.split('-')
            #print(p)
            for i in range(int(p[0]), int(p[1])+1):
                s = "{}".format(i)
                for j in range(1,11):
                    jj = '\\1' * j
                    m = rf"^(\d+){jj}$"
                    #print(m)
                    if re.match(m, s):
                        h[i] = True
                        #print(i)
    for k in h.keys():
        rv2 += k


if part1:
    print(rv1)
else:
    print(rv2)
