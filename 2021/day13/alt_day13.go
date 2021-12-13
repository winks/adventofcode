package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

type Fold struct {
	xy rune
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

func pp(p [][]rune) {
	for y := 0; y < len(p); y++ {
		for x := 0; x < len(p[0]); x++ {
			fmt.Printf("%v", string(p[y][x]))
		}
		fmt.Printf("\n")
	}
}

func count(p [][]rune) int {
	rv := 0
	for y := 0; y < len(p); y++ {
		for x := 0; x < len(p[0]); x++ {
			if p[y][x] == '#' {
				rv++
			}
		}
	}
	return rv
}

func part(lines []string, runPart1 bool) int {
	folds_x := 0
	folds_y := 0
	xmax := 0
	ymax := 0
	for _, line := range lines {
		if len(line) < 1 {
			continue
		}
		if line[0] == 'f' {
			xy := rune(line[11])
			if xy == 'x' {
				folds_x++
			} else {
				folds_y++
			}
			continue
		}
		li := strings.Split(line, ",")
		x, err := strconv.Atoi(li[0])
		check(err)
		y, err := strconv.Atoi(li[1])
		check(err)
		if x > xmax {
			xmax = x
		}
		if y > ymax {
			ymax = y
		}
	}
	xmax++
	ymax++

	if (runPart1) {
		folds_x = 1
		folds_y = 0
	}
	ffx := math.Pow(2, float64(folds_x))
	ffy := math.Pow(2, float64(folds_y))
	part_x := int(float64(1 + xmax) / float64(ffx)) - 1
	part_y := int(float64(1 + ymax) / float64(ffy)) - 1

	paper2 := [][]rune{}
	for y := 0; y < part_y; y++ {
		paper2 = append(paper2, []rune{})
		for x := 0; x < part_x; x++ {
			paper2[y] = append(paper2[y], ' ')
		}
	}

	for _, line := range lines {
		if len(line) < 1 || line[0] == 'f' {
			continue
		}
		li := strings.Split(line, ",")
		x, err := strconv.Atoi(li[0])
		check(err)
		y, err := strconv.Atoi(li[1])
		check(err)

		nx := x / (part_x + 1)
		ny := y / (part_y + 1)
		
		xx := x - nx * part_x - nx
		if nx % 2 == 1 {
			xx = part_x - xx - 1
		}
		yy := y - ny * part_y - ny
		if ny % 2 == 1 {
			yy = part_y - yy - 1
		}
		paper2[yy][xx] = '#'
	}
	if runPart1 {
		return count(paper2)
	} else {
		pp(paper2)
	}
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
	p1 := part(lines, true)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part(lines, false)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
