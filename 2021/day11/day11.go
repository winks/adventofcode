package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"time"
)

type Point struct {
	x int
	y int
	v int
	f bool
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

func getne(p Point, lines [10][10]Point) []Point {
	rv := []Point{}
	if p.y > 0 {
		rv = append(rv, lines[p.y-1][p.x])
	}
	if p.y < len(lines)-1 {
		rv = append(rv, lines[p.y+1][p.x])
	}
	if p.x > 0 {
		rv = append(rv, lines[p.y][p.x-1])
	}
	if p.x < len(lines[0])-1 {
		rv = append(rv, lines[p.y][p.x+1])
	}
	if p.y > 0 && p.x > 0 {
		rv = append(rv, lines[p.y-1][p.x-1])
	}
	if p.y > 0 && p.x < len(lines[0])-1 {
		rv = append(rv, lines[p.y-1][p.x+1])
	}
	if p.x > 0 && p.y < len(lines)-1 {
		rv = append(rv, lines[p.y+1][p.x-1])
	}
	if p.x < len(lines[0])-1 && p.y < len(lines)-1 {
		rv = append(rv, lines[p.y+1][p.x+1])
	}
	return rv
}

func pp(m [10][10]Point, print bool) int {
	c := 0
	for y := 0; y < 10; y++ {
		for x := 0; x < 10; x++ {
			if print {
				fmt.Printf("%d ", m[y][x].v)
			}
			if m[y][x].v > 9 && !m[y][x].f {
				c += 1
			}
		}
		if print {
			fmt.Printf("\n")
		}
	}
	if print {
		fmt.Printf("_ [%d]\n", c)
	}
	return c
}

func flash(p Point, m [10][10]Point) ([10][10]Point, int) {
	f := 0
	ne := []Point{}
	if p.v > 9 && !p.f {
		f += 1
		p.f = true
		m[p.y][p.x] = p
		ne = getne(p, m)
		//fmt.Printf("# %v -- %v\n", p, ne)
		for _, t := range ne {
			t.v += 1
			m[t.y][t.x] = t
		}
	}
	return m, f
}

func step(m [10][10]Point) ([10][10]Point, int) {
	f := 0
	for y := 0; y < 10; y++ {
		for x := 0; x < 10; x++ {
			m[y][x].v += 1
		}
	}
	//pp(m, true)
	for (pp(m, false) > 0) {
		for y := 0; y < 10; y++ {
			for x := 0; x < 10; x++ {
				mm, ff := flash(m[y][x], m)
				f += ff
				m = mm
			}
		}
	}
	//pp(m, true)
	for y := 0; y < 10; y++ {
		for x := 0; x < 10; x++ {
			if m[y][x].v > 9 {
				m[y][x].v = 0
				m[y][x].f = false
			}
		}
	}
	//pp(m, true)
	//fmt.Printf("========================================\n")
	return m, f
}

func part1(lines []string) int {
	m := [10][10]Point{}
	for y := 0; y < len(lines); y++ {
		for x := 0; x < len(lines[0]); x++ {
			v, err := strconv.Atoi(string(lines[y][x]))
			check(err)
			p := Point {x, y, v, false}
			m[y][x] = p
		}
	}
	f := 0
	//pp(m, true)
	//fmt.Printf("============\n")
	for i := 1; i < 101; i++ {
		//fmt.Printf("### step: %d\n", i)
		mm, ff := step(m)
		f += ff
		m = mm
	}
	return f
}

func dx(m [10][10]Point) bool {
	c := 0
	for y := 0; y < 10; y++ {
		for x := 0; x < 10; x++ {
			if (m[y][x].v > 9 || m[y][x].v == 0) {
				c +=1
			}
		}
	}
	return c == 100
}

func part2(lines []string) int {
	m := [10][10]Point{}
	for y := 0; y < len(lines); y++ {
		for x := 0; x < len(lines[0]); x++ {
			v, err := strconv.Atoi(string(lines[y][x]))
			check(err)
			p := Point {x, y, v, false}
			m[y][x] = p
		}
	}
	f := 0
	for i := 1; i < 501; i++ {
		mm, ff := step(m)
		f += ff
		m = mm
		if dx(m) {
			return i
		}
	}
	return f
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
