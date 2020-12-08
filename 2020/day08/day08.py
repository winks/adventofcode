import sys
import re
import timeit

fname = '../input/day08/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()

codex = []
for line in lines:
    line = line.strip()
    parts = line.split(' ')
    cmd = parts[0]
    num = int(parts[1])
    codex.append((cmd, num))

def run(code):
    i = 0
    acc = 0
    visited = set()
    loop_acc = None
    finished = False
    while i < len(code):
        ins = code[i]
        #print("#", ins, i, acc)
        if i in visited:
            loop_acc = acc
            return [loop_acc, False, acc]
        visited.add(i)
        if ins[0] == 'acc':
            acc += ins[1]
            i += 1
            #print(acc, i)
            continue
        elif ins[0] == 'nop':
            i += 1
            #print(acc, i)
            continue
        elif ins[0] == 'jmp':
            i += ins[1]
            #print(acc, i)
            continue
        else:
            print("ERROR", i, ins)
    finished = True
    return [loop_acc, finished, acc]

def mutate(code, idx):
    code2 = code.copy()
    for i in range(idx, len(code)):
        if code2[i][0] == 'acc':
            continue
        elif code2[i][0] == 'jmp':
            code2[i] = ('nop', code2[i][1])
            return code2
        elif code2[i][0] == 'nop':
            code2[i] = ('jmp', code2[i][1])
            return code2
        else:
            print("error", i, code[i])
    return []

if part1:
    start = timeit.default_timer()
    (loop_acc, fin, acc) = run(codex)
    end = timeit.default_timer()
    print("#", (end - start) * 1000)
    if loop_acc:
        #print("loop detected, last acc:", loop_acc)
        print(loop_acc)
    else:
        print("hmmm", loop_acc, fin, acc)
else:
    idx = 0
    loop_acc = None
    finished = False
    acc = 0
    code2 = codex.copy()
    start = timeit.default_timer()
    avg = []
    while idx < len(code2) and not finished:
        start2 = timeit.default_timer()
        code2 = mutate(codex, idx)
        #print("mutated line",idx)
        (loop_acc, finished, acc) = run(code2)
        end2 = timeit.default_timer()
        avg.append((end2-start2))
        idx += 1
    #print("terminated with acc:", loop_acc, finished, acc, idx) #, code2)
    end = timeit.default_timer()
    print("#", (end - start) * 1000, len(avg), (sum(avg)/len(avg)) * 1000 )
    print(acc)
