import sys
import timeit

part1 = True
if len(sys.argv) > 2 and sys.argv[2]:
    part1 = False

lines = []
with open(sys.argv[1], 'r') as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

cur = 50
rv1 = 0
rv2 = 0

for line in lines:
    num = int(line[1:])
    if line[0] == "R":
        cur = cur + num
        while cur > 99:
            cur = cur - 100
    else:
        cur = cur - num
        while cur < 0:
            cur = cur + 100
    if cur == 0:
        rv1 = rv1 + 1

cur = 50

for line in lines:
    num = int(line[1:])
    if line[0] == "R":
        for i in range(0, num):
          cur += 1
          if cur == 100:
            cur = 0
          if cur == 0:
            rv2 += 1
            #print(rv2)
    elif line[0] == "L":
        for i in range(0, num):
          cur -= 1
          if cur == -100:
            cur = 0
          if cur == 0:
            rv2 += 1
    #print("    ...",last)


if part1:
    print(rv1)
else:
    print(rv2)
