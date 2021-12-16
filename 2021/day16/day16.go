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
	versub  int
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
			return Packet{int(vers), int(tid), 0, 0, true, false, []Packet{}}, idx
		} else {
			return Packet{int(vers), int(tid), 0, 0, false, true, []Packet{}}, idx
		}
	}

	val := 0
	parts := []int{}
	done := false
	for {
		i := idx
		if i+4 > len(bits)-1 {
			done = false
			break
		}
		xa := 0.0

		for ii := i + 4; ii > i; ii-- {
			j := bits[ii]
			xa += float64(j) * math.Pow(float64(2), float64(i+4-ii))
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
			val += (p << ((len(parts) - m - 1) * 4))
		}
		return Packet{int(vers), int(tid), val, 0, false, false, []Packet{}}, idx
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
		//mt.Printf(":: basic %v\n", p)
		return []Packet{p}, pos
	} else {
		pos += 1
		offset := 10
		if p.opLen {
			offset += 4
		}
		xa := 0.0
		for i := pos + offset; i > pos; i-- {
			j := bits[start+i]
			xa += float64(j) * math.Pow(float64(2), float64(pos+offset-i))
		}
		rle := int(xa)
		pos += offset + 1
		//fmt.Printf(":: opNum with %v, pos is %v -- %v\n", num, pos, p
		bRead := 0
		for i := 0; i < rle; i++ {
			pp, n := parse1(bits[start+pos:], 0)
			//fmt.Printf("  :: subNum %v %v -- %v , %v @ %v\n", i, rv[0], pp, n, pos)
			pos += n
			bRead += n
			p.sub = append(p.sub, pp...)
			if bRead == rle {
				break
			}
		}
		p.value = cho(p.typeId, p.value, p.sub)
		for _, k := range p.sub {
			p.versub += k.version + k.versub
		}
		//fmt.Printf("retNum %v\n", rv0)
		return []Packet{p}, pos
	}
}

func conv(lines []string) []uint64 {
	//fmt.Printf("# %v, %v\n", lines[0], len(lines[0]))
	bits := []uint64{}
	for _, ch := range lines[0] {
		val, err := strconv.ParseUint(string(ch), 16, 4)
		check(err)
		bits2 := []uint64{}
		for i := 0; i < 8; i++ {
			bits2 = append([]uint64{val & 0x1}, bits2...)
			val = val >> 1
		}
		bits = append(bits, bits2[4:]...)
	}
	//fmt.Printf("# %v - %v\n", bits, len(bits))
	return bits
}

func part1(lines []string) int {
	bits := conv(lines)
	pp, pos := parse1(bits, 0)
	rv := pp[0].version + pp[0].versub
	if pos == len(bits) {
		return rv
	}
	sum := 0
	for _, r := range bits[pos:] {
		sum += int(r)
	}
	if sum < 1 {
		return rv
	}
	return 0
}

func part2(lines []string) int {
	bits := conv(lines)
	pp, pos := parse1(bits, 0)
	if pos == len(bits) {
		return pp[0].value
	}
	sum := 0
	for _, r := range bits[pos:] {
		sum += int(r)
	}
	if sum < 1 {
		return pp[0].value
	}
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
