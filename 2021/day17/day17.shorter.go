package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
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

func step(s State) State {
	vx := 0
	if s.vx > 0 {
		vx = s.vx - 1
	} else if s.vx < 0 {
		vx = s.vx + 1
	}
	return State{s.x + s.vx, s.y - s.vy, vx, s.vy - 1}
}

func run(s State, tx0 int, tx1 int, ty0 int, ty1 int) (int, bool) {
	best_y := 0
	for {
		s = step(s)
		if s.y < best_y {
			best_y = s.y
		}
		if s.y > ty1 || s.x > tx1 {
			return 0, true
		}
		if s.y >= ty0 && s.y <= ty1 && s.x >= tx0 && s.x <= tx1 {
			return best_y, false
		}
	}
}

func part1(line string) (int, int) {
	parts := strings.Split(line, " ")
	mx := strings.Split(strings.Replace(strings.Replace(parts[2], "x=", "", -1), ",", "", -1), "..")
	my := strings.Split(strings.Replace(strings.Replace(parts[3], "y=", "", -1), ",", "", -1), "..")
	tx0, err := strconv.Atoi(mx[0])
	check(err)
	tx1, err := strconv.Atoi(mx[1])
	check(err)
	ty0, err := strconv.Atoi(my[0])
	check(err)
	ty1, err := strconv.Atoi(my[1])
	check(err)
	ty0 = int(math.Abs(float64(ty0)))
	ty1 = int(math.Abs(float64(ty1)))
	if ty1 < ty0 {
		ty0, ty1 = ty1, ty0
	}

	best_y := 99
	total := 0
	runs := 310
	for y := -1 * runs; y < runs; y++ {
		for x := -1 * runs; x < runs; x++ {
			s := State{0, 0, x, y}
			res, err := run(s, tx0, tx1, ty0, ty1)
			if !err {
				total += 1
				if res < best_y {
					best_y = res
				}
			}
		}
	}
	return -1 * best_y, total
}

func main() {
	fh, err := os.OpenFile(os.Args[1], os.O_RDONLY, os.ModePerm)
	check(err)
	sc := bufio.NewScanner(fh)
	for sc.Scan() {
		p1, p2 := part1(sc.Text())
		fmt.Printf("Part 1: %d\nPart 2: %d\n", p1, p2)
	}
}
