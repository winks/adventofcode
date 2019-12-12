function getl(file)
  lines = {}
  for line in io.lines(file) do
    lines[#lines+1] = line
  end
  return lines
end

function pp(t) end

function rpad(s,l,c)
	local res = s .. string.rep(c or ' ', l - #s)
	return res, res ~= s
end

function strx(v)
	local sz = 5
	return "! " .. rpad(v.name, 10) ..
	' //  x:' .. rpad(''..v.x, sz) .. 
	" /  y: " .. rpad(''..v.y, sz) .. 
	" /  z: " .. rpad(''..v.z, sz) ..
	' // vx:' .. rpad(''..v.vx,sz) .. 
	" / vy: " .. rpad(''..v.vy,sz) .. 
	" / vz: " .. rpad(''..v.vz,sz)
end

function world(t)
	local rv = "=== WORLD\n"
	for k,v in ipairs(t) do
		rv = rv .. strx(v) .. "\n"
	end
	return rv .. "WORLD ==="
end

function fnd(s, t)
	for i,v in ipairs(t) do
		if s == v then return i end
	end
	return 0
end

function ppm(t)
	for k,v in ipairs(t) do
		print(strx(v))
	end
end

function parse(line)
	x,y,z = string.match(line, "^<x=([^,]+),.*y=([^,]+),.*z=([^,]+)>")
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
	moons[#moons+1] = { name = "Io" }
	moons[#moons+1] = { name = "Europa" }
	moons[#moons+1] = { name = "Ganymede" }
	moons[#moons+1] = { name = "Callisto" }
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
	print("---------------- initialized")
	

	if not part2 then
		print("---------------- part1")
		local steps = 0
		local len = 1000
		for i=1,len,1 do
			moons = calcgrav(moons)
			moons = calcvelo(moons)
			steps = steps + 1
			print("----------------" .. steps .. " steps done")
		end
		ppm(moons)
		e = calcenergy(moons)
		print(e)
		print("---------------- part1")
	else
		print("---------------- part2")
		local history = {}
		local history_x = {}
		local history_y = {}
		history[#history+1] = world(moons)
		history_x[#history_x+1] = moons[1].x
		history_y[#history_y+1] = moons[1].y
		steps = 0
		len = 10000000
		for i=1,len,1 do
			moons = calcgrav(moons)
			moons = calcvelo(moons)
			steps = steps + 1
			w = world(moons)
			f1 = fnd(w, history)
			if f1 > 0 then
				print('found:' .. i .. ' ' .. f1)
				break
			end
			history[#history+1] = w
			history_x[#history_x+1] = moons[1].x
			history_y[#history_y+1] = moons[1].y
			--print(#history)
			if math.fmod(i,10000) == 0 then print(":: " .. i) end
		end
		print('len: ' .. #history)
		--print(history[1])
		for x,y in ipairs(history) do
			if x > 2770 and x < 2774 then
				--print(x)
				--print(y)
			end
		end
		print("---------------- part2")
	end
end


main()
