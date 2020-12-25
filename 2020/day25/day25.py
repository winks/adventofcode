import sys
import timeit

fname = '../input/day25/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    p1 = int(lines[0])
    p2 = int(lines[1])
    print("#", p1, p2)

    expo = 1
    rem = 20201227
    while True:
        x = pow(7, expo, rem)
        if x == p1:
            y = pow(p2, expo, rem)
            return y
        if x == p2:
            y = pow(p1, expo, rem)
            return y
        expo += 1

start = timeit.default_timer()
num = ppart1(lines)
end = timeit.default_timer()
print("#", (end - start) * 1000)
print(num)
