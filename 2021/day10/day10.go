package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
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

func part1(lines []string) (int, []string) {
	rv := 0
	good := []string{}
	vals := make(map[string]int)
	vals[")"] = 3
	vals["]"] = 57
	vals["}"] = 1197
	vals[">"] = 25137
	for i, li := range lines {
		fmt.Printf("# %d %v\n", i, li)
		rvl := 0
		// ( [ { <
		data := [4]int{}
		tmp := ""
		for j, c := range(li) {
			err := false
			if c == '(' {
				data[0] += 1
				tmp += string(c)
			} else if c == ')' {
				data[0] -= 1
				if tmp[len(tmp)-1] == '(' {
					tmp = strings.TrimSuffix(tmp, string('('))
				} else if j < len(li)-1 {
					rvl = vals[string(c)]
					break
				}
			} else if c == '[' {
				data[1] += 1
				tmp += string(c)
			} else if c == ']' {
				data[1] -= 1
				if tmp[len(tmp)-1] == '[' {
					tmp = strings.TrimSuffix(tmp, string('['))
				} else if j < len(li)-1 {
					rvl = vals[string(c)]
					break
				}
			} else if c == '{' {
				data[2] += 1
				tmp += string(c)
			} else if c == '}' {
				data[2] -= 1
				if len(tmp) > 0 && tmp[len(tmp)-1] == '{' {
					tmp = strings.TrimSuffix(tmp, string('{'))
				} else if j < len(li)-1 {
					rvl = vals[string(c)]
					break
				}
			} else if c == '<' {
				data[3] += 1
				tmp += string(c)
			} else if c == '>' {
				data[3] -= 1
				if tmp[len(tmp)-1] == '<' {
					tmp = strings.TrimSuffix(tmp, string('<'))
				} else if j < len(li)-1 {
					rvl = vals[string(c)]
					break
				}
			}
			fmt.Printf("## %v %s %s\n", data, string(c), tmp)
			if err {
				break
			}
		}
		if rvl > 0 {
			fmt.Printf("_rvl %d %v\n ", i, rvl)
		} else {
			good = append(good, tmp)
		}
		rv += rvl
		fmt.Printf("  %v\n\n ", data)
	}
	fmt.Printf("_  %v\n ", rv)

	return rv, good
}

func part2(lines []string) int {
	fmt.Printf("_ %d  %v\n", len(lines), lines)
	rvs := []int{}
	for _, line := range(lines) {
		fmt.Printf("### %v\n", line)
		score := 0
		for len(line) > 0 {
			c := line[len(line)-1]
			line = strings.TrimSuffix(line, string(c))
			score *= 5
			if c == '(' {
				score += 1
			} else if c == '[' {
				score += 2
			} else if c == '{' {
				score += 3
			} else if c == '<' {
				score += 4
			}
			fmt.Printf("__ %d\n", score)
		}
		rvs = append(rvs, score)
	}
	fmt.Printf("# %v\n", rvs)
	sort.Ints(rvs)
	return rvs[len(rvs)/2]
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
	p1, good := part1(lines)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part2(good)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
