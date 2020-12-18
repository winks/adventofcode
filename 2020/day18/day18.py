import sys
import timeit
import re

fname = '../input/day18/input.txt'
#fname = '../input/day18/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def red1(tok):
    rv = 0
    if len(tok) >= 3:
        if tok[1] == '+':
            rv = int(tok[0]) + int(tok[2])
        elif tok[1] == '*':
            rv = int(tok[0]) * int(tok[2])
        tok = tok[3:]
        tok.insert(0, rv)
    return tok

def red2(tok):
    while True:
        if not '+' in tok:
            break
        for s in range(0, len(tok)):
            if tok[s] != '+':
                continue
            rv = int(tok[s-1]) + int(tok[s+1])
            to = tok.copy()
            tok = to[0:s-1]
            tok.append(rv)
            tok.extend(to[s+2:])
            break

    return red1(tok)

def parse(xx):
    tok = []
    last = ""
    for x in xx:
        if x == ' ' or x == '(' or x == ')':
            if len(last) > 0:
                tok.append(last)
            last = ""
            continue
        elif x == '+' or x == '*':
            if len(last) > 0:
                tok.append(last)
            last = ""
            tok.append(x)
        else:
            if len(last) > 0:
                last += x
            else:
                last = x
    if len(last) > 0:
        tok.append(last)
    return tok

def ppart1(lines, redfn=None):
    redfn = redfn or red1
    p = re.compile(r'(\([^\(\)]+\))')
    rv = []
    for line in lines:
        tok = []
        while True:
            m = p.search(line)
            if not m:
                break
            tok = parse(m.groups()[0])
            while len(tok) > 1:
                tok = redfn(tok)
            if len(tok) < 2:
                line = line.replace(m.groups()[0], str(tok[0]))
                if not '(' in line:
                    break
        
        tok = parse(line)
        while len(tok) > 1:
            tok = redfn(tok)
        rv.append(tok[0])
    return sum(rv)

start = timeit.default_timer()
if part1:
    num = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    num = ppart1(lines, red2)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
