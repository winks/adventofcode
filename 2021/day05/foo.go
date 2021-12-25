package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func numArg(s string, def int) int {
	stx, err := strconv.Atoi(s)
	if err != nil {
		return def
	}
	return stx
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

func draw(floor [][]int, start []string, end []string) [][]int {
//func draw(floor [10][10]int, start []string, end []string) [10][10]int {
	x1, err := strconv.Atoi(start[0])
	check(err)
	x2, err := strconv.Atoi(end[0])
	check(err)
	y1, err := strconv.Atoi(start[1])
	check(err)
	y2, err := strconv.Atoi(end[1])
	check(err)
	if (x2 < x1) {
		tmp := x1
		x1 = x2
		x2 = tmp
	}
	if (y2 < y1) {
		tmp := y1
		y1 = y2
		y2 = tmp
	}
	for x :=x1; x <= x2; x++ {
		for y := y1; y <= y2; y++ {
			floor[y][x] += 1
		}
	}
	return floor
}

func count(floor [][]int) int {
//func count(floor [10][10]int) int {
	rv := 0
	for y, _ := range(floor) {
		for x, _ := range(floor) {
			if floor[y][x] > 1 {
				rv += 1
			}
		}
	}
	return rv
}

func part1(lines []string) int {
	floor := make([][]int, 1000)
	for i := 0; i < 1000; i++ {
		floor[i] = make([]int, 1000)
	}
	//floor := [10][10]int{}
	//fmt.Printf("# %v\n", floor)
	for _, v := range(lines) {
		line := strings.Split(v, " -> ")
		//fmt.Printf("%v\n", line)
		start := strings.Split(line[0], ",")
		end := strings.Split(line[1], ",")
		if start[0] != end[0] && start[1] != end[1] {
			continue
		}
		floor = draw(floor, start, end)
	}
	//fmt.Printf("# %v\n", floor)
	return count(floor)
}


func main() {
	argv := os.Args
	if len(argv) < 2 {
		fmt.Printf("Usage: %v /path/to/file\n", argv[0])
		return
	}
	fmt.Printf("# Argv    %s\n", argv)

	lines := getLines(argv[1])
	p1 := part1(lines)
	fmt.Printf("Part 1: %d\n", p1)

	a1 := 1
	b2 := 2

	a1, b2 = b2, a1
	fmt.Printf("%d %d\n", a1, b2)
}
