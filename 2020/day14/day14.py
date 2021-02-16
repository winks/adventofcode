import sys
import timeit

fname = '../input/day14/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    mem = {}
    mask = ""
    ins = []
    sets = []
    for line in lines:
        if line[0:4] == 'mask':
            if len(mask) > 0:
                sets.append((mask, ins))
                ins = []
            mask = line.split(' ')[-1]
        else:
            addr = int(line.split(']')[0].split('[')[1])
            val = int(line.split(' ')[-1])
            ins.append((addr, val))
    sets.append((mask, ins))

    rv = 0
    bits = 36
    for cur_set in sets:
        m1 = cur_set[0].replace('X', '0')
        m11 = []
        m0 = cur_set[0].replace('X', '1')
        m00 = []
        for i in range(0, bits):
            m11.append(int(m1[i]))
            m00.append(int(m0[i]))

        m02 = 0
        m12 = 0
        for i in range(bits-1, -1, -1):
            if int(m1[i]) > 0:
                m12 += pow(2, bits-i-1)
            if int(m0[i]) == 0:
                m02 += pow(2, bits-i-1)

        for instr in cur_set[1]:
            mem[instr[0]] = (instr[1] | m12 ) & (~ m02)
    return sum(mem.values())


def ppart2(lines):
    def conv(s):
        if s == 'x':
            return 0
        return int(s)
    
    tt0 = list(map(conv,lines[1].split(',')))


start = timeit.default_timer()
if part1:
    num = ppart1(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)
else:
    num = ppart2(lines)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    print(num)

