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
    #for i in range(0, 36):
    #    mem.append(0)
    #print(mem, len(mem))
    curm = ""
    ins = []
    sets = []
    for line in lines:
        if line[0:4] == 'mask':
            if len(curm) > 0:
                sets.append((curm, ins))
                #print(curm, ins)
                ins = []
            curm = line.split(' ')[-1]
        else:
            #print(line.split(']')[0])
            addr = int(line.split(']')[0].split('[')[1])
            val = int(line.split(' ')[-1])
            ins.append((addr, val))
    sets.append((curm, ins))
    #print(len(sets))
    #print('------')
    
    rv = 0
    for sx in sets:
        curm = sx[0]
        ins = sx[1]
        m1 = curm.replace('X', '0')
        m0 = curm.replace('X', '1')
        #print(m1)
        #print(m0)
        m00 = []
        m02 = 0
        m11 = []
        m12 = 0
        for i in range(0, len(m1)):
            c1 = int(m1[i])
            c0 = int(m0[i])
            m11.append(c1)
            m00.append(c0)
        for i in range(len(m1)-1, -1, -1):
            if int(m1[i]) > 0:
                #print(i, m1[i], len(m1)-i-1, pow(2,len(m1)-i-1))
                m12 += pow(2, len(m1)-i-1)
            if int(m0[i]) == 0:
                #print(i, m1[i], len(m1)-i-1, pow(2,len(m1)-i-1))
                m02 += pow(2, len(m1)-i-1)
        #print(''.join(map(str,m11)), m12)
        #print(''.join(map(str,m00)),'~', m02)

        for instr in ins:
            tmpv = rv
            tmpv = instr[1] | m12
            #print(instr[1], tmpv, rv)
            tmpv = tmpv & (~ m02)
            #print(instr[1], tmpv, rv)
            mem[instr[0]] = tmpv
    #print(len(mem))
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

