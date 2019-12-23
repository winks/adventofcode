function dist(a, b)
	return sqrt( (a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2]) )
end

function sub(a,b)
	return (a[1] - b[1], a[2] - b[2])
end

function angle2(a, b)
	return atan(b[2] - a[2], b[1] - a[1])
end

function part1(coord, pairs)
	rv = []
	for t in pairs
		u1 = sub(t[2], coord)
		x = angle2((0,0), u1)
		md = rad2deg(x)
		if !(md in rv)
			append!(rv, md)
		end
	end
	return rv
end

function part2(coord, pairs)
	rv = []
	for t in pairs
		u1 = sub(t[2], coord)
		x = angle2(coord, t[2])
		md = rad2deg(x)
		push!(rv, (t[2][1], t[2][2], md))
	end
	return rv
end

function los1(m)
	rv = []
	for y in 1:length(m)
		for x in 1:length(m[y])
			if m[y][x] == '.'
				continue
			end
			ck = []
			for y1 in 1:length(m)
				for x1 in 1:length(m[y])
					if m[y1][x1] == '.'
						continue
					end
					if x == x1 && y == y1
						continue
					end
					push!(ck, ((x,y),(x1,y1)))
				end
			end
			angles = part1((x,y), ck)
			push!(rv, (x,y,length(angles)))
		end
	end
	mx = 0
	bs = (0,0)
	for r in rv
		if r[3] > mx
			bs = (r[1], r[2])
			mx = r[3]
		end
	end
	println()
	println("Part 1: ($(bs[1]-1),$(bs[2]-1)) :: $(mx)")
	println()
	return bs
end

function h(x, bs, lang)
	return (((x[3] - lang) % 360) * 1000  + dist(bs, x))
end

function mmin(aa, bs, lang)
	mm = 999999999
	rv = (1,2,3)
	rx = 0
	idx = 1
	for a in aa
		hx = abs(h(a, bs, lang))
		println("MM ",a," ",bs," ",lang," = ",hx)
		if hx < mm
			mm = hx
			rv = a
			rx = idx
		end
		idx += 1
	end
	return (rv, rx)
end

function los2(m, bs)
	ck = []
	for y1 in 1:length(m)
		for x1 in 1:length(m[y1])
			if m[y1][x1] == '.'
				continue
			end
			if y1 == bs[2] && x1 == bs[1]
				continue
			end
			push!(ck, ((0,0),(x1,y1)))
		end
	end
	aa = part2(bs, ck)
	for i in 1:length(aa)
		aa[i] = (aa[i][1], aa[i][2], (aa[i][3] + 90 + 360) % 360)
	end
	for a in aa
		println(a," ",a[3] * 1000 + dist(bs, a))
	end
	println(length(aa), aa[1])
	shot = []
	lang = 0
	print("aa: ")
	print(length(aa))
	print(" shot: ")
	println(length(shot))
	println("----")

	tgt = (0,0,0)
	lang = 0
	while true
		if length(aa) < 1
			break
		end
		(tgt,idx) = mmin(aa, bs, lang)
		hx = h(tgt, bs, lang)
		println("Target: ",tgt," ",hx ," l ", lang)
		aa = deleteat!(aa, idx)
		push!(shot, tgt)
		lang = (hx + 0.001) % 360
		println("aa:", length(aa), " shot: ", length(shot), " last: ", tgt, " lang: ", lang)
		println()
	end
	println("Part 2: (", tgt[1]-1,"/",tgt[2]-1,") :: ", (tgt[1]-1)*100 + (tgt[2]-1))
end


filename = "../input/day10/part1"

if length(ARGS) > 0
	filename = ARGS[1]
end

println("File: $(filename)")
am = readlines(filename)
bs = los1(am)
los2(am, bs)
