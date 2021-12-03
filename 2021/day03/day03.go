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

func part1(lines []string) (int, []int) {
	r := make([]int, 0)
	for i, s := range(lines) {
		for j := 0; j < len(s); j++ {
			if (i == 0) {
				r = append(r, 0)
			}
			if s[j:j+1] == "1" {
				r[j] += 1
			}
		}
	}
	rvg := ""
	rve := ""
	for j := 0; j < len(r); j++ {
		if r[j] > (len(lines)/2) {
			rvg += "1"
			rve += "0"
		} else {
			rvg += "0"
			rve += "1"
		}
	}
	rvg1, err := strconv.ParseInt(rvg, 2, 64)
	check(err)
	rve1, err := strconv.ParseInt(rve, 2, 64)
	check(err)
	return int(rvg1 * rve1), r
}

func part2(lines []string, r []int)  int {
	lines_o := []string{}
	lines_c := []string{}
	cutoff := float64(len(lines))/2.0

	lines_tmp := lines
	for true {
		for j := 0; j < len(lines[0]); j++ {
			for _, s := range(lines_tmp) {
				if float64(r[j]) > cutoff && s[j:j+1] == "1" {
					lines_o = append(lines_o, s)
				} else if float64(r[j]) < cutoff && s[j:j+1] == "0" {
					lines_o = append(lines_o, s)
				} else if float64(r[j]) == cutoff && s[j:j+1] == "1" {
					lines_o = append(lines_o, s)
				}
			}
			if len(lines_o) == 1 {
				lines_tmp = lines_o
				break
			}
			lines_tmp = lines_o
			cutoff = float64(len(lines_tmp))/2.0
			_, r = part1(lines_tmp)
			lines_o = []string{}
		}
		if len(lines_tmp) == 1 {
			break
		}
	}
	rvo1, err := strconv.ParseInt(lines_tmp[0], 2, 64)
	check(err)

	lines_tmp = lines
	_, r = part1(lines_tmp)
	cutoff = float64(len(lines_tmp))/2.0
	for true {
		for j := 0; j < len(lines[0]); j++ {
			for _, s := range(lines_tmp) {
				if float64(r[j]) < cutoff && s[j:j+1] == "1" {
					lines_c = append(lines_c, s)
				} else if float64(r[j]) > cutoff && s[j:j+1] == "0" {
					lines_c = append(lines_c, s)
				} else if float64(r[j]) == cutoff && s[j:j+1] == "0" {
					lines_c = append(lines_c, s)
				}
			}
			if len(lines_c) == 1 {
				lines_tmp = lines_c
				break
			}
			lines_tmp = lines_c
			cutoff = float64(len(lines_tmp))/2.0
			_, r = part1(lines_tmp)
			lines_c = []string{}
		}
		if len(lines_tmp) == 1 {
			break
		}
	}
	rvc1, err := strconv.ParseInt(lines_tmp[0], 2, 64)
	check(err)

	return int(rvo1 * rvc1)
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
	p1, p1x := part1(lines)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part2(lines, p1x)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
