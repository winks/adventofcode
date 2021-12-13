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

//func pp(p [15][11]rune) {
func pp(p [895][1311]rune) {
	for y := 0; y < len(p); y++ {
		for x := 0; x < len(p[0]); x++ {
			fmt.Printf("%v", string(p[y][x]))
		}
		fmt.Printf("\n")
	}
	fmt.Printf("//////////////////////////////////////////\n")
}

//func counte(p [15][11]rune, ym int, xm int) int {
func counte(p [895][1311]rune, ym int, xm int) int {
	rv := 0
	for y := 0; y < ym; y++ {
		for x := 0; x < xm; x++ {
			if p[y][x] == '#' {
				rv++
			}
		}
	}
	return rv
}

func part1(lines []string) int {
	sizex := 11
	sizey := 15
	sizex = 1311
	sizey = 895
	//paper := [15][11]rune{}
	paper := [895][1311]rune{}
	for y := 0; y < sizey; y++ {
		for x := 0; x < sizex; x++ {
			paper[y][x] = '.'
		}
	}
	//pp(paper)
	folds := []Fold{}
	xmax := 0
	ymax := 0
	for _, line := range lines {
		if len(line) < 1 {
			continue
		}
		if line[0] == 'f' {
			f1a := rune(line[11])
			f1 := line[13:]
			f1n, err := strconv.Atoi(f1)
			check(err)
			ff := Fold {f1a, f1n}
			folds = append(folds, ff)
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
	fmt.Printf("xx: %d yy: %d\n", xmax, ymax)
	for i, ff := range folds {
		fmt.Printf("# fold %d : %s=%d\n", i, string(ff.xy), ff.val)
	}

	//folds = []Fold{ folds[0] }
	//pp(paper)
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
		}
	}
	pp(paper)

	//return counte(paper, folds[0].val, len(paper[0]))
	return counte(paper, len(paper), folds[0].val)
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
