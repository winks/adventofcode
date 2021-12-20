package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"time"
)

type Point struct {
	x   int
	y   int
	val rune
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

func pp(m [][]Point, print bool) {
	for y := 0; y < len(m); y++ {
		for x := 0; x < len(m[0]); x++ {
			if print {
				fmt.Printf("%v", string(m[y][x].val))
			}
		}
		if print {
			fmt.Printf("\n")
		}
	}
	fmt.Printf("\n\n")
}

/// get the neighbors (incl p) in a 3x3 grid
/// this one is in order of right to left, top to down
func getne(p Point, lines [][]Point) []Point {
	rv := []Point{}
	if p.y > 0 && p.x > 0 {
		rv = append(rv, lines[p.y-1][p.x-1])
	}
	if p.y > 0 {
		rv = append(rv, lines[p.y-1][p.x])
	}
	if p.y > 0 && p.x < len(lines[0])-1 {
		rv = append(rv, lines[p.y-1][p.x+1])
	}
	if p.x > 0 {
		rv = append(rv, lines[p.y][p.x-1])
	}
	rv = append(rv, lines[p.y][p.x])
	if p.x < len(lines[0])-1 {
		rv = append(rv, lines[p.y][p.x+1])
	}
	if p.x > 0 && p.y < len(lines)-1 {
		rv = append(rv, lines[p.y+1][p.x-1])
	}
	if p.y < len(lines)-1 {
		rv = append(rv, lines[p.y+1][p.x])
	}
	if p.x < len(lines[0])-1 && p.y < len(lines)-1 {
		rv = append(rv, lines[p.y+1][p.x+1])
	}

	return rv
}

func join(ps []Point) string {
	s := ""
	for _, p := range ps {
		s += string(p.val)
	}
	return s
}

func conv(s string) int {
	r := 0
	for i := len(s) - 1; i >= 0; i-- {
		if s[i] == '#' {
			idx := len(s) - 1 - i
			n := int(math.Pow(2, float64(idx)))
			r += n
		}
	}
	return r
}

func step(image [][]Point, algo string) [][]Point {
	nim := make([][]Point, 0)
	for y := range image {
		row := []Point{}
		for x := range image[y] {
			row = append(row, image[y][x])
		}
		nim = append(nim, row)
	}

	my := 0
	mx := 0
	for y := range image {
		for x := range image[y] {
			p := image[y][x]
			pos := conv(join(getne(p, image)))
			p2 := Point{p.x, p.y, rune(algo[pos])}
			nim[y][x] = p2
			mx = x
		}
		my = y
	}
	// curse you, infinite grids!
	if nim[0][1].val == '.' {
		nim[0][0].val = '.'
		nim[0][mx].val = '.'
		nim[my][0].val = '.'
		nim[my][mx].val = '.'
	}
	return nim
}

func part1(lines []string, runs int) int {
	algo := ""
	image0 := []string{}
	done := false
	image := make([][]Point, 0)

	offset := runs + 5
	erow := ""
	lrrow := ""
	for j := 0; j < offset; j++ {
		lrrow += "."
	}

	for _, line := range lines {
		if len(line) < 1 {
			done = true
			continue
		} else if done {
			line2 := lrrow + line + lrrow
			image0 = append(image0, line2)
		} else {
			algo = algo + line
		}
	}
	for j := 0; j < len(image0[0]); j++ {
		erow += "."
	}
	for i := 0; i < offset; i++ {
		image0 = append([]string{erow}, image0...)
		image0 = append(image0, erow)
	}

	for iy, y := range image0 {
		image = append(image, []Point{})
		for ix := range y {
			image[iy] = append(image[iy], Point{ix, iy, rune(y[ix])})
		}
	}

	for i := 0; i < runs; i++ {
		image = step(image, algo)
	}

	rv := 0
	for y := range image {
		for x := range image[y] {
			if image[y][x].val == '#' {
				rv++
			}
		}
	}
	return rv
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
	p1 := part1(lines, 2)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part1(lines, 50)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
