package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"time"
)

type Point struct {
	y int
	x int
	v int
	f bool
}

type Way struct {
	path []Point
	cost int
}

type ppp []Point

func (p ppp) Len() int {
	return len(p)
}

func (p ppp) Swap(i, j int) {
	p[i], p[j] = p[j], p[i]
}

func (p ppp) Less(i, j int) bool {
	return p[i].v < p[j].v
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

func pp(m [][]Point, print bool) int {
	c := 0
	for y := 0; y < len(m); y++ {
		for x := 0; x < len(m[0]); x++ {
			if print {
				fmt.Printf("%d ", m[y][x].v)
			}
			//if m[y][x].v > 9 && !m[y][x].f {
			//	c += 1
			//}
		}
		if print {
			fmt.Printf("\n")
		}
	}
	if print {
		fmt.Printf("_ [%d]\n", c)
	}
	return c
}

func getne(p Point, lines [][]Point) []Point {
	rv := []Point{}
	if p.x < len(lines[0])-1 {
		rv = append(rv, lines[p.y][p.x+1])
	}
	if p.y < len(lines)-1 {
		rv = append(rv, lines[p.y+1][p.x])
	}
	if p.x > 0 {
		rv = append(rv, lines[p.y][p.x-1])
	}
	if p.y > 0 {
		rv = append(rv, lines[p.y-1][p.x])
	}
	return rv
}

func sum(way []Point) int {
	rv := 0
	for _, w := range way {
		rv += w.v
	}
	return rv
}

func get_path(visi map[Point]Point, cur Point, end Point) []Point {
	tp := []Point{cur}
	//fmt.Printf("GP %v %v\n", len(visi), visi)
	//for aa, vv := range visi {
	//fmt.Printf("__ (%v,%v) (%v,%v)\n", aa.y, aa.x, vv.y, vv.x)
	//}
	cur2 := cur
	for {
		v, ok := visi[cur2]
		//fmt.Printf("GP. %v %v %v\n", cur2, ok, v)
		if ok {
			cur2 = v
			if cur2.y == end.y && cur2.x == end.x {
				break
			}
			tp = append([]Point{cur2}, tp...)
			//delete(visi, cur2)
			//fmt.Printf("GP %v\n", len(visi))
			//fmt.Printf("TP %v -- %v\n", len(tp), tp)
		} else {
			break
		}
	}
	return tp
}

func h(p1 Point, p2 Point) float64 {
	dx := p1.x - p2.x
	dy := p1.y - p2.y
	//fmt.Printf("Ps %v %v %v\n", dx, dy, (dy*dy)+(dx*dx))
	s := math.Sqrt(float64((dy * dy) + (dx * dx)))
	if s < 0 {
		return -1 * s
	}
	return s
}

func part1(lines []string) int {
	cave := make([][]Point, 0)
	for y := 0; y < len(lines); y++ {
		cave = append(cave, []Point{})
		line := lines[y]
		for x := 0; x < len(line); x++ {
			v, err := strconv.Atoi(string(line[x]))
			check(err)
			p := Point{y, x, v, false}
			cave[y] = append(cave[y], p)
		}
	}
	pp(cave, true)
	pos := cave[0][0]
	start := pos
	goal := cave[len(cave)-1][len(cave[0])-1]
	fmt.Printf("S %v\n", pos)
	fmt.Printf("E %v\n", goal)
	open := make([]Point, 0)
	open = append(open, pos)
	fmt.Printf("OS %d - %v\n\n", len(open), open)
	way := make([]Point, 0)
	cameFrom := make(map[Point]Point, 0)
	gscore := make(map[Point]int, 0)
	gscore[pos] = 0
	fscore := make(map[Point]float64)
	fscore[pos] = h(pos, goal)

	fmt.Printf("FS %d - %v\n\n", len(fscore), fscore)

	for len(open) > 0 {
		mmin := -1
		mi := 0
		for ii, vv := range open {
			if mmin < 0 {
				mmin = vv.v
				mi = ii
			}
		}
		//cur := open[0]
		cur := open[mi]
		if cur.y == goal.y && cur.x == goal.x {
			fmt.Printf("### FOUND %v\n", cur)
			way = get_path(cameFrom, cur, start)
			fmt.Printf("### FOUND %v\n", way)
			break
		}
		if len(open) > 1 {
			open = append(open[:mi], open[mi+1:]...)
		} else {
			open = []Point{}
		}
		//open = open[1:]
		ne := getne(cur, cave)

		//fmt.Printf("P %v -- %v\n", cur, open)
		//fmt.Printf("  NE %d - %v\n", len(ne), ne)
		//mmin := 10
		//mp := Point{0, 0, 10, false}
		//sort.Sort(ppp(ne))
		for _, v := range ne {
			gtmp := gscore[cur] + v.v
			vx, ok := gscore[v]
			if (ok && gtmp < vx) || !ok {
				cameFrom[v] = cur
				gscore[v] = gtmp
				fscore[v] = float64(gtmp) + h(v, goal)
				found := false
				for _, vv := range open {
					if vv == v {
						found = true
						break
					}
				}
				//fmt.Printf("  GT %v gs:%v fs:%v f:%v\n", v, gscore[v], fscore[v], found)
				if !found {
					open = append(open, v)
				}
			}
		}
		//fmt.Printf("  W %d - %v\n", len(ways), ways)
		//fmt.Printf("  D %d - %v\n", len(done), done)
	}

	return sum(way)
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
