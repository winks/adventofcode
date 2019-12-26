# Julia 1.3.0

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
	return (bs, mx)
end

function m(x, bs, lang)
	rv = ((((x[3] - lang) % 360) + 360) % 360) * 1000 + dist(bs, x)
	#println("    m(",x," ",bs," ",lang," ",dist(bs,x),")=",rv)
	return rv
end

function los2(mm, bs)
	ck = []
	for y1 in 1:length(mm)
		for x1 in 1:length(mm[y1])
			if mm[y1][x1] == '.'
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
	for a in sort(aa)
		#println(a," ",a[3] * 10000 + dist(bs, a))
	end
	shot = []
	lang = 0
	println("left: ",length(aa)," shot: ",length(shot))
	println()

	tgt = (0,0,0)
	lang = 0
	while true
		if length(aa) < 1
			break
		end
		if length(shot) >= 200
			break
		end
		tmpa = sort(aa, by = x -> m(x, bs, lang))
		tgt = tmpa[1]
		idx = 1
		hx = m(tgt, bs, lang)
		println("Target: (",tgt[1],", ",tgt[2],", ",tgt[3],") m: ",hx ," l: ", lang)
		aa = deleteat!(tmpa, idx)
		push!(shot, tgt)
		lang = (tgt[3] + 0.001) % 360
		println("left: ", length(aa), " shot: ", length(shot), " last: ", tgt, " lang: ", lang)
		println()
	end
	println("Part 2: (", tgt[1]-1,"/",tgt[2]-1,") :: ", (tgt[1]-1)*100 + (tgt[2]-1))
	return tgt
end

filename = "../input/day10/part1"

if length(ARGS) > 0
	filename = ARGS[1]
end

println("File: $(filename)")
am = readlines(filename)
(bs, mx) = los1(am)
tgt = los2(am, bs)
println("---")
println("Part 1: ($(bs[1]-1),$(bs[2]-1)) :: $(mx)")
println("Part 2: (", tgt[1]-1,"/",tgt[2]-1,") :: ", (tgt[1]-1)*100 + (tgt[2]-1))
