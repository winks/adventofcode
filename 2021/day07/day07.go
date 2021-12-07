package main

import (
	"bufio"
	"fmt"
	"math"
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
	lines2 := strings.Split(lines[0], ",")
	nums := []int{}
	nmin := 0
	nmax := 0
	for _, v := range(lines2) {
		n, err := strconv.Atoi(v)
		check(err)
		nums = append(nums, n)

		if n < nmin {
			nmin = n
		}
		if n > nmax {
			nmax = n
		}
	}
	fmt.Printf("%d %d | %v\n", nmin, nmax, nums)

	fuel_min := 0.0
	for i := nmin; i <= nmax; i++ {
		fuel := 0.0
		for _, v := range(nums) {
			fuel += math.Abs( float64(v) - float64(i) )
		}
		//fmt.Printf("# %d %d\n", i, fuel)
		if fuel_min < 0.01 {
			fuel_min = fuel
		}
		if fuel_min > 0 && fuel < fuel_min {
			fuel_min = fuel
		}
		//fmt.Printf("########\n")
	}

	return int(fuel_min)
}

func part2(lines []string) int {
	lines2 := strings.Split(lines[0], ",")
	nums := []int{}
	nmin := 0
	nmax := 0
	for _, v := range(lines2) {
		n, err := strconv.Atoi(v)
		check(err)
		nums = append(nums, n)

		if n < nmin {
			nmin = n
		}
		if n > nmax {
			nmax = n
		}
	}
	fmt.Printf("%d %d | %v\n", nmin, nmax, nums)

	fuel_min := 0.0
	for i := nmin; i <= nmax; i++ {
		fuel := 0.0
		for _, v := range(nums) {
			diff := math.Abs( float64(v) - float64(i) )
			for d := 1.0; d <= diff; d += 1.0 {
				fuel += d
			}
		}
		fmt.Printf("# %d %d\n", i, fuel)
		if fuel_min < 0.01 {
			fuel_min = fuel
		}
		if fuel_min > 0 && fuel < fuel_min {
			fuel_min = fuel
		}
		fmt.Printf("########\n")
	}

	return int(fuel_min)
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
