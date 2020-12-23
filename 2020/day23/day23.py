import sys
import timeit
import re

fname = '../input/day23/input.txt'
#fname = '../input/day23/test'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def ppart1(lines):
    nums = []
    for c in lines[0]:
        nums.append(int(c))
    
    pos = 0
    cur = nums[0]
    max_len = len(nums)
    min_val = min(nums)
    max_val = max(nums)
    print(nums, cur, "@", pos)
    print()
    last = cur

    for i in range(0, 100):
        tmp = []
        for i in range(0, 3):
            x = (pos+1) % len(nums)
            #print(",",x,"_",nums[x],tmp,nums)
            tmp.append(nums.pop(x))
            pos = nums.index(cur)
            #print(",",tmp,nums, len(nums))
        print(nums)
        print(tmp)
        num_ins = cur - 1
        print(num_ins)
        while num_ins in tmp or num_ins < 1:
            num_ins -= 1
            if num_ins < min_val or num_ins < 1:
                num_ins = max_val
        print(num_ins)
        pos_ins = nums.index(num_ins)
        
        while len(tmp) > 0:
            nums.insert(pos_ins + 1, tmp.pop())
        pos = (nums.index(cur) + 1) % len(nums)
        print(pos)
        cur = nums[pos]
        #cur += 1
        print(nums, cur, "@", pos)
        print()
    
    x = nums.index(1) + 1
    rv = ""
    for i in range(0, len(nums)-1):
        rv += str( nums[(i+x) % len(nums)] )
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
