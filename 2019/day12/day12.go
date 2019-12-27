// go 1.13.5

package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

type moon struct {
	name string
	x    int
	y    int
	z    int
	vx   int
	vy   int
	vz   int
}

func NewMoon(name string) *moon {
	moon := moon{name: name}
	return &moon
}

func gcd(m int, n int) int {
	for {
		if n == 0 {
			break
		}
		q := m
		m = n
		n = q % n
	}
	return m
}

func lcm(m int, n int) int {
	if m == 0 || n == 0 {
		return 0
	}
	return m * n / gcd(m, n)
}

func parse(line string) (int, int, int) {
	r, err := regexp.Compile("^<x=(?P<x>[^,]+),.*y=(?P<y>[^,]+),.*z=(?P<z>[^,]+)>")
	check(err)

	match := r.FindStringSubmatch(line)
	x := 0
	y := 0
	z := 0
	if len(match) != 4 {
		return x, y, z
	}
	x, err = strconv.Atoi(match[1])
	check(err)
	y, err = strconv.Atoi(match[2])
	check(err)
	z, err = strconv.Atoi(match[3])
	check(err)

	return x, y, z
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func calcenergy(moons []moon) int {
	total := 0
	for _, m := range moons {
		pt := Abs(m.x) + Abs(m.y) + Abs(m.z)
		kt := Abs(m.vx) + Abs(m.vy) + Abs(m.vz)
		total += (pt * kt)
	}
	return total
}

func calcgrav(moons []moon, what string) []moon {
	for i1, _ := range moons {
		for i2, _ := range moons {
			if i2 <= i1 {
				continue
			}
			if what == "x" {
				if moons[i1].x < moons[i2].x {
					moons[i1].vx++
					moons[i2].vx--
				} else if moons[i1].x > moons[i2].x {
					moons[i2].vx++
					moons[i1].vx--
				}
			} else if what == "y" {
				if moons[i1].y < moons[i2].y {
					moons[i1].vy++
					moons[i2].vy--
				} else if moons[i1].y > moons[i2].y {
					moons[i2].vy++
					moons[i1].vy--
				}
			} else {
				if moons[i1].z < moons[i2].z {
					moons[i1].vz++
					moons[i2].vz--
				} else if moons[i1].z > moons[i2].z {
					moons[i2].vz++
					moons[i1].vz--
				}
			}
		}
	}
	return moons
}

func calcvelo(moons []moon, what string) []moon {
	for i, _ := range moons {
		if what == "x" {
			moons[i].x = moons[i].x + moons[i].vx
		} else if what == "y" {
			moons[i].y = moons[i].y + moons[i].vy
		} else {
			moons[i].z = moons[i].z + moons[i].vz
		}
	}
	return moons
}

func part1(omoons []moon, loops int) int {
	moons := make([]moon, len(omoons))
	copy(moons, omoons)
	steps := -1
	for i := 0; i < loops; i++ {
		moons = calcgrav(moons, "x")
		moons = calcgrav(moons, "y")
		moons = calcgrav(moons, "z")

		moons = calcvelo(moons, "x")
		moons = calcvelo(moons, "y")
		moons = calcvelo(moons, "z")
		steps = i
	}
	fmt.Printf("Steps done: %v \n", steps+1)
	fmt.Printf("Moons :\n %v\n", moons)
	fmt.Printf("Part 1:\n %v\n", calcenergy(moons))
	return calcenergy(moons)
}

func part2(moons []moon, what string) int {
	state0 := make([]moon, len(moons))
	copy(state0, moons)
	loops := 4686774924 + 10
	sz := len(moons)
	ok := 0
	for i := 0; i < loops; i++ {
		moons = calcgrav(moons, what)
		moons = calcvelo(moons, what)
		m := 0
		for k := 0; k < sz; k++ {
			if what == "x" {
				if moons[k].x != state0[k].x || moons[k].vx != 0 || moons[k].vy != 0 || moons[k].vz != 0 {
					continue
				}
				m++
			} else if what == "y" {
				if moons[k].y != state0[k].y || moons[k].vy != 0 {
					continue
				}
				m++
			} else {
				if moons[k].z != state0[k].z || moons[k].vz != 0 {
					continue
				}
				m++
			}
		}
		if m == sz {
			ok = i + 1
			break
		}
	}
	return ok
}

func main() {
	argv := os.Args
	if len(argv) < 2 {
		fmt.Printf("Usage: %v /path/to/file\n", argv[0])
		return
	}
	steps := 1000
	if len(argv) > 2 {
		stx, err := strconv.Atoi(argv[2])
		if err == nil {
			steps = stx
		}
	}
	filename := argv[1]
	fh, err := os.OpenFile(filename, os.O_RDONLY, os.ModePerm)
	check(err)
	defer fh.Close()

	lines := make([]string, 0)
	sc := bufio.NewScanner(fh)
	for sc.Scan() {
		line := sc.Text()
		lines = append(lines, line)
	}
	check(sc.Err())
	fmt.Printf("> %s\n", lines)

	moons := make([]moon, 0)
	//m := NewMoon("Io")
	moons = append(moons, *NewMoon("Io"))
	moons = append(moons, *NewMoon("Europa"))
	moons = append(moons, *NewMoon("Ganymede"))
	moons = append(moons, *NewMoon("Callisto"))

	for i, _ := range moons {
		//fmt.Printf("> %s\n", lines[i])
		x0, y0, z0 := parse(lines[i])
		moons[i].x = x0
		moons[i].y = y0
		moons[i].z = z0
	}

	fmt.Printf("Moons:\n %v\n-------------------------------\n", moons)
	e1 := part1(moons, steps)
	//fmt.Printf("------------------------------- %d\n", steps)

	p2x := part2(moons, "x")
	fmt.Printf("x %d\n", p2x)
	p2y := part2(moons, "y")
	fmt.Printf("y %d\n", p2y)
	p2z := part2(moons, "z")
	fmt.Printf("z %d\n", p2z)
	pp1 := lcm(p2x, p2y)
	pp2 := lcm(pp1, p2z)
	fmt.Printf("Part 1: %d\n", e1)
	fmt.Printf("Part 2: %d\n", pp2)

}
