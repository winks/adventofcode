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
	for _, li := range lines {
		rvl := 0
		tmp := ""
		for j, c := range(li) {
			if c == '(' {
				tmp += string(c)
			} else if c == ')' {
				if tmp[len(tmp)-1] == '(' {
					tmp = strings.TrimSuffix(tmp, string('('))
				} else if j < len(li)-1 {
					rvl = vals[string(c)]
					break
				}
			} else if c == '[' {
				tmp += string(c)
			} else if c == ']' {
				if tmp[len(tmp)-1] == '[' {
					tmp = strings.TrimSuffix(tmp, string('['))
				} else if j < len(li)-1 {
					rvl = vals[string(c)]
					break
				}
			} else if c == '{' {
				tmp += string(c)
			} else if c == '}' {
				if len(tmp) > 0 && tmp[len(tmp)-1] == '{' {
					tmp = strings.TrimSuffix(tmp, string('{'))
				} else if j < len(li)-1 {
					rvl = vals[string(c)]
					break
				}
			} else if c == '<' {
				tmp += string(c)
			} else if c == '>' {
				if tmp[len(tmp)-1] == '<' {
					tmp = strings.TrimSuffix(tmp, string('<'))
				} else if j < len(li)-1 {
					rvl = vals[string(c)]
					break
				}
			}
		}
		if rvl < 1 {
			good = append(good, tmp)
		}
		rv += rvl
	}
	return rv, good
}

func part2(lines []string) int {
	rvs := []int{}
	for _, line := range(lines) {
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
		}
		rvs = append(rvs, score)
	}
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
