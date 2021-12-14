package main

import (
	"bufio"
	"fmt"
	"os"
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

func part1(lines []string, runs int) int {
	tpls := lines[0]
	lines = lines[2:]
	rules := [][]string{}
	tpl := []rune{}
	for _, t := range tpls {
		tpl = append(tpl, t)
	}
	for _, line := range lines {
		rule := strings.Split(line, " ")
		rules = append(rules, []string{ rule[0], rule[2] })
	}

	tpl2 := make(map[string]int, 0)
	for i := 0; i < len(tpl); i++ {
		if i + 2 > len(tpl) {
			tpl2[ string(tpl[i]) + "_" ] = 1
			tpl2[ "_" + string(tpl[0]) ] = 1
			break
		}
		curx := string(tpl[i:i+2])
		tpl2[curx] += 1
	}

	cn := make(map[byte]int, 0)
	mmin := 9999999999999999
	mmax := 0
	tpl3 := make(map[string]int, 0)
	for step := 0; step < runs; step ++ {
		//fmt.Printf("\nSTEP %v %v\n", step, tpl2)
		tpl3 = make(map[string]int, 0)
		for x, y := range tpl2 {
			tpl3[x] = y
		}
		for cur,_ := range tpl3 {
			if cur[0] == '_' || cur[1] == '_' || tpl3[cur] < 1{
				continue
			}
			for _, k := range rules {
				if k[0] == cur {
					cur1 := string(cur[0]) + k[1]
					cur2 := k[1] + string(cur[1])
					tpl2[cur1] += tpl3[cur]
					tpl2[cur2] += tpl3[cur]
					tpl2[cur] -= tpl3[cur]
					break
				}
			}
		}
		cn = make(map[byte]int, 0)
		for t, ti := range tpl2 {
			cn[t[0]] += ti
			cn[t[1]] += ti
		}
		delete(cn, '_')
	}

	for _, t := range cn {
		if t > mmax {
			mmax = t
		}
	}
	for _, t := range cn {
		if t < mmin {
			mmin = t
		}
	}
	return (mmax - mmin) / 2
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
	p1 := part1(lines, 10)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part1(lines, 40)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
