package main

import (
	"bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
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

func isNum(c []byte) (int, error) {
	nre := regexp.MustCompile(`\d`)
	if nre.Match(c) {
		num, err := strconv.Atoi(string(c))
		if err != nil {
			return 0, err
		}
		return num, nil
	} else {
		return 0, errors.New("not isNum")
	}
}

func nextNum(s string) ([3]int, error) {
	for i2, c2 := range s {
		n2, err := isNum([]byte{byte(c2)})
		if err != nil {
			continue
		}
		if i2+2 > len(s) {
			return [3]int{n2, i2, 0}, nil
		}
		n3, err := isNum([]byte{byte(c2), byte(s[i2+1])})
		if err != nil {
			return [3]int{n2, i2, 1}, nil
		}
		return [3]int{n3, i2, 0}, nil
	}
	return [3]int{}, errors.New("not nextNum")
}

func splitter(n int) string {
	if n < 10 {
		return fmt.Sprintf("%d", n)
	}
	left := n / 2
	right := n / 2
	if n%2 == 1 {
		right += 1
	}
	return fmt.Sprintf("[%d,%d]", left, right)
}

func reduce(line string) (string, error) {
	opened := 0
	lastNums := [][3]int{}
	left := [3]int{}
	right := [3]int{}
	for i := 0; i < len(line)-1; i++ {
		c := line[i]
		if c == '[' {
			opened++
		} else if c == ',' {
		} else if c == ']' && opened <= 4 {
			opened--
		} else if c == ']' && opened > 4 {
			right = lastNums[len(lastNums)-1]
			left = lastNums[len(lastNums)-2]
			// nothing on the left side
			if len(lastNums) < 3 {
				fmt.Printf("! RED1  %v\n", line)
				begin := line[0:left[1]-1] + "0"
				rest := line[i+1:]
				fmt.Printf("! RED1b %v \n", begin)
				fmt.Printf("! RED1r     %v \n", rest)
				next, err := nextNum(rest)
				check(err)
				newNum02 := fmt.Sprintf("%d", next[0]+right[0])
				endTmp := next[1]
				if next[0] > 9 {
					endTmp++
				}
				endLine := "" + rest[0:next[1]] + newNum02 + rest[endTmp+1:]
				fmt.Printf("! RED1e     %v \n", endLine)
				fmt.Printf("! RED1! %v \n", begin+endLine)
				return begin + endLine, nil
			}
			rightMost := true
			rest := line[i+1:]
			for _, c2 := range rest {
				if c2 != ']' {
					rightMost = false
					break
				}
			}
			// nothing on the right side
			if rightMost {
				fmt.Printf("! RED2  %v  \n", line)
				prevNum := lastNums[len(lastNums)-3]
				newNum := fmt.Sprintf("%d", prevNum[0]+left[0])
				line = line[0:prevNum[1]] + newNum + ",0" + rest
				fmt.Printf("! RED2! %v  \n", line)
				return line, nil
			} else {
				// in the middle
				prevNum := lastNums[len(lastNums)-3]
				begin := line[0 : left[1]-1]
				fmt.Printf("! RED3   %v\n", line)
				fmt.Printf("! RED3<  %v\n", begin)
				fmt.Printf("! RED3>                            %v \n", rest)
				fmt.Printf("! RED3#  ::%v | < %v , %v >\n", prevNum, left, right)

				newNum01 := fmt.Sprintf("%d", prevNum[0]+left[0])
				next, err := nextNum(rest)
				check(err)
				newNum02 := fmt.Sprintf("%d", next[0]+right[0])

				endTmp := next[1]
				if next[0] > 9 {
					endTmp++
				}

				begTmp := prevNum[1]
				beginLine1 := begin[0:begTmp]
				begTmp += prevNum[2]
				beginLine2 := begin[begTmp+1:]
				fmt.Printf("! RED3b %v\n", beginLine1)
				fmt.Printf("! RED3_ <%v>\n", newNum01)
				fmt.Printf("! RED3b %v\n", beginLine2)

				endLine := "" + rest[0:next[1]] + newNum02 + rest[endTmp+1:]
				fmt.Printf("! RED3e      %v\n", endLine)
				line2 := beginLine1 + newNum01 + beginLine2 + "0" + endLine

				fmt.Printf("! RED3!  %v\n", line)
				return line2, nil
			}
		} else {
			fmt.Printf("! else %v @ %v/%v | %v \n", string(c), i, len(line)-1, line[0:i])
			nre := regexp.MustCompile(`\d`)
			sm1 := []byte{byte(c)}
			if i+1 < len(line) {
				sm2 := []byte{line[i+1]}
				if nre.Match(sm2) {
					sm1 = append(sm1, sm2[0])
				}
			}
			n2, err := isNum(sm1)
			check(err)

			num := [3]int{n2, i, len(sm1) - 1}
			fmt.Printf("! else num %v \n", num)
			lastNums = append(lastNums, num)
			if num[0] > 9 {
				i++
			}
		}
		fmt.Printf("! %v :: op: %v\n", string(c), opened)
		//if opened == 0
	}
	return line, nil
}

func splitit(line string) string {
	nre := regexp.MustCompile(`\d{2}`)
	for i := 0; i < len(line)-1; i++ {
		//fmt.Printf("S %v/%v\n", i, len(line))
		b := []byte{line[i], line[i+1]}
		if nre.Match(b) {
			n, err := nextNum(string(b))
			check(err)
			return line[0:i] + splitter(n[0]) + line[i+2:]
		}
	}
	return line
}

func mag(s string) int {
	nre := regexp.MustCompile(`\[\d+,\d+\]`)
	for {
		lastComma := 0
		lastOpen := 0
		s2 := ""
		for i := 0; i < len(s); i++ {
			c := s[i]
			if c == '[' {
				lastOpen = i
			} else if c == ',' {
				lastComma = i
			} else if c == ']' {
				sm := s[lastOpen : i+1]
				if nre.Match([]byte(sm)) {
					left, err := strconv.Atoi(string(s[lastOpen+1 : lastComma]))
					check(err)
					right, err := strconv.Atoi(string(s[lastComma+1 : i]))
					check(err)
					if len(s[0:lastOpen]) < 1 && len(s[i+1:]) < 1 {
						return 3*left + 2*right
					}
					s2 = s[0:lastOpen] + fmt.Sprintf("%d", 3*left+2*right) + s[i+1:]
					break
				}
			}
		}
		s = s2
	}
}

func part1(lines []string) int {
	resultLine := ""
	lastLine := ""
	for i, linex := range lines {
		line := ""
		if i == 0 {
			lastLine = linex
			continue
		} else {
			line = "[" + lastLine + "," + linex + "]"
		}
		for {
			fmt.Printf("R11    %v\n", line)
			line2, err := reduce(line)
			check(err)
			fmt.Printf("R12    %v\n", line2)
			if line2 == line {
				line2 = splitit(line)
				if line2 == line {
					fmt.Printf("R17    %v \n", line)
					break
				}
				fmt.Printf("R18    %v \n", line2)
				line = line2
			}
			line = line2
		}
		lastLine = line
		resultLine = line
	}
	fmt.Printf("RESULT %v\n", resultLine)
	return mag(resultLine)
}

func part2(lines []string) int {
	mx := 0
	for _, line1 := range lines {
		for _, line2 := range lines {
			if line1 == line2 {
				continue
			}
			res := part1([]string{line1, line2})
			if res > mx {
				mx = res
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
