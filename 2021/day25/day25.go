package main

import (
	"bufio"
	"fmt"
	"os"
	"time"
)

type Point struct {
	x, y int
	val  string
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

func xcopy(sea [][]Point) [][]Point {
	sea0 := make([][]Point, len(sea))
	for a := range sea {
		sea0[a] = make([]Point, 0)
		for b := range sea[a] {
			sea0[a] = append(sea0[a], sea[a][b])
		}
	}
	return sea0
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

func getNbEast(s [][]Point, x int, y int) Point {
	nx := x + 1
	ny := y
	if nx >= len(s[0]) {
		nx = 0
	}
	return s[ny][nx]
}

func getNbSouth(s [][]Point, x int, y int) Point {
	nx := x
	ny := y + 1
	if ny >= len(s) {
		ny = 0
	}
	return s[ny][nx]
}

func part1(lines []string) int {
	sea := [][]Point{}
	for y, line := range lines {
		row := []Point{}
		for x := range line {
			row = append(row, Point{x, y, string(line[x])})
		}
		sea = append(sea, row)
	}
	i := 1
	for {
		sea0 := xcopy(sea)
		//fmt.Printf("STEP %v\n", i)
		sea2 := xcopy(sea)
		for turn := 1; turn <= 2; turn++ {
			//fmt.Printf("T %v\n", turn)
			if turn == 1 {
				moved := []Point{}
				for y := 0; y < len(sea); y++ {
					for x := 0; x < len(sea[0]); x++ {
						nb := getNbEast(sea, x, y)
						cont := false
						for _, pp := range moved {
							if (nb.y == pp.y && nb.x == pp.x) || (y == pp.y && x == pp.x) {
								cont = true
								break
							}
						}
						if cont {
							continue
						}
						if sea[y][x].val == ">" && nb.val == "." {
							sea2[nb.y][nb.x].val = ">"
							sea2[y][x].val = "."
							moved = append(moved, sea2[nb.y][nb.x])
						} else {
							sea2[y][x].val = sea[y][x].val
						}
					}
				}
			} else {
				moved := []Point{}
				for y := 0; y < len(sea); y++ {
					for x := 0; x < len(sea[0]); x++ {
						nb := getNbSouth(sea, x, y)
						cont := false
						for _, pp := range moved {
							if (nb.y == pp.y && nb.x == pp.x) || (y == pp.y && x == pp.x) {
								cont = true
								break
							}
						}
						if cont {
							continue
						}
						if sea[y][x].val == "v" && nb.val == "." {
							sea2[nb.y][nb.x].val = "v"
							sea2[y][x].val = "."
							moved = append(moved, sea2[nb.y][nb.x])
						} else {
							sea2[y][x].val = sea[y][x].val
						}
					}
				}
			}
			sea = xcopy(sea2)
		}
		// check eq
		eqc := 0
		for yc1 := range sea0 {
			for xc1 := range sea0[0] {
				if sea0[yc1][xc1] == sea[yc1][xc1] {
					eqc++
				}
			}
		}

		if eqc == len(sea)*len(sea[0]) {
			return i
		}
		//pp(sea, true)
		i++
	}
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
