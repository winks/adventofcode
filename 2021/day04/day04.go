package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

type Field struct {
	number string
	done   bool
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

func makeBoard(cur string) []Field {
	board := []Field{}
	c1 := strings.Split(cur, " ")
	for _, v := range c1 {
		v = strings.Trim(v, " ")
		if len(v) < 1 {
			continue
		}
		f := Field{v, false}
		board = append(board, f)
	}
	return board
}

func won(board []Field) bool {
	for i := 0; i < 5; i++ {
		if board[i].done && board[i+5].done && board[i+10].done && board[i+15].done && board[i+20].done {
			return true
		}
		if board[i*5+0].done && board[i*5+1].done && board[i*5+2].done && board[i*5+3].done && board[i*5+4].done {
			return true
		}
	}
	return false
}

func update(board []Field, num string) []Field {
	for i, f := range board {
		if f.number == num {
			board[i].done = true
			return board
		}
	}
	return board
}

func calc(board []Field) int {
	rv := 0
	for _, f := range board {
		if !f.done {
			x, err := strconv.Atoi(f.number)
			check(err)
			rv += x
		}
	}
	return rv
}

func prep(lines []string) ([]string, [][]Field) {
	nums := strings.Split(lines[0], ",")
	boards := [][]Field{}
	cur := ""
	for i := 1; i < len(lines); i++ {
		line := strings.Replace(lines[i], "  ", " ", -1)
		line = strings.Replace(line, "  ", " ", -1)
		line = strings.Trim(line, "\n")
		if len(line) < 3 {
			if i > 1 && len(cur) > 0 {
				boards = append(boards, makeBoard(cur))
				cur = ""
			}
			continue
		}
		cur += " "
		cur += line
	}
	boards = append(boards, makeBoard(cur))
	return nums, boards
}

func part1(lines []string) int {
	nums, boards := prep(lines)

	for _, draw := range nums {
		for i, b := range boards {
			b = update(b, draw)
			if won(b) {
				d, err := strconv.Atoi(draw)
				check(err)
				return d * calc(b)
			}
			boards[i] = b
		}
	}

	return 0
}

func contains(arr []int, i int) bool {
	for _, a := range arr {
		if a == i {
			return true
		}
	}
	return false
}

func part2(lines []string) int {
	nums, boards := prep(lines)
	done_boards := []int{}

	for _, draw := range nums {
		for i, b := range boards {
			b = update(b, draw)
			if won(b) {
				d, err := strconv.Atoi(draw)
				check(err)
				if !contains(done_boards, i) {
					done_boards = append(done_boards, i)
				}
				if len(done_boards) == len(boards) {
					return d * calc(boards[done_boards[len(done_boards)-1]])
				}
				boards[i] = b
			}
		}
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
