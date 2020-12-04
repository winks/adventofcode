import sys
import re

fname = '../input/day04/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

ff = ['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']
ffs = set(ff)
pp = []
lines = []
with open(fname) as fh:
    lines = fh.readlines()

i = 0

tmp = ""
for line in lines:
    line = line.strip()
    #print(line)
    tmp = tmp + " " + line
    if len(line) < 1 and i > 0:
        pp.append(tmp)
        tmp = ""
        continue
    i = i + 1
pp.append(tmp)

def chk(p):
    #print(p)
    ecl = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    if int(p['byr']) < 1920:
        #print("byr1")
        return False
    if int(p['byr']) > 2002:
        #print("byr2")
        return False
    if int(p['iyr']) < 2010:
        #print("iyr1")
        return False
    if int(p['iyr']) > 2020:
        #print("iyr2")
        return False
    if int(p['eyr']) < 2020:
        #print("eyr1")
        return False
    if int(p['eyr']) > 2030:
        #print("eyr2")
        return False
    if not re.match(r"^([0-9]{3}cm|[0-9]{2}in)$", p['hgt']):
        #print("hgt1", p['hgt'])
        return False
    if 'cm' == p['hgt'][3:]:
        h = int(p['hgt'][0:3])
        #print("hgt4",h)
        if h < 150 or h > 193:
            #print("hgt2",h)
            return False
    else:
        h = int(p['hgt'][0:2])
        #print("hgt5",h)
        if h < 59 or h > 76:
            #print("hgt3",h)
            return False
    if not re.match(r"^\#[0-9a-f]{6}$", p['hcl']):
        #print("hclr1", p['hcl'])
        return False
    else:
        #print("hclr2", p['hcl'])
        pass
    if p['ecl'] not in ecl:
        #print("ecl1")
        return False
    if not re.match(r"^[0-9]{9}$", p['pid']):
        #print("pid1", p['pid'])
        return False
    else:
        #print("pid2", p['pid'])
        pass
    #print("T")
    return True

#print(pp)
pp2 = []
valid = 0
for p in pp:
    parts = p.strip().split(' ')
    #print(parts)
    tmp = set()
    tmp2 = {}
    for pa in parts:
        pax = pa.split(':')
        k = pax[0].strip()
        v = pax[1].strip()
        tmp.add(k)
        tmp2[k] = v
        #print(k,v)
    #print(tmp, tmp2)
    
    if tmp == ffs:
        if part1:
            valid = valid + 1
        else:
            if chk(tmp2):
                valid = valid + 1
    else:
        t2 = tmp
        t2.add('cid')
        if t2 == ffs:
            if part1:
                valid = valid + 1
            else:
                if chk(tmp2):
                    valid = valid + 1

print(valid)
