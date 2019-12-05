# crystal-lang

class Calc
  def initialize()
    @numbers = Array(Int32).new
  end

  def read(name : String)
    fh = File.open(name)
    puts "reading from '#{name}' : #{fh}"

    fh.each_line do |line|
      @numbers.push(line.to_i32)
    end
    puts "Read #{@numbers.size} items."
  end

  def run()
    total = 0
    total2 = 0
    @numbers.each do |n|
      fuel = calc(n)
      total += fuel
      fuelfuel = fuel
      while (fuelfuel > 0)
        fuelfuel = calc(fuelfuel.to_i)
        total2 += fuelfuel if (fuelfuel > 0)
      end
    end
    t3 = total + total2
    puts "Total: #{total} + #{total2} = #{t3}"
  end

  def calc(mass : Int32)
    n1 = mass / 3.0
    n2 = n1.floor
    return n2 - 2
  end
end

name = "input/day5"
c = Calc.new
c.read(name)
c.run()
