package main

// after 12h of fighting my mess of a code I looked for a solution that was
// close to mine and then I adapted the following code:
// https://github.com/dankoo97/AoC_2021/blob/06936b9707cdae0f2d88c46f2fda1899b6af1a07/BeaconScanner.py

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

type Point struct {
	x, y, z int
}

type Scanner struct {
	num     int
	beacons map[Point]bool
	pos     Point
}

type MapKey struct {
	trans [3]int
	perm  [3]int
}

func add(p1 Point, p2 Point) Point {
	return Point{p1.x + p2.x, p1.y + p2.y, p1.z + p2.z}
}

func sub(p1 Point, p2 Point) Point {
	return Point{p1.x - p2.x, p1.y - p2.y, p1.z - p2.z}
}

func mul(p1 Point, t [3]int) Point {
	return Point{p1.x * t[0], p1.y * t[1], p1.z * t[2]}
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

func getTrans() [][3]int {
	trans := [][3]int{}
	trans = append(trans, [3]int{1, 1, 1})
	trans = append(trans, [3]int{-1, 1, 1})
	trans = append(trans, [3]int{1, -1, 1})
	trans = append(trans, [3]int{1, 1, -1})
	trans = append(trans, [3]int{1, -1, -1})
	trans = append(trans, [3]int{-1, 1, -1})
	trans = append(trans, [3]int{-1, -1, 1})
	trans = append(trans, [3]int{-1, -1, -1})
	return trans
}

func getPerm() [][3]int {
	r := [][3]int{}
	r = append(r, [3]int{0, 1, 2})
	r = append(r, [3]int{0, 2, 1})
	r = append(r, [3]int{1, 0, 2})
	r = append(r, [3]int{1, 2, 0})
	r = append(r, [3]int{2, 0, 1})
	r = append(r, [3]int{2, 1, 0})
	return r
}

func getPermP(p [3]int, pe [3]int) Point {
	p2 := Point{}
	p2.x = p[pe[0]]
	p2.y = p[pe[1]]
	p2.z = p[pe[2]]
	return p2
}

func manh(p1 Point, p2 Point) int {
	dx := math.Abs(float64(p1.x) - float64(p2.x))
	dy := math.Abs(float64(p1.y) - float64(p2.y))
	dz := math.Abs(float64(p1.z) - float64(p2.z))
	return int(dx + dy + dz)
}

func find(s1 Scanner, s2 Scanner) Scanner {
	m := make(map[MapKey]map[Point]int, 0)
	for _, t := range getTrans() {
		for _, pe := range getPerm() {
			mk := MapKey{t, pe}
			m[mk] = make(map[Point]int, 0)
			for p1 := range s1.beacons {
				for p2 := range s2.beacons {
					np2 := getPermP([3]int{p2.x, p2.y, p2.z}, pe)
					np := add(p1, mul(np2, t))
					m[mk][np]++
				}
			}
			for k, v := range m[mk] {
				if v >= 12 {
					//fmt.Printf("XXX %v %v\n", k, v)
					s2.pos = k
					b2 := make(map[Point]bool, 0)
					for b := range s2.beacons {
						nb2 := getPermP([3]int{b.x, b.y, b.z}, pe)
						nb := sub(s2.pos, mul(nb2, t))
						b2[nb] = true
					}
					s2.beacons = b2
					return s2
				}
			}
		}
	}
	return Scanner{}
}

func part1(lines []string) (int, []Scanner) {
	scanners := []Scanner{}
	cur := Scanner{0, make(map[Point]bool, 0), Point{}}
	for _, line := range lines {
		if len(line) < 1 {
			scanners = append(scanners, cur)
			cur = Scanner{0, make(map[Point]bool, 0), Point{}}
		} else if line[0:2] == "--" {
			p := strings.Split(line, " ")
			num, err := strconv.Atoi(p[2])
			check(err)
			cur.num = num
		} else {
			p := strings.Split(line, ",")
			x, err := strconv.Atoi(p[0])
			check(err)
			y, err := strconv.Atoi(p[1])
			check(err)
			z := 0
			if len(p) > 2 {
				z, err = strconv.Atoi(p[2])
				check(err)
			}
			pt := Point{x, y, z}
			cur.beacons[pt] = true
		}
	}
	scanners = append(scanners, cur)
	scanners[0].pos = Point{0, 0, 0}

	done := make(map[int]bool, 0)
	done[0] = true
	allb := make(map[Point]bool)
	for i := range scanners[0].beacons {
		allb[i] = true
	}
	//fmt.Printf("LEN  %v\n", len(allb))
	//fmt.Printf("DONE %v\n", done)

	for len(done) < len(scanners) {
		for k := range done {
			for i := 0; i < len(scanners); i++ {
				if done[i] == true {
					continue
				}
				//fmt.Printf("NOW %v PLUS %v\n", k, i)
				cur := find(scanners[k], scanners[i])
				scanners[i].pos = cur.pos
				//fmt.Printf("F %v\n", cur)
				if len(cur.beacons) > 0 {
					done[cur.num] = true
					//fmt.Printf("DONE  %v\n", len(done))
					for i := range cur.beacons {
						allb[i] = true
					}
					scanners[i].beacons = allb
					scanners[k].beacons = allb
				}
				//fmt.Printf("LEN %v\n", len(allb))
			}
		}
	}
	return len(allb), scanners
}

func part2(sc []Scanner) int {
	mx := 0
	for _, s1 := range sc {
		for _, s2 := range sc {
			m := manh(s1.pos, s2.pos)
			if m > mx {
				mx = m
			}
		}
	}
	return mx
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
	p1, sc := part1(lines)
	elapsed1 := time.Since(timeStart1)
	fmt.Printf("# Part1   %s\n", elapsed1)
	timeStart2 := time.Now()
	p2 := part2(sc)
	elapsed2 := time.Since(timeStart2)
	fmt.Printf("# Part2   %s\n", elapsed2)
	fmt.Printf("# Total   %s\n", time.Since(timeStart))

	fmt.Printf("Part 1: %d\n", p1)
	fmt.Printf("Part 2: %d\n", p2)
}
