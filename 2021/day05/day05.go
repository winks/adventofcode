package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
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

func draw(floor [1000][1000]int, start []string, end []string) [1000][1000]int {
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

//func draw2(floor [10][10]int, start []string, end []string) [10][10]int {
func draw2(floor [1000][1000]int, start []string, end []string) [1000][1000]int {
	x1, err := strconv.Atoi(start[0])
	check(err)
	x2, err := strconv.Atoi(end[0])
	check(err)
	y1, err := strconv.Atoi(start[1])
	check(err)
	y2, err := strconv.Atoi(end[1])
	check(err)
	
	stops := []int{}
	
	stops = append(stops, x1)
	stops = append(stops, y1)
	
	for x1 != x2 && y1 != y2 {
		if (x2 > x1)  {
			x1 += 1
		} else {
			x1 -= 1
		}
		if y2 > y1 {
			y1 += 1
		} else {
			y1 -= 1
		}
		stops = append(stops, x1)
		stops = append(stops, y1)
	}

	for i := 0; i< len(stops); i +=2 {
		x := stops[i]
		y := stops[i+1]
		floor[y][x] += 1
	}

	//fmt.Printf("## %v\n", stops)
	return floor
}

func count(floor [1000][1000]int) int {
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
	//floor := make([][]int, len(lines))
	//for i, _ := range(lines) {
	//	floor[i] = make([]int, len(lines))
	//}
	floor := [1000][1000]int{}
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

func part2(lines []string) int {
	floor := [1000][1000]int{}
	//fmt.Printf("# %v\n", floor)
	for _, v := range(lines) {
		line := strings.Split(v, " -> ")
		//fmt.Printf("%v\n", line)
		start := strings.Split(line[0], ",")
		end := strings.Split(line[1], ",")
		
		if start[0] != end[0] && start[1] != end[1] {
			floor = draw2(floor, start, end)
		} else {
			floor = draw(floor, start, end)
		}
		
	}
	//fmt.Printf("# %v\n", floor)
	return count(floor)
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
