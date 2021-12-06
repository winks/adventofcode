package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type School struct {
	amount int
	tick int
}

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

func count(fish []School) int {
	rv := 0
	for _, f := range(fish) {
		rv += f.amount
	}
	return rv
}

func part1(lines []string) int {
	lines2 := strings.Split(lines[0], ",")
	fish := []int{}
	for _, v := range(lines2) {
		n, err := strconv.Atoi(v)
		check(err)
		fish = append(fish, n)
	}

	done := false
	day := 0
	for !done {
		for i, f := range(fish) {
			if f > 0 {
				f -= 1
			} else if f == 0 {
				f = 6
				fish = append(fish, 8)
			} else {
				fmt.Printf("ERR %v\n", f)
			}
			fish[i] = f
		}
		day +=1
		if day >= 80 {
			done = true
		}
	}
	return len(fish)
}

func part2(lines []string) int {
	lines2 := strings.Split(lines[0], ",")
	fish := []School{}
	for _, v := range(lines2) {
		n, err := strconv.Atoi(v)
		check(err)
		f := School{1, n}
		fish = append(fish, f)
	}

	done := false
	day := 0
	for !done {
		spawn := 0
		for i, f := range(fish) {
			if f.tick > 0 {
				f.tick -= 1
			} else if f.tick == 0 {
				f.tick = 6
				spawn += f.amount
			} else {
				fmt.Printf("ERR %v\n", f)
			}
			fish[i] = f
		}
		if spawn > 0 {
			nf := School{spawn, 8}
			fish = append(fish, nf)
		}
		day +=1
		if day >= 256 {
			done = true
		}
	}
	return count(fish)
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
