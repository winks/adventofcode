package org.f5n.aoc2024

import java.nio.file.attribute.PosixFileAttributes

class Day06 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
		var result1 = 0
		var result2 = 0
		var guard = Pos(0,0)
		var visited = emptyList<Pos>()
		println(board.width)
		println(board.length)
		//board.print()
		for (y in 0 until board.length) {
			for (x in 0 until board.width) {
				val p = Pos(x, y)
				if (board.peek(p) == '^') {
					guard = p
					println(p)
					visited += p
					break
				}
			}
		}
		var dir = Board.direction.N
		while (board.valid(guard)) {
			val ng = when (dir) {
				Board.direction.N -> Pos(guard.x, guard.y - 1)
				Board.direction.E -> Pos(guard.x + 1, guard.y)
				Board.direction.S -> Pos(guard.x, guard.y + 1)
				Board.direction.W -> Pos(guard.x - 1, guard.y)
			}
			println("ng $ng")
			if (board.valid(ng) && board.peek(ng) != '#') {
				guard = ng
				if (!visited.contains(guard)) {
					visited += guard
				}
			} else if (!board.valid(ng)) {
				break
			} else {
				dir = when (dir) {
					Board.direction.N -> Board.direction.E
					Board.direction.E -> Board.direction.S
					Board.direction.S -> Board.direction.W
					Board.direction.W -> Board.direction.N
				}
			}
		}
		println(visited)
		println(visited.size)
	}
}
