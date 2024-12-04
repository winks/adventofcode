package org.f5n.aoc2024

import jdk.internal.icu.lang.UCharacter.getDirection

class Day04 {
	private fun follow(p: Pos, board: Board, what: String, dir: Board.directionAll): Int {
		val ind = " ".repeat(4-what.length)
		println("${ind}follow: $p, $dir, $what, ${what.length}")
		if (what.length == 1 && board.peek(p) == what[0]) return 1
		val ne = board.getNeighborsAll(p).filter { board.getDirection(p, it) == dir }
		println("$ind $ne")
		var count = 0
		if (board.peek(p) == what[0]) {
			ne.forEach {
				count += follow(it, board, what.substring(1), dir)
			}
		}
		return count
	}
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
		var result = 0
		for (y in 0 until board.length) {
			for (x in 0 until board.width) {
				val p = Pos(x, y)
				//result += check(p, board, "XMAS")
				if (board.peek(p) == 'X') {
					val ne = board.getNeighborsAll(p)
					ne.forEach {
						val dir = board.getDirection(p, it)
						result += follow(it, board, "MAS", dir)
					}
				}
			}
		}
		println(result)
	}
}
