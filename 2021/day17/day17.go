package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type State struct {
	x  int
	y  int
	vx int
	vy int
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

func pp(m [][]rune, print bool) int {
	c := 0
	for y := 0; y < len(m); y++ {
		for x := 0; x < len(m[0]); x++ {
			if print {
				fmt.Printf("%s", string(m[y][x]))
			}
		}
		if print {
			fmt.Printf("\n")
		}
	}
	if print {
		//fmt.Printf("_ [%d]\n", c)
	}
	return c
}

func step(floor [][]rune, s State, print bool) ([][]rune, State) {
	if print {
		fmt.Printf("was: x %v, y %v | vx %v vy %v\n", s.x, s.y, s.vx, s.vy)
	}
	x2 := s.x + s.vx
	y2 := s.y - s.vy

	vx := 0
	if s.vx > 0 {
		vx = s.vx - 1
	} else if s.vx < 0 {
		vx = s.vx + 1
	}
	vy := s.vy - 1

	if print {
		fmt.Printf("now: x, %v y, %v | vx %v vy %v\n", x2, y2, vx, vy)
		//floor[s.y][s.x] = '~'
		size := len(floor)
		floor2 := make([][]rune, 0)
		for i := 0; i < size; i++ {
			row := make([]rune, 0)
			floor2 = append(floor2, row)
			for j := 0; j < size; j++ {
				floor2[i] = append(floor2[i], floor[i][j])
			}
		}
		if x2 >= 0 && y2 >= 0 {
			floor2[y2][x2] = '#'
		}

		return floor2, State{x2, y2, vx, vy}
	} else {
		return floor, State{x2, y2, vx, vy}
	}
}

func run(floor [][]rune, s State, tx0 int, tx1 int, ty0 int, ty1 int, print bool) (int, bool) {
	i := 0
	best_y := 0
	for {
		if print {
			fmt.Printf("# %v -- (%v,%v) %v\n", i, s.vx, s.vy, s)
		}
		floor, s = step(floor, s, print)
		if s.y < best_y {
			best_y = s.y
		}
		i++
		if print {
			pp(floor, true)
		}
		if s.y > ty1 || s.x > tx1 {
			return 0, true
		}
		if s.y >= ty0 && s.y <= ty1 && s.x >= tx0 && s.x <= tx1 {
			if print {
				pp(floor, true)
				fmt.Printf("HIT %v -- %v\n", i, s)
			}
			break
		}
	}
	return best_y, false
}

func part1(lines []string) (int, int) {
	sizey := 77
	sizex := 310
	runs := 310

	line := lines[0]
	parts := strings.Split(line, " ")
	parts[2] = strings.Replace(parts[2], "x=", "", -1)
	parts[2] = strings.Replace(parts[2], ",", "", -1)
	mx := strings.Split(parts[2], "..")
	parts[3] = strings.Replace(parts[3], "y=", "", -1)
	parts[3] = strings.Replace(parts[3], ",", "", -1)
	my := strings.Split(parts[3], "..")
	//fmt.Printf("%v %v || ", mx, my)
	tx0, err := strconv.Atoi(mx[0])
	check(err)
	tx1, err := strconv.Atoi(mx[1])
	check(err)
	ty0, err := strconv.Atoi(my[0])
	check(err)
	ty1, err := strconv.Atoi(my[1])
	check(err)
	if tx0 < 0 {
		tx0 = -1 * tx0
	}
	if tx1 < 0 {
		tx1 = -1 * tx1
	}
	if ty0 < 0 {
		ty0 = -1 * ty0
	}
	if ty1 < 0 {
		ty1 = -1 * ty1
	}
	if tx1 < tx0 {
		tx0, tx1 = tx1, tx0
	}
	if ty1 < ty0 {
		ty0, ty1 = ty1, ty0
	}
	//fmt.Printf("T %v %v -- %v %v\n", tx0, tx1, ty0, ty1)

	xoff := 0
	yoff := 0
	//fmt.Printf("xoff yoff %v %v \n", xoff, yoff)
	//fmt.Printf("T %v %v -- %v %v\n", tx0, tx1, ty0+yoff, ty1+yoff)
	start := []int{yoff * 3, xoff}
	//fmt.Printf("S %v \n", start)

	floor := make([][]rune, 0)
	for i := 0; i < sizey; i++ {
		row := make([]rune, 0)
		for j := 0; j < sizex; j++ {
			row = append(row, '.')
		}
		floor = append(floor, row)
	}
	floor[start[0]][start[1]] = 'S'
	for i := ty0; i <= ty1; i++ {
		for j := tx0; j <= tx1; j++ {
			floor[i][j] = 'T'
		}
	}
	//pp(floor, true)

	best_y := 99
	total := 0
	for y := -1 * runs; y < runs; y++ {
		for x := -1 * runs; x < runs; x++ {
			s := State{start[1], start[0], x, y}
			pri := false
			res, err := run(floor, s, tx0, tx1, ty0, ty1, pri)
			if !err {
				total += 1
			}
			if pri {
				if !err && res < best_y {
					best_y = res
					fmt.Printf("new best: %v,%v = %v\n", x, y, best_y)
				} else if !err {
					fmt.Printf("not best: %v,%v = %v\n", x, y, res)
				} else {
					fmt.Printf("best err: %v,%v = %v\n", x, y, res)
				}
			} else {
				if !err && res < best_y {
					best_y = res
				}
			}
		}
	}

	return -1*best_y + yoff, total
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
	p1, p2 := part1(lines)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
