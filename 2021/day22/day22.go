package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type Cube struct {
	x, y, z int
	on      bool
}

type Mega struct {
	x1, x2 int
	y1, y2 int
	z1, z2 int
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func getLines(filename string) []string {
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
	return lines
}

func cc(c map[int]map[int]map[int]bool) int {
	rv := 0
	for z := range c {
		for y := range c[z] {
			for x := range c[z][y] {
				if c[z][y][x] {
					rv++
				}
			}
		}
	}
	return rv
}

func part1(lines []string) int {
	others := []Mega{}
	size := 50
	mag := 0
	world := make(map[int]map[int]map[int]bool, 0)
	for z := -1 * size; z <= size; z++ {
		world[z] = make(map[int]map[int]bool, 0)
		for y := -1 * size; y <= size; y++ {
			world[z][y] = make(map[int]bool, 0)
			for x := -1 * size; x <= size; x++ {
				mag++
				world[z][y][x] = false
			}
		}
	}
	fmt.Printf("count %v..%v: %v/%v\n", -1*size, size, cc(world), mag)
	fmt.Printf("others: %v\n", len(others))

	for _, line := range lines {
		st_coord := strings.Split(line, " ")
		coord := strings.Split(st_coord[1], ",")
		xs := strings.Split(coord[0], "..")
		ys := strings.Split(coord[1], "..")
		zs := strings.Split(coord[2], "..")
		x1, err := strconv.Atoi(string(xs[0][2:]))
		check(err)
		x2, err := strconv.Atoi(xs[1])
		check(err)
		y1, err := strconv.Atoi(string(ys[0][2:]))
		check(err)
		y2, err := strconv.Atoi(ys[1])
		check(err)
		z1, err := strconv.Atoi(string(zs[0][2:]))
		check(err)
		z2, err := strconv.Atoi(zs[1])
		check(err)
		on := false
		if st_coord[0] == "on" {
			on = true
		}
		if x2 < x1 {
			x1, x2 = x2, x1
		}
		if y2 < y1 {
			y1, y2 = y2, y1
		}
		if z2 < z1 {
			z1, z2 = z2, z1
		}

		//fmt.Printf("Parsed: %v, x[%v %v] y[%v %v] z[%v %v]\n", on, x1, x2, y1, y2, z1, z2)
		if x1 < -100 || x1 > 100 || y1 < -100 || y1 > 100 || z1 < -100 || z2 > 100 {
			o := Mega{x1, x2, y1, y2, z1, z2}
			others = append(others, o)
		} else {
			for z := z1; z <= z2; z++ {
				for y := y1; y <= y2; y++ {
					for x := x1; x <= x2; x++ {
						if on {
							world[z][y][x] = true
						} else {
							world[z][y][x] = false
						}
					}
				}
			}
		}
	}
	fmt.Printf("count %v..%v: %v\n", -1*size, size, cc(world))
	fmt.Printf("others: %v\n", len(others))

	for _, o := range others {
		if o.x1 > size && o.x2 > size || o.x1 < -1*size && o.x2 < -1*size ||
			o.y1 > size && o.y2 > size || o.y1 < -1*size && o.y2 < -1*size ||
			o.z1 > size && o.z2 > size || o.z1 < -1*size && o.z2 < -1*size {
			//fmt.Printf("Ignoring %v\n", o)
			continue
		} else {
			if o.x1 > size && o.x2 > size || o.x1 < -1*size && o.x2 < -1*size ||
				o.y1 > size && o.y2 > size || o.y1 < -1*size && o.y2 < -1*size ||
				o.z1 > size && o.z2 > size || o.z1 < -1*size && o.z2 < -1*size {
				fmt.Printf("Full overlap %v\n", o)

			} else {
				fmt.Printf("Partial %v\n", o)
			}
		}
	}

	return cc(world)
}

func part2(lines []string) int {
	return 0
}

func main() {
	timeStart := time.Now()
	argv := os.Args
	if len(argv) < 2 {
		fmt.Printf("Usage: %v /path/to/file\n", argv[0])
		return
	}
	fmt.Printf("# Argv    %s\n", argv)

	lines := getLines(argv[1])
	fmt.Printf("# Inputs  %d\n", len(lines))
	elapsed := time.Since(timeStart)
	fmt.Printf("# Parsing %s\n", elapsed)
	timeStart1 := time.Now()
	p1 := part1(lines)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part2(lines)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
