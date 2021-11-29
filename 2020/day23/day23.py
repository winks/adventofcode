import sys
import timeit
import re

fname = '../input/day23/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

lines = []
with open(fname) as fh:
    lines = fh.readlines()
    lines = list(map(lambda s: s.strip(), lines))

def run1(nums, runs=100):
    pos = 0
    cur = nums[0]
    min_val = 1
    max_val = 9

    for i in range(0, runs):
        tmp = []
        for i in range(0, 3):
            x = (pos+1) % len(nums)
            tmp.append(nums.pop(x))
            pos = nums.index(cur)
        num_ins = cur - 1
        while num_ins in tmp or num_ins < min_val:
            num_ins -= 1
            if num_ins < min_val:
                num_ins = max_val
        pos_ins = nums.index(num_ins)

        while len(tmp) > 0:
            nums.insert(pos_ins + 1, tmp.pop())
        pos = (nums.index(cur) + 1) % len(nums)
        cur = nums[pos]
    
    x = nums.index(1) + 1
    rv = ""
    for i in range(0, len(nums)-1):
        rv += str( nums[(i+x) % len(nums)] )
    return rv


def run2(nums, runs=100, overall=9):
    pos = 0
    cur = nums[pos]
    min_val = 1
    max_val = overall
    #print(nums, cur, "@", pos)
    #print()

    for i in range(0, runs):
        tmp = []
        x_pos = pos
        for i in range(0, 3):
            ###x = (pos+1) % len(nums)
            #print(",",x,"_",nums[x],tmp,nums)
            ###tmp.append(nums.pop(x))
            ###pos = nums.index(cur)

            x_pos = (x_pos+1) % overall
            print(x_pos)
            if x_pos in nums.keys():
                tmp.append(nums[x_pos])
                del nums[x_pos]
                #x_pos += 1

            lo = sorted(nums.keys())
            lala = []
            for l in lo:
                lala.append(nums[l])
            print(",",tmp,lala, len(nums.keys()), nums.keys())
        break
        #print(nums)
        #print(tmp)
        num_ins = cur - 1
        #print(num_ins)
        while num_ins in tmp or num_ins < min_val:
            num_ins -= 1
            if num_ins < min_val or num_ins < min_val:
                num_ins = max_val
        #print(num_ins)
        pos_ins = nums.index(num_ins)
        
        while len(tmp) > 0:
            nums.insert(pos_ins + 1, tmp.pop())
        pos = (nums.index(cur) + 1) % len(nums)
        #print(pos)
        cur = nums[pos]
        #cur += 1
        #print(nums, cur, "@", pos)
        #print()
        if i % 100 == 0:
            print("#",i)
    
    print(nums)
    x = nums.index(1) + 1
    y = nums.index(1) + 2
    return (nums[x], nums[y], nums[x] * nums[y])

class WeirdList():
    start = None
    end = None
    state = []
    indexx = 0
    def __init__(self, state=None, start=None, end=None):
        #print("_init",state,start,end)
        if state:
            self.state = state
            #for s in state:
            #    if isinstance(s, WeirdList):
            #        self.state.append(s)
            #    else:
            #        n = WeirdList(state=None, start=s)
            #        print("_crea",n, s, isinstance(s, WeirdList))
            #        self.state.append(n)
            #self.indexx = 0
        else:
            #print("_ielse")
            self.start = start
            self.end = end
    def __repr__(self):
        if self.end is None:
            return "WLs<{}>".format(self.start)
        elif self.start:
            return "WLse<[{}...{}]({})>".format(self.start, self.end, (self.end-self.start+1))
        elif len(self.state) == 1:
            return "WL_<[{}]>".format(self.state[0])
        elif len(self.state) == 2:
                return "WL_<[{},{}]>".format(self.state[0],self.state[1])
        elif len(self.state) == 3:
            return "WL_<[{},{},{}]>".format(self.state[0].__repr__(),self.state[1].__repr__(),self.state[2].__repr__())
        elif len(self.state) > 3:
            return "WL_<[...] ({})>".format(len(self.state[0]))
        else:
            raise Exception
    def append(self, x):
        if self.start:
            m2 = WeirdList(None, self.start, self.end)
            self.start = None
            self.end = None
            self.state.append(m2)
            self.state.append(x)
        else:
            self.state.append(x)
    def __iter__(self):
        return self.state.__iter__()
    def __next__(self):
        if self.indexx + 1 >= len(self.state):
            raise StopIteration
        self.indexx = self.indexx + 1
        return self.state[self.indexx]
    def pop(self, idx=None):
        if idx is not None and idx >= len(self):
            raise IndexError
        print("_pop", idx, len(self.state))
        if self.end:
            if idx is None or idx == len(self) - 1:
                last = self.end
                self.end -= 1
                self.state = []
                #self.state.append(x)
                print("__pop_fork", last, self.start, self.end, len(self), self)
                return WeirdList(None, last)
        elif self.start:
            return x
        else:
            print("_pope", self.state)
            if idx is None:
                idx = len(self.state) - 1
            x = self.state.pop(idx)
            print(x)
            return x
            #print("__pop", x, x.pp(), x.start, x.end,  self.state, self.start, self.end)
    def __len__(self):
        rv = 0
        #print("called __len", self.start, self.end,"=",rv)
        if self.end:
            rv += (self.end - self.start +1)
        elif self.start:
            rv += 1
        else:
            for s in self.state:
                if s.end:
                    #print(s.end - s.start, rv)
                    rv += (s.end - s.start + 1)
                elif s.start:
                    rv += 1
                else:
                    #print("rec",s.state)
                    rv += len(s.state)
        #print("called __len",self.state, self.start, self.end,"=",rv)
        #print("called __len", self.start, self.end,"=",rv)
        return rv
    def __index__(self):
        if not self.end and self.start:
            return self.start
        else:
            raise TypeError
    def index(self, x):
        x2 = WeirdList(None, x)
        a = self.state.index(x2)
        return a
    def __eq__(self, other):
        if self.end:
            return self.end == other.end and self.start == other.start
        elif self.start:
            #print("eq", self.end, self.start, other)
            if isinstance(other, WeirdList):
                return self.start == other.start
            else:
                return self.start == other
        else:
            raise ValueError
    def contains(self, i):
        if self.end:
            return self.start <= i <= self.end
        elif self.start:
            return self.start == i
        else:
            #print("__cont",len(self.state))
            for x in self.state:
                if x.contains(i):
                    return True
            return False
    def pp(self):
        rv = []
        for k in self.state:
            rv.append(k.__repr__())
        return ",".join(rv)
    def __str__(self):
        return self.__repr__()
    def insert(self, idx, item):
        print("_ins", idx, item, item.pp(), "            " ,self.state)
        if self.end or self.start:
            raise ValueError
        cx = False
        for i in range(0, idx):
            if len(self.state[i]) > 1:
                print("??", i, len(self.state[i]), self.state[i])
                cx = True
                break
        if not cx:
            self.state.insert(idx, item)
        else:
            print("MEH")
            raise TypeError
    def __getitem__(self, idx):
        if self.end or self.start:
            raise ValueError
        cx = False
        for i in range(0, idx):
            if len(self.state[i]) > 1:
                cx = True
                break
        if cx:
            print("MEH2", i, self.state[i])
            raise TypeError
        else:
            return self.state[idx]




def run11(nums, runs=100):
    pos = 0
    cur = nums[0]
    min_val = 1
    max_val = max(nums)

    for i in range(0, runs):
        tmp = []
        for i in range(0, 3):
            x = (pos+1) % len(nums)
            tmp.append(nums.pop(x))
            pos = nums.index(cur)
        num_ins = cur - 1
        while num_ins in tmp or num_ins < min_val:
            num_ins -= 1
            if num_ins < min_val:
                num_ins = max_val
        pos_ins = nums.index(num_ins)
        #print(nums, cur, "@", pos)
        #print(tmp)
        

        while len(tmp) > 0:
            nums.insert(pos_ins + 1, tmp.pop())
        pos = (nums.index(cur) + 1) % len(nums)
        cur = nums[pos]

        print("#",nums)
        #print("--")
        #print()
        #print()
    
    #x = nums.index(1) + 1
    #y = nums.index(1) + 2
    #return (nums[x], nums[y], nums[x] * nums[y])

def run12(nums, runs=100, max_num=20):
    pos = 0
    cur = nums[0]
    min_val = 1
    max_val = 9

    nums2 = []
    for n in nums:
        n = WeirdList(None, n)
        nums2.append(n)
    
    print(nums2)
    rest = WeirdList(None, max_val+1, max_num)
    print(len(nums2) == 9, len(rest) == 11)
    nums2.append(rest)
    nums = WeirdList(nums2)
    cur = nums[0]
    print(len(nums) == 20)
    print('---')
    w1 = WeirdList(None, 1)
    w11 = WeirdList([w1])
    x = nums.contains(w1)
    y = w11.contains(w1)
    print(x,y,len(w1) == 1, len(w11)== 1)
    print('---')
    w3 = WeirdList(None, 3)
    w4 = WeirdList(None, 4)
    w11.append(w3)
    w11.append(w4)
    print(len(w11) == 3)
    wx = w11.pop()
    print(wx == w4,len(wx) == 1, len(wx.state) == 0, wx.start == 4, wx.end is None)
    w11.insert(0, wx)
    print('#t3',len(w11) == 3)
    wx = w11.pop(0)
    print(wx == w4, len(w11) == 2)
    print('---')
    ws = WeirdList(None, 2, 4)
    print(len(ws) == 3, ws)
    xx1 = ws.pop()
    xx2 = WeirdList(None, 4)
    print('#t5',len(ws) == 2, len(xx1) == 1, xx1 == xx2, xx1)
    ws.append(xx1)
    print('#t6',len(ws) == 3, ws[-1] == xx1)
    xx1 = ws.pop(0)
    xx2 = WeirdList(None, 2)
    print('#t7',len(ws) == 2, len(xx1) == 1, xx1 == xx2)
    print('---')
    print('---')
    #print(len(nums))

    for i in range(0, runs):
        tmp = WeirdList([])
        print(tmp.pp())
        print("++++++",i)
        for i in range(0, 3):
            x = (pos+1) % len(nums)
            tt = nums.pop(x)
            #print("+++", x, tt)
            tmp.append(tt)
            pos = nums.index(cur)
        if cur.start:
            num_ins = cur.start - 1
        else:
            print("_____",cur)
        #print(tmp.pp(), len(tmp))
        #tmp = WeirdList(tmp)
        while tmp.contains(num_ins) or num_ins < min_val:
            #while num_ins in tmp or num_ins < min_val:
            #if num_ins <
            #for k in tmp:
            #    if k.contains(num_ins):
            #        continue
            num_ins -= 1
            if num_ins < min_val:
                num_ins = max_val
        print(nums.pp(), cur, "@", pos, " after",num_ins)
        pos_ins = nums.index(num_ins)
        print(nums.pp(), cur, "@", pos, " at pos",pos_ins)
        print(tmp.pp(), len(tmp))


        print("=========")
        while len(tmp) > 0:
            item = tmp.pop()
            print("loop",item, item.pp(),"   ", tmp)
            nums.insert(pos_ins + 1, item)
            print('wah', len(nums), nums.pp())
        pos = (nums.index(cur) + 1) % len(nums)
        cur = nums[pos]

        print(pos, cur, nums.index(cur), len(nums))
        print(nums.pp())
        print(tmp.pp())
        #print()
        #print()
        print("=========")
    
    x = nums.index(1) + 1
    y = nums.index(1) + 2
    return (nums[x], nums[y], nums[x] * nums[y])


class WL():
    data = []
    positions = ()
    start_pos = 0
    tmp = []
    def __init__(self, data, start_pos=None):
        self.data = data
        if start_pos:
            self.start_pos = start_pos
    def get(self, n):
        if len(self.data) < 1:
            raise IndexError
        if n == 0:
            return self.data[0].get(n)
        last = 0
        for k in self.data:
            if last == 0:
                last = k
                continue
            if n < k.start_pos:
                return last.get(n)
            if n < k.end_pos():
                return k.get(n)
        raise IndexError
    def _rebal(self):
        data2 = []
        for i in range(0, len(self.data)):
            if len(self.data[i].tmp) == 0:
                data2.append(self.data[i])
            else:
                (lower, upper) = self.data[i].tmp
                if isinstance(lower, WLrun) and lower.start == lower.end:
                    lower = WLvec([lower.start], lower.start_pos)
                if lower:
                    data2.append(lower)
                if isinstance(upper, WLrun) and upper.start == upper.end:
                    upper = WLvec([upper.start], upper.start_pos)
                if upper:
                    data2.append(upper)
        self.data = data2
        print("___",len(self.data),self.data)
        print("___",self.dbg())
    def pop(self, n=None):
        if len(self.data) < 1:
            raise IndexError
        if n is None:
            item = self.data[-1].pop(n)
            self._rebal()
            return item
        last = 0
        for ki in range(0, len(self.data)):
            if last == 0:
                last = self.data[ki]
                continue
            if n < self.data[ki].start_pos:
                item = last.pop(n)
                self.data[ki].start_pos -= 1
                self._rebal()
                return item
            if n < self.data[ki].end_pos():
                item = self.data[ki].pop(n)
                if ki + 1 < len(self.data):
                    self.data[ki+1].start_pos -= 1
                self._rebal()
                return item
        raise IndexError
    def insert(self, pos, item):
        #print("_ins",pos,item,self.data[1].start_pos)
        #if pos > len(self.data):
        #    raise IndexError
        if len(self.data) < 1:
            self.data.append(item)
            return
        last = None
        for ki in range(0, len(self.data)):
            print("_insl",ki, self.data[ki].start_pos, self.data[ki].end_pos())
            if last is None:
                last = self.data[ki]
                continue
            if pos < self.data[ki].start_pos:
                offset = last.insert(pos, item)
                if offset > 0:
                    self.data[ki].start_pos += offset
                self._rebal()
                return
            if pos <= self.data[ki].end_pos():
                print("_innnn")
                offset = self.data[ki].insert(pos, item)
                if ki + 1 < len(self.data):
                    self.data[ki+1].start_pos += offset
                self._rebal()
                return
        raise IndexError
    def index(self, n):
        #print("_index",n)
        if len(self.data) < 1:
            return ValueError
        
        r = list(filter(lambda s: isinstance(s, WLrun), self.data))
        v = list(filter(lambda s: isinstance(s, WLvec), self.data))
        for k in r:
            #print("_indexr",n,k,k.start_pos)
            if n == k.end:
                return len(k) + k.start_pos - 1
            elif n == k.start:
                return k.start_pos
            elif k.start < n < k.end:
                return int((k.start + k.end) / 2 )
        for k in v:
            try:
                #print("_index",n,k)
                #for vv in k.items:
                #    print(vv)
                x = k.index(n)
                return x
            except ValueError:
                continue
        raise ValueError
    def __repr__(self):
        l = len(self.data)
        v = len(list(filter(lambda s: isinstance(s, WLvec), self.data)))
        return "WL<({}={}v+{}r)>".format(l,v,l-v)
    def __len__(self):
        rv = 0
        for k in self.data:
            rv += len(k)
        return rv
    def dbg(self):
        rv = ""
        return "|".join(map(lambda s: s.dbg(), self.data))

class WLrun(WL):
    start = None
    end = None
    def __init__(self, start, end, start_pos):
        self.start = start
        self.end = end
        self.start_pos = start_pos
    def get(self, n):
        n2 = n - self.start_pos
        return n2 + self.start
    def __repr__(self):
        return "WLrun<{}..{} ({})@{}>".format(self.start, self.end, len(self), self.start_pos)
    def end_pos(self):
        return self.start_pos + len(self)
    def __len__(self):
        return self.end - self.start + 1
    def pop(self, idx=None):
        if idx is None:
            last = self.end
            self.end -= 1
            return last
        elif idx == self.start_pos:
            first = self.start
            self.start += 1
            return first
        elif idx is not None:
            print("_popr", idx, self.start_pos, self.end_pos())
            if idx > self.end_pos() or idx < self.start_pos:
                raise IndexError
            num = idx - self.start_pos
            print("_",num)
            if self.start == self.start+num-1:
                lower = WLvec([self.start], self.start_pos)
            else:
                lower = WLrun(self.start, self.start+num-1, self.start_pos)
            print(lower.dbg())
            if self.start+num+1 > self.end:
                upper = None
            elif self.start+num+1 == self.end:
                upper = WLvec([self.end], self.start_pos + len(lower))
                print(upper.dbg())
            else:
                upper = WLrun(self.start+num+1, self.end, self.start_pos + len(lower))
                print(upper.dbg())
            self.tmp = [lower, upper]
            print(self.start + num)
            return self.start + num
        else:
            raise Exception
    def insert(self, pos, item):
        rv = 0
        if pos == self.start_pos:
            lower = WLvec([item], self.start_pos)
            self.start_pos += 1
            upper = WLrun(self.start, self.end, self.start_pos)
            rv = 1
        elif pos == self.end_pos():
            tmp_end = self.end
            self.end -= 1
            lower = WLrun(self.start, self.end, self.start_pos)
            upper = WLvec([item], self.end_pos())
            rv = 0
        else:
            npos = pos - self.start_pos
            lower = WLrun(self.start, self.start+npos-1, self.start_pos)
            upper = WLrun(self.start+npos+1, self.end, self.start_pos + len(lower))
            rv = 1
        print("_insr",pos, self.start_pos, self.end_pos())
        print("_insr2",lower.dbg(), upper.dbg())
        self.tmp = [lower, upper]
        self.start = 0
        self.end = 0
        return rv
    def dbg(self):
        return "[{}..{}]@{}".format(self.start, self.end,self.start_pos)

class WLvec(WL):
    items = []
    def __init__(self, items, start_pos=0):
        self.items = items
        self.start_pos = start_pos
    def get(self, n):
        return self.items[n-self.start_pos]
    def __repr__(self):
        if len(self.items) > 0:
            return "WLvec<{},.. ({})@{}>".format(self.items[0], len(self.items), self.start_pos)
        else:
            return "WLvec<.. (0)>"
    def end_pos(self):
        return self.start_pos + len(self.items)
    def __len__(self):
        return len(self.items)
    def pop(self, idx=None):
        print("_popv", idx, self.items, self.start_pos)
        if idx is not None and idx >= len(self) + self.start_pos:
            raise IndexError
        if idx is None:
            idx = len(self.items) - 1
        x = self.items.pop(idx - self.start_pos)
        return x
    def insert(self, pos, item):
        print("_insv",pos,item,len(self.items),self.items)
        if pos > len(self.items)+self.start_pos:
            raise IndexError
        elif pos == len(self.items):
            self.items.append(item)
        self.items.insert(pos, item)
        return 1
    def index(self, n):
        try:
            x = self.items.index(n)
            return x + self.start_pos
        except ValueError:
            raise ValueError
    def dbg(self):
        return ",".join(map(str, self.items))

def run13(nums, runs=100, max_num=20):
    pos = 0
    min_val = 1
    max_val = 9

    base = WLvec(nums, pos)
    rest = WLrun(max_val+1, max_num, 9)
    nums2 = WL([base, rest])

    print(nums)
    print(base)
    print(rest)
    print(nums2)
    cur = nums2.get(0)
    print(cur)
    #print(cur, nums2.get(8))
    #print(nums2.get(19))

    """
    base2 = WLvec(nums, pos)
    print("#t10",base2.pop(), len(base2), base2)
    print("#t11",base2.pop(0), len(base2), base2)
    print("#t12",base2.pop(3), len(base2), base2)
    rest2 = WLrun(max_val+1, max_num, 9)
    print("#t20",rest2.pop(), len(rest2), rest2, len(rest2.tmp))
    print("#t21",rest2.pop(9), len(rest2), rest2, len(rest2.tmp))
    rest2 = WLrun(max_val+1, max_num, 20)
    print("#t22",rest2.pop(23), len(rest2), rest2, len(rest2.tmp))
    """

    print("===================================")

    for i in range(0, runs):
        print("+++++++++++++++++",i)
        tmp = []
        npos = pos + 1
        for j in range(0, 3):
            x = (pos + 1) % len(nums2)
            #print(pos, x)
            print("POP",x)
            tmp.append(nums2.pop(x))
            pos = nums2.index(cur)
            #print(tmp, nums2, nums2.data[0])
            #break
        new_ins = cur - 1
        print("TMP",tmp, "cval",cur, "dval",new_ins)
        

        while new_ins in tmp or new_ins < min_val:
            new_ins -= 1
            if new_ins < min_val:
                new_ins = max_num
                break
        pos_ins = nums2.index(new_ins)
        print ("ni pi", new_ins, pos_ins)

        print("=========")
        while len(tmp) > 0:
            item = tmp.pop()
            print("loop", item, pos_ins)
            print("___ooo   ",nums2.dbg(), cur, "@", pos, "after", new_ins)
            nums2.insert(pos_ins + 1, item)
            print(nums2, len(nums2.data[0]))
            print("___ooo   ",nums2.dbg(), cur, "@", pos, "dval", pos_ins)

        #return
        pos = (nums2.index(cur) + 1) % len(nums2)
        cur = nums2.get(pos)
        #pos_ins = nums2.index(cur)
        print("___ooo   ",nums2.dbg(), "cval", cur, "@", pos, ">",len(nums2) )

def ppart1(lines):
    nums = []
    for c in lines[0]:
        nums.append(int(c))
    return run1(nums)

def ppart2(lines):
    nums = []
    for c in lines[0]:
        nums.append(int(c))
    mx = max(nums) + 1
    nums2 = nums.copy()
    while len(nums2) < 100:
        nums2.append(mx)
        mx +=1
    print(len(nums2))
    print("---")
    return run11(nums2, 10)
    return run13(nums, 10, 20)
    # run11
    # 20 nums, 1 run
    # [3, 2, 5, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] 3 @ 0
    # [8, 9, 1]
    # [3, 2, 8, 9, 1, 5, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    # [8, 9, 1]

    # [3, 2, 8, 9, 1, 5, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    # [3, 2, 5, 4, 6, 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 8, 9, 1]
    # [3, 4, 6, 7, 2, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 8, 9, 1]
    # [3, 4, 6, 7, 2, 5, 10, 14, 15, 16, 17, 18, 19, 20, 8, 9, 11, 12, 13, 1]
    # [3, 4, 6, 7, 2, 5, 10, 14, 18, 19, 20, 8, 9, 11, 12, 13, 15, 16, 17, 1]
    # [3, 4, 6, 7, 2, 5, 10, 14, 18, 9, 11, 12, 13, 15, 16, 17, 19, 20, 8, 1]
    # [3, 4, 6, 7, 2, 5, 10, 14, 18, 9, 15, 16, 17, 19, 20, 8, 11, 12, 13, 1]
    # [3, 4, 6, 7, 2, 5, 10, 14, 16, 17, 19, 18, 9, 15, 20, 8, 11, 12, 13, 1]
    # [3, 4, 6, 7, 2, 5, 10, 14, 16, 17, 19, 8, 11, 12, 18, 9, 15, 20, 13, 1]
    # [6, 7, 2, 5, 10, 14, 16, 17, 19, 8, 11, 12, 1, 3, 4, 18, 9, 15, 20, 13]


    # 20 nums, 10 runs
    # [6, 10, 16, 3, 4, 2, 5, 7, 9, 12, 13, 14, 1, 8, 11, 15, 17, 18, 20, 19]

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
