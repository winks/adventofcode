package main

import (
	"bufio"
	"fmt"
	"os"
	"reflect"
	"strings"
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

func part1(lines []string) int {
	rv := 0
	for _, line := range(lines) {
		lr := strings.Split(line, "|")
		//left := strings.Split(strings.Trim(lr[0], " "), " ")
		right := strings.Split(strings.Trim(lr[1], " "), " ")
		for _, x := range(right) {
			if (len(x) == 2 || len(x) == 3 || len(x) == 4 || len(x) == 7) {
				rv +=1
			}
		}
		//fmt.Printf("L %v\n", left)
		//fmt.Printf("R %v\n", right)
	}
	return rv
}

func guess(left []string) (string, string, string, string, string, string, string) {
	//n0 := ""
	n1 := ""
	//n2 := ""
	//n3 := ""
	n4 := ""
	//n5 := ""
	//n6 := ""
	n7 := ""
	n8 := ""
	//n9 := ""
	sa := ""
	sb := ""
	sc := ""
	sd := ""
	se := ""
	sf := ""
	sg := ""
	scf := ""
	sbd := ""
	seg := ""
	// find unique
	len6 := []string{}
	len5 := []string{}
	for _, x := range(left) {
		if len(x) == 2 {
			n1 = x
		}
		if len(x) == 3 {
			n7 = x
		}
		if len(x) == 4 {
			n4 = x
		}
		if len(x) == 7 {
			n8 = x
		}
		if len(x) == 6 {
			len6 = append(len6,  x)
		}
		if len(x) == 5 {
			len5 = append(len5, x)
		}
	}
	// find TOPa with 7-1
	for i := 0; i < len(n7); i++ {
		if !strings.Contains(n1, string(n7[i])) {
			sa = string(n7[i])
			break
		}
	}
	// find right side with 7-TOPa
	for i := 0; i < len(n7); i++ {
		if string(n7[i]) != sa {
			scf += string(n7[i])
		}
	}
	// find part of 4 with 4-1
	for i := 0; i < len(n4); i++ {
		if !strings.Contains(n1, string(n4[i])){
			sbd += string(n4[i])
		}
	}
	// find seg with 8-7-4
	seteg := make(map[byte]bool)
	for i := 0; i < len(n8); i++ {
		seteg[n8[i]] = true
	}
	for i := 0; i < len(n7); i++ {
		delete(seteg, n7[i])
	}
	for i := 0; i < len(n4); i++ {
		delete(seteg, n4[i])
	}
	for i := range seteg {
		seg += string(i)
	}

	//fmt.Printf("n0 %v\n", n0)
	//fmt.Printf("n1 %v\n", n1)
	//fmt.Printf("n2 %v\n", n2)
	//fmt.Printf("n3 %v\n", n3)
	//fmt.Printf("n4 %v\n", n4)
	//fmt.Printf("n5 %v\n", n5)
	//fmt.Printf("n6 %v\n", n6)
	//fmt.Printf("n7 %v\n", n7)
	//fmt.Printf("n8 %v\n", n8)
	//fmt.Printf("n9 %v\n", n9)

	scde := ""
	for n := 0; n < len(len6); n++ {
		set6 := make(map[byte]bool)
		for i := 0; i < len(n8); i++ {
			set6[n8[i]] = true
		}
		for i := 0; i < len(len6[n]); i++ {
			delete(set6, len6[n][i])
		}
		for i := range set6 {
			scde += string(i)
		}
		//fmt.Printf("X %v\n", scde)
	}
	// e = scde-4
	sete := make(map[byte]bool)
	for i := 0; i < len(scde); i++ {
		sete[scde[i]] = true
	}
	for i := 0; i < len(n4); i++ {
		delete(sete, n4[i])
	}
	for i := range sete {
		se = string(i)
	}
	// g = seg-se
	setg := make(map[byte]bool)
	for i := 0; i < len(seg); i++ {
		setg[seg[i]] = true
	}
	delete(setg, se[0])
	for i := range setg {
		sg = string(i)
	}
	// d = scde - 1  - e
	setd := make(map[byte]bool)
	for i := 0; i < len(scde); i++ {
		setd[scde[i]] = true
	}
	for i := 0; i < len(n1); i++ {
		delete(setd, n1[i])
	}
	delete(setd, se[0])
	for i := range setd {
		sd = string(i)
	}
	// c = scde - e - d
	setc := make(map[byte]bool)
	for i := 0; i < len(scde); i++ {
		setc[scde[i]] = true
	}
	delete(setc, se[0])
	delete(setc, sd[0])
	for i := range setc {
		sc = string(i)
	}
	// f = scf - c
	setf := make(map[byte]bool)
	for i := 0; i < len(scf); i++ {
		setf[scf[i]] = true
	}
	delete(setf, sc[0])
	for i := range setf {
		sf = string(i)
	}
	// b = sbd - d
	setb := make(map[byte]bool)
	for i := 0; i < len(sbd); i++ {
		setb[sbd[i]] = true
	}
	delete(setb, sd[0])
	for i := range setb {
		sb = string(i)
	}

	////fmt.Printf("_scf %v\n", scf)
	////fmt.Printf("_sbd %v\n", sbd)
	////fmt.Printf("_seg %v\n", seg)
	////fmt.Printf("_sde %v\n", sde)
	//fmt.Printf("sa %v\n", sa)
	//fmt.Printf("sb %v\n", sb)
	//fmt.Printf("sc %v\n", sc)
	//fmt.Printf("sd %v\n", sd)
	//fmt.Printf("se %v\n", se)
	//fmt.Printf("sf %v\n", sf)
	//fmt.Printf("sg %v\n", sg)
	////fmt.Printf("n4 %v\n", n4)
	////fmt.Printf("n6 %v\n", n6)

	return sa, sb, sc, sd, se, sf, sg
}

func convert(s string, m []string) map[byte]bool {
	x := make(map[byte]bool)

	for _, is := range(m) {
		if strings.Contains(s, string(is)) {
			x[is[0]] = true
		}
	}
	return x
}

func part2(lines []string) int {
	rv := 0
	for _, line := range(lines) {
		lr := strings.Split(line, "|")
		left := strings.Split(strings.Trim(lr[0], " "), " ")
		right := strings.Split(strings.Trim(lr[1], " "), " ")

		sa, sb, sc, sd, se, sf, sg := guess(left)
		m := []string{sa, sb, sc, sd, se, sf, sg}

		x0 := make(map[byte]bool)
		x1 := make(map[byte]bool)
		x2 := make(map[byte]bool)
		x3 := make(map[byte]bool)
		x4 := make(map[byte]bool)
		x5 := make(map[byte]bool)
		x6 := make(map[byte]bool)
		x7 := make(map[byte]bool)
		x8 := make(map[byte]bool)
		x9 := make(map[byte]bool)

		x0[sa[0]] = true
		x0[sb[0]] = true
		x0[sc[0]] = true
		x0[se[0]] = true
		x0[sf[0]] = true
		x0[sg[0]] = true

		x1[sc[0]] = true
		x1[sf[0]] = true

		x2[sa[0]] = true
		x2[sc[0]] = true
		x2[sd[0]] = true
		x2[se[0]] = true
		x2[sg[0]] = true

		x3[sa[0]] = true
		x3[sc[0]] = true
		x3[sd[0]] = true
		x3[sf[0]] = true
		x3[sg[0]] = true

		x4[sb[0]] = true
		x4[sc[0]] = true
		x4[sd[0]] = true
		x4[sf[0]] = true

		x5[sa[0]] = true
		x5[sb[0]] = true
		x5[sd[0]] = true
		x5[sf[0]] = true
		x5[sg[0]] = true

		x6[sa[0]] = true
		x6[sb[0]] = true
		x6[sd[0]] = true
		x6[se[0]] = true
		x6[sf[0]] = true
		x6[sg[0]] = true

		x7[sa[0]] = true
		x7[sc[0]] = true
		x7[sf[0]] = true

		x8[sa[0]] = true
		x8[sb[0]] = true
		x8[sc[0]] = true
		x8[sd[0]] = true
		x8[se[0]] = true
		x8[sf[0]] = true
		x8[sg[0]] = true

		x9[sa[0]] = true
		x9[sb[0]] = true
		x9[sc[0]] = true
		x9[sd[0]] = true
		x9[sf[0]] = true
		x9[sg[0]] = true

		rvx := ""
		for i := 0; i < len(right); i++ {
			s := right[i]
			c := convert(s, m)
			//fmt.Printf("! %s %v %v\n", s, c, x3)
			if reflect.DeepEqual(c, x1) {
				rvx += "1"
			} else if reflect.DeepEqual(c, x2) {
				rvx += "2"
			} else if reflect.DeepEqual(c, x3) {
				rvx += "3"
			} else if reflect.DeepEqual(c, x4) {
				rvx += "4"
			} else if reflect.DeepEqual(c, x5) {
				rvx += "5"
			} else if reflect.DeepEqual(c, x6) {
				rvx += "6"
			} else if reflect.DeepEqual(c, x7) {
				rvx += "7"
			} else if reflect.DeepEqual(c, x8) {
				rvx += "8"
			} else if reflect.DeepEqual(c, x9) {
				rvx += "9"
			} else if reflect.DeepEqual(c, x0) {
				rvx += "0"
			}
		}
		//fmt.Printf("! %v\n", rvx)
		rva, err := strconv.Atoi(rvx)
		check(err)
		rv += rva
	}

	return rv
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
