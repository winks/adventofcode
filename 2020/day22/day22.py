import sys
import timeit
import re

fname = '../input/day22/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def play(d1, d2):
    i = 1
    while True:
        if len(d1) < 1 or len(d2) < 1:
            break
        c1 = d1.pop(0)
        c2 = d2.pop(0)
        if c1 > c2:
            d1.append(c1)
            d1.append(c2)
        elif c2 > c1:
            d2.append(c2)
            d2.append(c1)
        i += 1
    
    if len(d1) > 0:
        print("p1 won:", len(d1), len(d2))
        winner = d1
    else:
        print("p2 won:", len(d2), len(d1))
        print(d2)
        winner = d2

    rv = 0
    i = 1
    while True:
        if len(winner) < 1:
            break
        c = winner.pop()
        x = (c * i)
        #print(c, x)
        rv += x
        i += 1
    return rv

def ppart1(lines):
    player1 = True
    deck1 = []
    deck2 = []
    for line in lines:
        if line[0:8] == "Player 2":
            player1 = False
        if line[0:4] == "Play" or len(line) == 0:
            continue
        if player1:
            deck1.append(int(line))
        else:
            deck2.append(int(line))
    
    print(deck1)
    print(deck2)
    return play(deck1, deck2)

def ppart2(lines):
    pass

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
