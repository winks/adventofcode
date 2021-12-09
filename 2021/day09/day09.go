package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"time"
)

type Point struct {
	x int
	y int
	val int
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

func contains(s []Point, p Point) bool {
	for _, a := range s {
		if a == p {
			return true
		}
	}
	return false
}

func getne(p Point, lines []string) []Point {
	rv := []Point{}
	if p.y > 0 {
		v, err := strconv.Atoi(string(lines[p.y-1][p.x]))
		check(err)
		rv = append(rv, Point{p.x, p.y-1, v})
	}
	if p.y < len(lines)-1 {
		v, err := strconv.Atoi(string(lines[p.y+1][p.x]))
		check(err)
		rv = append(rv, Point{p.x, p.y+1, v})
	}
	if p.x > 0 {
		v, err := strconv.Atoi(string(lines[p.y][p.x-1]))
		check(err)
		rv = append(rv, Point{p.x-1, p.y, v})
	}
	if p.x < len(lines[0])-1 {
		v, err := strconv.Atoi(string(lines[p.y][p.x+1]))
		check(err)
		rv = append(rv, Point{p.x+1, p.y, v})
	}
	//fmt.Printf("N %v\n", rv)
	return rv
}

func getne2(p Point, lines []string) []Point {
	rv := []Point{}
	x, y := p.x, p.y
	for y > 0 {
		v, err := strconv.Atoi(string(lines[y-1][x]))
		check(err)
		if v < 9 {
			rv = append(rv, Point{x, y-1, v})
			y -= 1
		} else {
			break
		}
	}
	x, y = p.x, p.y
	for y < len(lines)-1 {
		v, err := strconv.Atoi(string(lines[y+1][x]))
		check(err)
		if v < 9 {
			rv = append(rv, Point{x, y+1, v})
			y += 1
		} else {
			break
		}
	}
	x, y = p.x, p.y
	for x > 0 {
		v, err := strconv.Atoi(string(lines[y][x-1]))
		check(err)
		if v < 9 {
			rv = append(rv, Point{x-1, y, v})
			x -=1
		} else {
			break
		}
	}
	x, y = p.x, p.y
	for x < len(lines[0])-1 {
		v, err := strconv.Atoi(string(lines[y][x+1]))
		check(err)
		if v < 9 {
			rv = append(rv, Point{x+1, y, v})
			x += 1
		} else {
			break
		}
	}
	rv = append(rv, p)
	return rv
}

func part1(lines []string) (int, []Point) {
	rv := []Point{}
	for y := 0; y < len(lines); y++ {
		for x := 0; x < len(lines[0]); x++ {
			v, err := strconv.Atoi(string(lines[y][x]))
			check(err)
			p := Point{x,y,v}
			neigh := getne(p, lines)
			low := true
			for _, n := range(neigh) {
				if p.val >= n.val {
					low = false
				}
			}
			if low {
				rv = append(rv, p)
			}
		}
	}
	rvx := 0
	for _, r := range(rv) {
		rvx += r.val+1
	}
	return rvx, rv
}

func part2(lines []string, points []Point) int {
	rv := []int{}
	for _, pt := range(points) {
		pp := []Point{}
		todo := []Point{ pt }
		for len(todo) > 0 {
			d := todo[0]
			todo = todo[1:]
			ne := getne2(d, lines)
			for _, n := range(ne) {
				if !contains(todo, n) && !contains(pp, n) {
					todo = append(todo, n)
				}
			}
			for _, n := range(ne) {
				if !contains(pp, n) {
					pp = append(pp, n)
				}
			}
		}
		rv = append(rv, len(pp))
	}
	sort.Ints(rv)
	rv = rv[len(rv)-3:]
	return rv[0] * rv[1] * rv[2]
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
	p1, pts := part1(lines)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part2(lines, pts)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
