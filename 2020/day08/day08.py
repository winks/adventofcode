import copy
import sys
import re

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
    codex.append([cmd, num])

def run(code):
    i = 0
    j = 0
    acc = 0
    visited = []
    loop_acc = None
    finished = False
    while i < len(code): # and j < 15:
        ins = code[i]
        #print("#", ins, i, acc)
        j += 1
        if i in visited:
            loop_acc = acc
            return [loop_acc, False, acc]
        visited.append(i)
        if ins[0] == 'acc':
            acc = acc + ins[1]
            i += 1
            #print(acc, i)
            continue
        elif ins[0] == 'nop':
            i += 1
            #print(acc, i)
            continue
        elif ins[0] == 'jmp':
            i = i + ins[1]
            #print(acc, i)
            continue
        else:
            print("ERROR", i, ins)
    finished = True
    return [loop_acc, finished, acc]

def mutate(code, idx):
    code2 = copy.deepcopy(code)
    for i in range(idx, len(code)):
        if i < idx:
            continue
        if code2[i][0] == 'acc':
            continue
        elif code2[i][0] == 'jmp':
            code2[i][0] = 'nop'
            return code2
        elif code2[i][0] == 'nop':
            code2[i][0] = 'jmp'
            return code2
        else:
            print("error", i, code[i])
    return []

if part1:
    (loop_acc, fin, acc) = run(codex)
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
    code2 = copy.deepcopy(codex)
    while idx < len(code2) and not finished:
        code2 = mutate(codex, idx)
        #print("mutated line",idx)
        (loop_acc, finished, acc) = run(code2)
        idx += 1
    #print("terminated with acc:", loop_acc, finished, acc, idx) #, code2)
    print(acc)