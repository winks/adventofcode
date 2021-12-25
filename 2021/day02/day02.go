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
	hp := 0
	d := 0

	for _, s := range lines {
		p := strings.Split(s, " ")
		arg, err := strconv.Atoi(p[1])
		check(err)
		if p[0] == "forward" {
			hp += arg
		} else if p[0] == "up" {
			d -= arg
		} else if p[0] == "down" {
			d += arg
		} else {
			fmt.Printf("X %v", p)
		}
	}
	return hp * d
}

func part2(lines []string) int {
	hp := 0
	d := 0
	aim := 0

	for _, s := range lines {
		p := strings.Split(s, " ")
		arg, err := strconv.Atoi(p[1])
		check(err)
		if p[0] == "forward" {
			hp += arg
			d += (aim * arg)
		} else if p[0] == "up" {
			//d -= arg
			aim -= arg
		} else if p[0] == "down" {
			//d += arg
			aim += arg
		} else {
			fmt.Printf("X %v", p)
		}
		//fmt.Printf("hp %d d %d aim %d\n", hp, d, aim)
	}
	return hp * d
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
