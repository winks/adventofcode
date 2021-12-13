package main

import (
	"bufio"
	"fmt"
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

func resize(orig [][]rune, ny int, nx int) [][]rune {
	rv := [][]rune{}
	if ny > 0 {
		for y := 0; y < ny; y++ {
			rv = append(rv, []rune{})
			for x := 0; x < len(orig[0]); x++ {
				rv[y] = append(rv[y], orig[y][x])
			}
		}
		return rv
	} else if nx > 0 {
		for y := 0; y < len(orig); y++ {
			rv = append(rv, []rune{})
			for x := 0; x < nx; x++ {
				rv[y] = append(rv[y], orig[y][x])
			}
		}
		return rv
	}
	return rv
}

func part(lines []string, runPart1 bool) int {
	folds := []Fold{}
	xmax := 0
	ymax := 0
	for _, line := range lines {
		if len(line) < 1 {
			continue
		}
		if line[0] == 'f' {
			f1 := line[13:]
			f1n, err := strconv.Atoi(f1)
			check(err)
			folds = append(folds, Fold {rune(line[11]), f1n})
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

	paper := [][]rune{}
	for y := 0; y < ymax; y++ {
		paper = append(paper, []rune{})
		for x := 0; x < xmax; x++ {
			paper[y] = append(paper[y], '.')
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
		paper[y][x] = '#'
	}

	for _, fold := range folds {
		if fold.xy == 'y' {
			for x := 0; x < len(paper[0]); x++ {
				paper[fold.val][x] = '-'
			}
			for y := 0; y < fold.val; y++ {
				readline := ymax - 1 - y
				for x := 0; x < len(paper[0]); x++ {
					if paper[readline][x] == '#' {
						paper[y][x] = '#'
					}
				}
			}
			paper = resize(paper, fold.val, 0)
			ymax = ymax/2
		} else if fold.xy == 'x' {
			for y := 0; y < len(paper); y++ {
				paper[y][fold.val] = '|'
			}
			for x := 0; x < fold.val; x++ {
				readcol := xmax - 1 - x
				for y := 0; y < len(paper); y++ {
					if paper[y][readcol] == '#' {
						paper[y][x] = '#'
					}
				}
			}
			paper = resize(paper, 0, fold.val)
			xmax = xmax/2
		}
		if runPart1 {
			return count(paper)
		} else {
			//fmt.Printf("fi: %d xx: %d yy: %d\n", fi, len(paper[0]), len(paper))
		}
	}

	pp(paper)
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
