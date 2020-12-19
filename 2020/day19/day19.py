import sys
import timeit
import re

fname = '../input/day19/input.txt'
#fname = '../input/day19/test2'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    rules = {}
    top = True
    data = []
    for line in lines:
        print("#", line)
        if len(line) == 0:
            top = False
            continue
        if not top:
            data.append(line)
            continue
        line = line.split(":")
        r = line[1].strip()
        rules[line[0]] = r
    print(rules,data)
    rules2 = {}

    for k in rules.keys():
        if '"' in rules[k]:
            print("mend", rules[k])
            rules2[k] = ["_leaf", rules[k].replace('"', '')]
            continue
        if '|' in rules[k]:
            print("malt", rules[k])
            x = rules[k].split('|')
            x = list(map(lambda s: s.strip(), x))
            x = list(map(lambda s: ["_row", s.split(" ")], x))
            #x = ["_row", x]
            rules2[k] = ["_alt", x]
        else:
            rules2[k] = ["_row", rules[k].split(' ')]
    print(rules2)

    rex = ""

    def resolve(r, rules2, acc=None):
        print("#resolve",r)
        if r[0] == "_leaf":
            return r[1]
        if r[0] == "_row":
            parts = []
            for k in r[1]:
                x = resolve(rules2[k], rules2)
                if x[0] != "_leaf":
                    x = resolve(x, rules2)
                parts.append(x)
            print("p",parts)
            done = False
            while not done:
                for px in range(0, len(parts)):
                    if isinstance(parts[px], list) and parts[px][0] == "_":
                        parts[px] = resolve(parts[px], rules2)
                        done = False
                    done = True
                #if not done:
                #for p in range(0, len(parts)):
                #    parts[p] = resolve(parts[p], rules2)
            
            print("333",parts)
            #for p in parts:
            #if isinstance()
            acc = ""
            for p in parts:
                if not isinstance(p, list):
                    acc += p
                else:
                    acc += "("+ "|".join(p) + ")"
            print("333",parts,x,acc)
            return acc
            return "("+x+")"
                
        if r[0] == "_alt":
            alts = []
            for k in r[1]:
                print(k)
                alts.append(resolve(k, rules2))
            print("alts",alts)
            return alts
        if not acc:
            return r
        acc += r
        return acc

    #for k in rules2[k]:

    x = resolve(rules2['0'], rules2,"")
    print(x)
    r = r"^"+x+"$"
    #print(re.match(r, "aab"))
    #print(re.match(r, "aba"))
    #print(re.match(r, "aaa"))
    # 2 3 
    # 44 45  44 54  55 45  55 54
    # aaab   aaba   bbab   bbba

    # 3 2
    #

    rv = 0
    for d in data:
        res = re.match(r, d)
        print(d,r, res and "ok")
        if res:
            rv += 1
    return rv


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
