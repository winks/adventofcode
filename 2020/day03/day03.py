import sys

fname = '../input/day03/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

size_x = 0
size_y = 0
mmap = []
lines = []

with open(fname) as fh:
    lines = fh.readlines()

row = 0
for line in lines:
    line = line.strip()
    size_x = len(line)
    col = 0
    mmap.append([])
    for x in line:
        mmap[row].append(x)
        col = col + 1
    row = row + 1
size_y = row

def slope(step_x, step_y):
    x = 0
    y = 0
    num = 0
    while y < size_y - 1:
        x = x + step_x
        y = y + step_y
        if x >= size_x:
            x = x - size_x
        if mmap[y][x] == '#':
            num = num + 1
    return num

if part1:
    num = slope(3, 1)
    print(num)
    sys.exit(0)

n1 = slope(1, 1)
n2 = slope(3, 1)
n3 = slope(5, 1)
n4 = slope(7, 1)
n5 = slope(1, 2)

print(n1, n2, n3, n4, n5)
print(n1*n2*n3*n4*n5)
