import sys

def adj(x, y, lines):
	r = []
	if y > 0:
		r.append(lines[y-1][x].strip())
	if x < len(lines[0])-1:
		r.append(lines[y][x+1].strip())
	if x > 0:
		r.append(lines[y][x-1].strip())
	if y < len(lines)-1:
		r.append(lines[y+1][x].strip())
	return r

def adj2(x, y, lines):
	r = [(x,y)]
	x0 = x
	y0 = y
	while y > 0:
		nxt = int(lines[y-1][x])
		y -= 1
		if nxt < 9:
			p = (x, y)
			r.append(p)
		else:
			break
	y = y0
	x = x0
	while x < len(lines[0])-1:
		nxt = int(lines[y][x+1])
		x += 1
		if nxt < 9:
			p = (x, y)
			r.append(p)
		else:
			break
	y = y0
	x = x0
	while x > 0:
		nxt = int(lines[y][x-1])
		x -= 1
		if nxt < 9:
			p = (x, y)
			r.append(p)
		else:
			break
	y = y0
	x = x0
	while y < len(lines)-1:
		nxt = int(lines[y+1][x])
		y += 1
		if nxt < 9:
			p = (x, y)
			r.append(p)
		else:
			break
	return r


with open(sys.argv[1], "r") as f:
	lines = f.readlines()
	lines2 = []
	for li in lines:
		lines2.append(li.strip())
	lines = lines2
	rv = []
	l2 = []
	for y in range(len(lines)):
		for x in range(len(lines[0])):
			p = int(lines[y][x])
			ad = adj(x, y, lines)
			low = True
			for a in ad:
				if p >= int(a):
					low = False
			if low:
				rv.append(p+1)
				l2.append((x, y))
	print("p1", sum(rv))
	rv2 = []
	for p2 in l2:
		ad2 = []
		todo = [p2]
		while len(todo) > 0:
			d = todo.pop()
			ad3 = adj2(d[0], d[1], lines)
			for x in ad3:
				if x not in todo and x not in ad2:
					todo.append(x)
			for x in ad3:
				if x not in ad2:
					ad2.append(x)
		rv2.append(len(ad2))
	s = sorted(rv2)[-3:]
	print("p2", s[0] * s[1] * s[2])
