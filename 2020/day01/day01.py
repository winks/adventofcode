import sys

fname = '../input/day01/input.txt'

part1 = True
if len(sys.argv) > 1 and sys.argv[1] == '2':
    part1 = False

with open(fname, "r") as t1:

    if part1:
        t1 = t1.readlines()
        t2 = t1
        for line1 in t1:
            line1 = int(line1.strip())
            for line2 in t2:
                line2 = int(line2.strip())
                if line1 + line2 == 2020:
                    print(line1,line2,line1+line2,line1*line2)
                    break
            else:
                continue
            break
        sys.exit(0)

    # part 2
    t1 = t1.readlines()
    t2 = t1
    t3 = t1
    for line1 in t1:
        line1 = int(line1.strip())
        for line2 in t2:
            line2 = int(line2.strip())
            for line3 in t3:
                line3 = int(line3.strip())
                if line1 + line2 + line3 == 2020:
                    print(line1,line2,line3,line1+line2+line3,line1*line2*line3)
                    sys.exit(0)
