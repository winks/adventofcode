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

func contains(w []string, s string) bool {
	for _, a := range w {
		if a == s {
			return true
		}
	}
	return false
}

func contains3(w []string, s string) (bool, map[string]int) {
	b := map[string]int{}
	w2 := make([]string, len(w))
	copy(w2, w)
	w2 = append(w2, s)
	for _, a1 := range w2 {
		if a1[0] < 97 || a1[0] > 122 {
			continue
		}
		for _, a2 := range w2 {
			if a2 == a1 {
				b[a1] += 1
				if b[a1] > 4 {
					return true, b
				}
			}
		}
	}
	bad := 0
	for _, a := range b {
		if a > 1 {
			bad += 1
		}
	}
	return bad > 1, b
}

func part(lines []string, runPart1 bool) int {
	//caves := make(map[string]int)
	paths := [][]string{}
	ways := [][]string{}
	done := [][]string{}
	for _, line := range lines {
		x := strings.Split(line, "-")
		//caves[x[0]] = 0
		//caves[x[1]] = 0
		p1 := []string{x[0], x[1]}
		p2 := []string{x[1], x[0]}

		if x[0] == "start" {
			ways = append(ways, p1)
		} else if x[1] == "start" {
			ways = append(ways, p2)
		} else {
			paths = append(paths, p1)
			paths = append(paths, p2)
		}
	}
	//fmt.Printf("caves %v\n", caves)
	//fmt.Printf("A Z %d %d\n", 'A', 'Z')
	//fmt.Printf("a z %d %d\n", 'a', 'z')
	//fmt.Printf("ways  %v\n", ways)
	//fmt.Printf("paths %v\n", paths)
	
	cur := []string{}
	for len(ways) > 0 {
		cur = ways[0]
		ways = ways[1:]
		////fmt.Printf("\nway  %v -- %v\n", cur, ways)
		for _, p := range paths {
			//fmt.Printf("  look %v + %v\n", cur, p)
			if p[0] == cur[len(cur)-1] {
				if cur[0] == "end" {
					fmt.Printf("      end00 %v + %v\n", cur, p)
					continue
				} else if cur[len(cur)-1] == "end" {
					fmt.Printf("      end01 %v + %v\n", cur, p)
					continue
				}
				
				////fmt.Printf("  cur %v + %v\n", cur, p)
				if p[1] == "end" {
					tmpx := make([]string, len(cur))
					copy(tmpx, cur)
					tmpx = append(tmpx, p[1])
					done = append(done, tmpx)
					//fmt.Printf("    eW %d %v\n", len(ways), ways)
					////fmt.Printf("   DDD %d %v\n", len(done), done)
					continue
				} else {
					// lowercase only once
					if p[1][0] >= 97 && p[1][0] <= 122 {
						cc := false
						if (runPart1) {
							cc = contains(cur, p[1])
						} else {
							cc, _ = contains3(cur, p[1])
						}
						////fmt.Printf("    cur lc %v + %s = %d %v\n", cur, p, cc, cd)
						if !cc {
							//fmt.Printf("    lW   %d . %v\n", len(ways), ways)
							tmpx := make([]string, len(cur))
							copy(tmpx, cur)
							//fmt.Printf("    lW    %v - %v\n", tmpx, cur)
							tmpx = append(tmpx, p[1])
							ways = append(ways, tmpx)
							////fmt.Printf("    lW   %d . %v\n", len(ways), ways)
						} else {
							//fmt.Printf("   weird %v + %v\n", cur, p)
						}
					} else {
						//fmt.Printf("    cur uc %v + %v\n", cur, p)
						//fmt.Printf("    uW   %d . %v\n", len(ways), ways)
						tmpx := make([]string, len(cur))
						copy(tmpx, cur)
						tmpx = append(tmpx, p[1])
						ways = append(ways, tmpx)
						//fmt.Printf("    uW   %d . %v\n", len(ways), ways)
					}
				}
			} else {
				//fmt.Printf("      nope %v + %v\n", cur, p)
			}
		}
	}
	return len(done)
}

func part2(lines []string) int {
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
	p1 := part(lines, true)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part(lines, false)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
