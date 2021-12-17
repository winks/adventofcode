import sys

def step(s):
	vx = ( (s[2] + 1, 0)[ s[2] < 0 ] , s[2] - 1)[ s[2] > 0 ]
	return [ s[0] + s[2], s[1] - s[3], vx , s[3] - 1 ]

def run(s, xs, ys):
	best = 0
	while True:
		s = step(s)
		if s[1] < best:
			best = s[1]
		if s[1] > ys[1] or s[0] > xs[1]:
			return 0, True
		if ys[0] <= s[1] <= ys[1] and xs[0] <= s[0] <= xs[1]:
			return best, False

with open(sys.argv[1], "r") as f:
	parts = list(map(lambda a:          a.replace(',',  ''),  f.readlines()[0].strip().split(' ')))
	xs =    list(map(lambda a:      int(a.replace('x=', '')), parts[2].split('..')))
	ys =    list(map(lambda a: -1 * int(a.replace('y=', '')), parts[3].split('..')))
	best = 99
	total = 0
	runs = 310
	for vx in range(-1 * runs, runs+1):
		for vy in range(-1 * runs, runs+1):
			(r, err) = run([0, 0, vx, vy], [min(xs), max(xs)], [min(ys), max(ys)])
			if not err:
				total += 1
				if r < best:
					best = r
	print(-1*best, total)