-- Lua 5.2 // Luajit 2.1.0-beta2

function getl(file)
	lines = {}
	for line in io.lines(file) do
		lines[#lines+1] = line
	end
	return lines
end

function gcd( m, n )
	while n ~= 0 do
		local q = m
		m = n
		n = q % n
	end
	return m
end

function lcm( m, n )
	return ( m ~= 0 and n ~= 0 ) and m * n / gcd( m, n ) or 0
end

function deepcopy2(t)
	local t2 = {};
	for k,v in pairs(t) do
		if type(v) == "table" then
			t2[k] = deepcopy2(v);
		else
			t2[k] = v;
		end
	end
	return t2;
end

function rpad(s,l,c)
	local res = s .. string.rep(c or ' ', l - #s)
	return res, res ~= s
end

function strx(v)
	local sz = 5
	return	'! '       .. rpad(v.name, 10) ..
			' // x: '  .. rpad(''..v.x, sz) ..
			' / y: '   .. rpad(''..v.y, sz) ..
			' / z: '   .. rpad(''..v.z, sz) ..
			' // vx: ' .. rpad(''..v.vx,sz) ..
			' / vy: '  .. rpad(''..v.vy,sz) ..
			' / vz: '  .. rpad(''..v.vz,sz)
end

function ppm(t)
	for k,v in ipairs(t) do
		print(strx(v))
	end
end

function parse(line)
	x,y,z = string.match(line, '^<x=([^,]+),.*y=([^,]+),.*z=([^,]+)>')
	return tonumber(x),tonumber(y),tonumber(z)
end

function calcvelo(moons)
	for k,m in ipairs(moons) do
		moons[k].x = moons[k].x + moons[k].vx
		moons[k].y = moons[k].y + moons[k].vy
		moons[k].z = moons[k].z + moons[k].vz
	end
	return moons
end

function calcgrav(moons)
	for k1,_ in ipairs(moons) do
		for k2,_ in ipairs(moons) do
			if k2 <= k1 then goto continue end
			if moons[k1].z < moons[k2].z then
				moons[k1].vz = moons[k1].vz + 1
				moons[k2].vz = moons[k2].vz - 1
			elseif moons[k1].z > moons[k2].z then
				moons[k1].vz = moons[k1].vz - 1
				moons[k2].vz = moons[k2].vz + 1
			end
			if moons[k1].x < moons[k2].x then
				moons[k1].vx = moons[k1].vx + 1
				moons[k2].vx = moons[k2].vx - 1
			elseif moons[k1].x > moons[k2].x then
				moons[k1].vx = moons[k1].vx - 1
				moons[k2].vx = moons[k2].vx + 1
			end
			if moons[k1].y < moons[k2].y then
				moons[k1].vy = moons[k1].vy + 1
				moons[k2].vy = moons[k2].vy - 1
			elseif moons[k1].y > moons[k2].y then
				moons[k1].vy = moons[k1].vy - 1
				moons[k2].vy = moons[k2].vy + 1
			end
			::continue::
		end
	end
	return moons
end

function calcvelo2(moons, what, vel)
	for k,_ in ipairs(moons) do
		moons[k][what] = moons[k][what] + moons[k][vel]
	end
	return moons
end

function calcgrav2(moons, what, vel)
	for k1,_ in ipairs(moons) do
		for k2,_ in ipairs(moons) do
			if k2 <= k1 then goto continue end
			if moons[k1][what] < moons[k2][what] then
				moons[k1][vel] = moons[k1][vel] + 1
				moons[k2][vel] = moons[k2][vel] - 1
			elseif moons[k1][what] > moons[k2][what] then
				moons[k1][vel] = moons[k1][vel] - 1
				moons[k2][vel] = moons[k2][vel] + 1
			end
			::continue::
		end
	end
	return moons
end

function calcenergy(moons)
	local total = 0
	for k,v in ipairs(moons) do
		local t = 0
		local pt = 0
		local kt = 0
		pt = pt + math.abs(v.x) + math.abs(v.y) + math.abs(v.z)
		kt = kt + math.abs(v.vx) + math.abs(v.vy) + math.abs(v.vz)
		t = pt * kt
		print(pt,kt,t)
		total = total + t
	end
	return total
end

function rpart1(moons)
	print('---------------- part1')
	local len = 1000
	local steps = 0
	for i=1,len,1 do
		moons = calcgrav2(moons, 'x', 'vx')
		moons = calcgrav2(moons, 'y', 'vy')
		moons = calcgrav2(moons, 'z', 'vz')

		moons = calcvelo2(moons, 'x', 'vx')
		moons = calcvelo2(moons, 'y', 'vy')
		moons = calcvelo2(moons, 'z', 'vz')
		steps = i
	end
	print('----------------' .. steps .. ' steps done')
	ppm(moons)
	local e = calcenergy(moons)
	print(e)
	print('---------------- part1')
end

function rpart2(moons, what)
	print('---------------- part2')
	local state0 = deepcopy2(moons)
	local szt = #state0
	ppm(state0)
	print(szt .. " moons")
	local len = 0
	len = 4686774924 + 10

	----- .  .  .
	local ok = 0
	print('---------------- part2 loop: ' .. len .. " " .. what)
	local what2 = 'v' .. what
	for i=1,len,1 do
		moons = calcgrav(moons)
		moons = calcvelo(moons)

		local m = 0
		for xk,_ in ipairs(state0) do
			if moons[xk][what] == state0[xk][what] and
				moons[xk][what2] == 0 and
				moons[xk][what2] == 0 and
				moons[xk][what2] == 0 then
				m = m + 1
			else
				goto continue
			end
		end
		if m == szt then
			ok = i
			goto breaks
		end
		::continue::
		if math.fmod(i,10000000) == 0 then print(':: ' .. i) end
	end
	::breaks::
	print(what .. ' : ' .. ok)
	print('---------------- part2')
	return ok
end

function main()
	if #arg < 1 then
		return 1
	end
	local fname = arg[1]
	local part2 = nil
	local what = nil
	if #arg > 1 then
		part2 = arg[2]
	end
	if #arg > 2 then
		what = arg[3]
	end

	local lines = getl(fname)
	local moons = {}
	moons[#moons+1] = { name = 'Io' }
	moons[#moons+1] = { name = 'Europa' }
	moons[#moons+1] = { name = 'Ganymede' }
	moons[#moons+1] = { name = 'Callisto' }
	if #lines ~= #moons then
		return 2
	end

	for i,m in pairs(moons) do
		x0,y0,z0 = parse(lines[i])
		m.x = x0
		m.y = y0
		m.z = z0
		m.vx = 0
		m.vy = 0
		m.vz = 0
	end
	ppm(moons)
	print('---------------- initialized')


	if not part2 then
		rpart1(moons)
	else
		if what then
			local xxx = rpart2(deepcopy2(moons), what)
			print(xxx)
		else
			local x2 = rpart2(deepcopy2(moons), "x")
			local y2 = rpart2(deepcopy2(moons), "y")
			local z2 = rpart2(deepcopy2(moons), "z")
			local pp1 = lcm(x2,y2)
			local pp2 = lcm(pp1, z2)
			print(string.format("%18.0f",pp2))
		end
	end
end

main()
