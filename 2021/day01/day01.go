package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"time"
)

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

func part1(lines []string) int {
	cnt := 0
	cur, err := strconv.Atoi(lines[0])
	check(err)
	for _, x := range lines {
		a, err := strconv.Atoi(x)
		check(err)
		if a > cur {
			cnt = cnt + 1
		}
		cur = a
	}
	return cnt
}

func part2(lines []string) int {
	cnt := 0
	cur := 0
	for i, x := range lines {
		if i > 1 && i < len(lines)-1 {
			a, err := strconv.Atoi(x)
			check(err)
			b, err := strconv.Atoi(lines[i-1])
			check(err)
			c, err := strconv.Atoi(lines[i-2])
			check(err)
			sum := a + b + c
			if sum > cur {
				cnt = cnt + 1
			}
			cur = sum
		}
	}
	return cnt
}

func main() {
	timeStart := time.Now()
	argv := os.Args
	if len(argv) < 2 {
		fmt.Printf("Usage: %v /path/to/file\n", argv[0])
		return
	}
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
