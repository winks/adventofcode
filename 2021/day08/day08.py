import sys

def c(x, sets):
	if len(x) == 2:
		return 1
	elif len(x) == 3:
		return 7
	elif len(x) == 4:
		return 4
	elif len(x) == 7:
		return 8
	elif len(x) == 6:
		# 6,9,0
		s = set(x).symmetric_difference(sets[4])
		if len(s) == 2:
			return 9
		else:
			s2 = sets[4].symmetric_difference(sets[1])
			s3 = set(x).symmetric_difference(s2)
			if len(s3) == 4:
				return 6
			else:
				return 0
	elif len(x) == 5:
		# 2,5,3
		s = set(x).symmetric_difference(sets[1])
		if len(s) == 3:
			return 3
		else:
			s2 = sets[4].symmetric_difference(sets[1])
			s3 = set(x).symmetric_difference(s2)
			if len(s3) == 3:
				return 5
			else:
				return 2

with open(sys.argv[1], "r") as f:
	lines = f.readlines()
	p1 = 0
	p2 = 0
	for line in lines:
		p = line.split("|")
		for n in p[1].strip().split(" "):
			n = n.strip()
			if len(n) == 2 or len(n) == 3 or len(n) == 4 or len(n) == 7:
				p1 += 1
	print("Part 1:", p1)
	for line in lines:
		p = line.split("|")
		sets = {1: None}
		for n in p[0].strip().split(" "):
			n = n.strip()
			if len(n) == 2:
				sets[1] = set(n)
			elif len(n) == 3:
				sets[7] = set(n)
			elif len(n) == 4:
				sets[4] = set(n)
			elif len(n) == 7:
				sets[8] = set(n)
		rvc = ""
		for n in p[1].strip().split(" "):
			rvc += str(c(n, sets))
		p2 += int(rvc)
	print("Part 2:", p2)