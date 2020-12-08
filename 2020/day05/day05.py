import sys
import re

fname = '../input/day05/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()

def bsp(s, high, low = 0):
    th = high
    tl = low
    for i in range(0, len(s)-1):
        x = s[i]
        if x == 'F' or x == 'L':
            th = int((th + tl + 1) / 2)
        if x == 'B' or x == 'R':
            tl = int((th + tl + 1) / 2)
    if s[-1] == 'F' or s[-1] == 'L':
        return tl
    else:
        if th - tl > 1:
            return th - 1
        return th

seats = set()
for line in lines:
    line = line.strip()
    r = bsp(line[0:7], 127)
    x = bsp(line[7:], 7)
    a = r * 8 + x
    seats.add(a)

s2 = sorted(seats)

if part1:
    print(int(s2[-1]))
else:
    last = s2[0]
    for i in range(1, len(s2)):
        if s2[i] - last > 1 and s2[i] != s2[-1]:
            #print(last, s2[i], s2[i+1])
            print(last + 1)
        last = s2[i]
