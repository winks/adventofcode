#!/usr/bin/env ruby2.5
def readf(fn)
  text = File.open(fn).read
  text.gsub!(/\r\n?/, "\n")
  text.each_line do |line|
    return line.strip!()
  end
end

def splitn(x)
  rv = []
  for i in 0..x.length-1 do
    rv.push(x[i].to_i)
  end
  return rv
end

def mul(x,y,rep=1)
  rv = []
  y2 = []
  for i in 0..(x.length+rep) do
    k = i%y.length
    v = y[k]
    for ii in 0..(rep-1) do
      y2.push y[i%y.length]
    end
  end
  y2 = y2.drop(1)
  for i in 0..(x.length-1) do
    b = y2[i]
    r = (x[i] * b) #% 10
    rv.push r
  end
  rv = rv.inject(0, :+)
  return (rv.abs) % 10
end

def phase(nums,base)
  rv = []
  for i in 0..nums.length-1 do
    r = mul(nums, base,i+1)
    rv.push r
  end
  return rv
end

def part2(nruns, line)
  puts "> #{nruns} phases, part 2"

  offset = line[0..6].to_i
  input = line * 10000
  input = input[offset..-1]
  nums = splitn input
  len = nums.length

  rv0 = []
  for x in 0..len do
    rv0[x] = 0
  end
  for p in 0..nruns-1 do
    rv = rv0

    for i in (len-1).downto(0) do
      rv[i] = (input[i].to_i + rv[i+1]) % 10
    end
    input = rv
    #puts "run #{p} done"
    #puts rv[0..19].join("")
    #puts rv[-20..-1].join("")
  end

  puts "> Part 2:"
  puts input[0..7].join("")

end

def part1(nruns, line)
  puts "> #{nruns} phases, part 1"

  nums = splitn line
  base = [0,1,0,-1]
  rv = nums
  dbg = ""
  for i in 0..(nruns-1) do
    rv = phase(rv, base)
    tx = rv.join " "
    dbg = dbg + "old: After phase #{i+1} : #{tx}\n"
  end
  #puts dbg
  #puts rv.length
  puts "> Part 1:"
  puts rv.slice(0,8).join("")

end

def main
  if ARGV.length < 2
    exit
  end
  fn = ARGV[0]
  nruns = ARGV[1].to_i
  line = readf(fn)
  puts "> #{line}"

  if ARGV[2].to_i == 2
   part2(nruns, line)
  else
    part1(nruns, line)
  end
end

main
