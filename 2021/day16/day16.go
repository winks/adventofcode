package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"time"
)

type Packet struct {
	version int
	typeId  int
	value   int
	opLen   bool
	opNum   bool
	sub     []Packet
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

func parseLit(bits []uint64) (Packet, int) {
	idx := 0
	vers := 0.0
	for i := 2; i >= 0; i-- {
		j := bits[i]
		vers += float64(j) * math.Pow(float64(2), float64(2-i))
	}
	idx += 3
	tid := 0.0
	for i := 5; i >= 3; i-- {
		j := bits[i]
		idx := i - 3
		tid += float64(j) * math.Pow(float64(2), float64(2-idx))
	}
	idx += 3
	if tid != 4 {
		if bits[idx] == 0 {
			return Packet{int(vers), int(tid), 0, true, false, []Packet{}}, idx
		} else {
			return Packet{int(vers), int(tid), 0, false, true, []Packet{}}, idx
		}
	}

	rv := 0
	parts := []int{}
	done := true
	for {
		i := idx
		if i+4 > len(bits)-1 {
			done = false
			break
		}
		xa := 0.0

		for ii := i + 4; ii > i; ii-- {
			j := bits[ii]
			idxx := ii - i
			xa += float64(j) * math.Pow(float64(2), float64(4-idxx))
		}
		parts = append(parts, int(xa))
		idx += 5
		if bits[i] == 0 {
			done = true
			break
		}
	}
	if done {
		for m, p := range parts {
			rv += (p << ((len(parts) - m - 1) * 4))
		}
		return Packet{int(vers), int(tid), rv, false, false, []Packet{}}, idx
	}
	fmt.Printf("xerr %v %v -- %v \n", idx, bits, bits[idx:])
	panic(3)
}

func cho(t int, old int, ps []Packet) int {
	if t == 0 {
		rv := old
		for _, p := range ps {
			rv += p.value
		}
		return rv
	} else if t == 1 {
		rv := old
		if rv == 0 {
			rv = 1
		}
		for _, p := range ps {
			rv *= p.value
		}
		return rv
	} else if t == 2 {
		rv := 9999999
		for _, p := range ps {
			if p.value < rv {
				rv = p.value
			}
		}
		return rv
	} else if t == 3 {
		rv := 0
		for _, p := range ps {
			if p.value > rv {
				rv = p.value
			}
		}
		return rv
	} else if t == 5 {
		if ps[0].value > ps[1].value {
			return 1
		} else {
			return 0
		}
	} else if t == 6 {
		if ps[0].value < ps[1].value {
			return 1
		} else {
			return 0
		}
	} else if t == 7 {
		if ps[0].value == ps[1].value {
			return 1
		} else {
			return 0
		}
	}
	return 0
}

func parse1(bits []uint64, start int) ([]Packet, int) {
	p, pos := parseLit(bits[start:])
	if p.typeId == 4 {
		fmt.Printf(":: basic %v\n", p)
		rv0 := []Packet{p}
		return rv0, pos
	} else if p.opLen {
		pos += 1
		xa := 0.0
		for i := pos + 14; i > pos; i-- {
			j := bits[start+i]
			idx := i - pos
			xa += float64(j) * math.Pow(float64(2), float64(14-idx))
		}
		num := int(xa)
		pos += 15
		fmt.Printf(":: opLen with %v, pos is %v -- %v\n", num, pos, p)
		n0 := 0
		rv0 := []Packet{p}
		for {
			pp, n := parse1(bits[start+pos:], 0)
			n0 += n
			pos += n
			fmt.Printf("  :: subLen %v %v -- %v,%v @ %v\n", rv0[0], pp, n, n0, pos)
			rv0[0].sub = append(rv0[0].sub, pp...)
			if n0 == num {
				break
			}
		}
		rv0[0].value = cho(rv0[0].typeId, rv0[0].value, rv0[0].sub)
		//fmt.Printf("retLen %v\n", rv0)
		return rv0, pos
	} else if p.opNum {
		pos += 1
		xa := 0.0
		for i := pos + 10; i > pos; i-- {
			j := bits[start+i]
			idx := i - pos
			xa += float64(j) * math.Pow(float64(2), float64(10-idx))
		}
		num := int(xa)
		pos += 11
		fmt.Printf(":: opNum with %v, pos is %v -- %v\n", num, pos, p)
		rv0 := []Packet{p}
		for i := 0; i < num; i++ {
			pp, n := parse1(bits[start+pos:], 0)
			fmt.Printf("  :: subNum %v %v -- %v , %v @ %v\n", i, rv0[0], pp, n, pos)
			pos += n
			rv0[0].sub = append(rv0[0].sub, pp...)
		}
		rv0[0].value = cho(rv0[0].typeId, rv0[0].value, rv0[0].sub)
		fmt.Printf("retNum %v\n", rv0)
		return rv0, pos
	}
	return []Packet{}, 0
}

func conv(lines []string) []uint64 {
	line := lines[0]
	fmt.Printf("# %v, %v\n", line, len(line))
	bits := []uint64{}
	for _, ch := range line {
		val, err := strconv.ParseUint(string(ch), 16, 4)
		check(err)
		bits2 := []uint64{}
		for i := 0; i < 8; i++ {
			bits2 = append([]uint64{val & 0x1}, bits2...)
			val = val >> 1
		}
		bits2 = bits2[4:]
		bits = append(bits, bits2...)
	}
	fmt.Printf("# %v - %v\n", bits, len(bits))
	return bits
}

func part1(lines []string) int {
	bits := conv(lines)
	versions := 0
	idx := 0
	for {
		pp, idx := parse1(bits, idx)
		fmt.Printf("pp %v\n", pp)
		for _, p := range pp {
			versions += p.version
		}
		fmt.Printf("vers %v\n", versions)
		rest := bits[idx:]
		fmt.Printf("idx %v %v\n", idx, rest)

		sum := 0
		for _, r := range rest {
			sum += int(r)
		}
		if idx == 0 || sum < 1 {
			return versions
		}

	}
	//fmt.Printf("%v\n", p)
	return 0
}

func part2(lines []string) int {
	bits := conv(lines)
	rv := 0
	for {
		pp, idx := parse1(bits, 0)
		for _, p := range pp {
			rv += p.value
		}
		rv = pp[0].value
		rest := bits[idx:]
		sum := 0
		for _, r := range rest {
			sum += int(r)
		}
		if idx == 0 || sum < 1 || idx == len(bits) {
			return rv
		}
	}
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
	//panic(p1)
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
