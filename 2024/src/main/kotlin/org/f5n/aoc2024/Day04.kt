package org.f5n.aoc2024

class Day04 {
	private fun follow(p: Pos, board: Board, what: String, dir: Board.directionAll): Int {
		//val ind = " ".repeat(4-what.length)
		//println("${ind}follow: $p, $dir, $what, ${what.length}")
		if (what.length == 1 && board.peek(p) == what[0]) return 1
		val ne = board.getNeighborsAll(p).filter { board.getDirection(p, it) == dir }
		//println("$ind $ne")
		var count = 0
		if (board.peek(p) == what[0]) {
			ne.forEach {
				count += follow(it, board, what.substring(1), dir)
			}
		}
		return count
	}
	private fun mas(p: Pos, board: Board) : Int {
		val ne = board.getNeighborsAll(p)
		var found = 0
		ne.forEach {
			if (board.getDirection(p, it) == Board.directionAll.NW) {
				val o1 = board.getOpposite(p, Board.directionAll.NW)
				val x1 = board.getOpposite(p, Board.directionAll.SW)
				val o2 = board.getOpposite(p, Board.directionAll.NE)
				if (board.valid(o1)) {
					//println("mas: $p $it $o1")
					if ((board.peek(it) == 'M' && board.peek(o1) == 'S') ||
						(board.peek(it) == 'S' && board.peek(o1) == 'M')
					) {
						if ((board.peek(x1) == 'M' && board.peek(o2) == 'S') ||
							(board.peek(x1) == 'S' && board.peek(o2) == 'M')
						) {
							found++
						}
					}
				}
			}
		}
		return found
	}
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
		var result1 = 0
		var result2 = 0
		for (y in 0 until board.length) {
			for (x in 0 until board.width) {
				val p = Pos(x, y)
				if (board.peek(p) == 'X') {
					val ne = board.getNeighborsAll(p)
					ne.forEach {
						val dir = board.getDirection(p, it)
						result1 += follow(it, board, "MAS", dir)
					}
				}
				if (board.peek(p) == 'A') {
					result2 += mas(p, board)
				}
			}
		}
		println(result1)
		println(result2)
	}
}
