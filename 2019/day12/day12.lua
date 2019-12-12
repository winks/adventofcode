function getl(file)
  lines = {}
  for line in io.lines(file) do
    lines[#lines+1] = line
  end
  return lines
end

function deepcopy(orig)
    local orig_type = type(orig)
    local copy
    if orig_type == 'table' then
        copy = {}
        for orig_key, orig_value in next, orig, nil do
            copy[deepcopy(orig_key)] = deepcopy(orig_value)
        end
        setmetatable(copy, deepcopy(getmetatable(orig)))
    else -- number, string, boolean, etc
        copy = orig
    end
    return copy
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

function world(t)
	local rv = '=== WORLD\n'
	for k,v in ipairs(t) do
		rv = rv .. strx(v) .. "\n"
	end
	return rv .. 'WORLD ==='
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

function main()
	if #arg < 1 then
		return 1
	end
	local fname = arg[1]
	local part2 = nil
	if #arg > 1 then
		part2 = arg[2]
	end

	lines = getl(fname)
	moons = {}
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
		e = calcenergy(moons)
		print(e)
		print('---------------- part1')
	else
		print('---------------- part2')
		state0 = deepcopy(moons)
		ppm(state0)
		local history = {}
		len = 100000
		len = 4686774924 + 10
		len = 5000000000
		----- .  .  .
		local okx = {}
		local oky = {}
		local okz = {}
		print('---------------- part2 loop: ' .. len)
		local szt = #state0
		for i=1,len,1 do
			moons = calcgrav2(moons, 'x', 'vx')
			moons = calcvelo2(moons, 'x', 'vx')
			local m = 0
			for xk,_ in ipairs(state0) do
				if moons[xk].x ~= state0[xk].x then
					goto cont1
				else
					m = m + 1
				end
				:: cont1 ::
			end
			if m == szt then okx[#okx+1] = i end
		end
		for _,i in ipairs(okx) do
			moons = calcgrav2(moons, 'y', 'vy')
			moons = calcvelo2(moons, 'y', 'vy')
			local m = 0
			for xk,_ in ipairs(state0) do
				if moons[xk].y ~= state0[xk].y then
					goto cont2
				else
					m = m + 1
				end
				:: cont2 ::
			end
			if m == szt then oky[#oky+1] = i end
		end
		for _,i in ipairs(oky) do
			moons = calcgrav2(moons, 'z', 'vz')
			moons = calcvelo2(moons, 'z', 'vz')
			local m = 0
			for xk,_ in ipairs(state0) do
				if moons[xk].z ~= state0[xk].z then
					goto cont3
				else
					m = m + 1
				end
				:: cont3 ::
			end
			if m == szt then okz[#okz+1] = i end
		end
		--[[
			if math.fmod(i,1000) == 0 then print(':: ' .. i) end
		]]--
		print('len: ' .. #okx)
		print('len: ' .. #oky)
		print('len: ' .. #okz)
		for k,x in ipairs(okz) do
			print(x)
		end
		print('---------------- part2')
	end
end

main()
