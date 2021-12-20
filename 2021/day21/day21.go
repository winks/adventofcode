package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type Pair struct {
	pos   int
	score int
}

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

func step(die int, pos int) (int, int) {
	tmp := 0
	for i := 0; i < 3; i++ {
		die++
		tmp += die
		if die >= 100 {
			die = 0
		}
	}
	return die, tmp
}

func part1(lines []string) int {
	p1 := strings.Split(lines[0], " ")
	p2 := strings.Split(lines[1], " ")
	p1p, err := strconv.Atoi(p1[4])
	check(err)
	p2p, err := strconv.Atoi(p2[4])
	check(err)

	p1s := 0
	p2s := 0
	die := 0
	diet := 0
	rolls := 0
	tmp := 0
	//fmt.Printf("D: %3v   P1p: %2v   P1s:%3v\n", die, p1p, p1s)
	//fmt.Printf("D: %3v   P2p: %2v   P2s:%3v\n==========================\n", die, p2p, p2s)
	for {
		diet, tmp = step(die, p1p)
		if diet < die {
			rolls++
		}
		die = diet
		if p1p+tmp > 10 {
			p1p = (p1p + tmp) % 10
			if p1p < 1 {
				p1s += 10
			}
		} else {
			p1p += tmp
		}
		p1s += p1p
		//fmt.Printf("D: %3v   P1p: %2v   P1s:%3v  _ %2v\n", die, p1p, p1s, tmp)
		if p1s >= 1000 {
			break
		}

		diet, tmp = step(die, p2p)
		if diet < die {
			rolls++
		}
		die = diet
		if p2p+tmp > 10 {
			p2p = (p2p + tmp) % 10
			if p2p < 1 {
				p2s += 10
			}
		} else {
			p2p += tmp
		}
		p2s += p2p
		//fmt.Printf("D: %3v   P2p: %2v   P2s:%3v  _ %2v\n\n", die, p2p, p2s, tmp)
		if p2s >= 1000 {
			break
		}
	}

	//fmt.Printf("DF: %v   P1s: %v   P1p:%v\n", die, p1s, p1p)
	//fmt.Printf("DF: %v   P2s: %v   P2p:%v x %v\n", die, p2s, p2p, (die + rolls*100))
	if p2s < p1s {
		return p2s * (die + rolls*100)
	} else {
		return p1s * (die + rolls*100)
	}
}

func part2(lines []string) int {
	p1 := strings.Split(lines[0], " ")
	p2 := strings.Split(lines[1], " ")
	p1p, err := strconv.Atoi(p1[4])
	check(err)
	p2p, err := strconv.Atoi(p2[4])
	check(err)
	fmt.Printf("P1 %v - P2 %v\n", p1p, p2p)

	univ0 := make(map[int]int, 0)
	univ0[3] = 1
	univ0[4] = 3
	univ0[5] = 6
	univ0[6] = 7
	univ0[7] = 6
	univ0[8] = 3
	univ0[9] = 1
	return 0
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
