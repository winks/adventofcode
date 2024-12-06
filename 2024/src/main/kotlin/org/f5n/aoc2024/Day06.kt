package org.f5n.aoc2024

import java.nio.file.attribute.PosixFileAttributes

class Day06 {
	private var multi = emptyMap<Pos, List<Pos>>().toMutableMap()

	private fun p1(board: Board, guard1: Pos): List<Pos> {
		multi = emptyMap<Pos, List<Pos>>().toMutableMap()
		var visited = listOf(guard1)
		var dir = Board.direction.N
		var guard = guard1
		while (board.valid(guard)) {
			val ng = when (dir) {
				Board.direction.N -> Pos(guard.x, guard.y - 1)
				Board.direction.E -> Pos(guard.x + 1, guard.y)
				Board.direction.S -> Pos(guard.x, guard.y + 1)
				Board.direction.W -> Pos(guard.x - 1, guard.y)
			}
			if (board.valid(ng) && board.peek(ng) != '#') {
				guard = ng
				if (!visited.contains(guard)) {
					visited += guard
				} else {
					if (multi.containsKey(guard)) {
						multi[guard] = multi[guard]!!.plus(guard)
						if (multi[guard]!!.size > 3) {
							return emptyList()
						}
					} else {
						multi[guard] = listOf(guard)
					}
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
		return visited
	}

	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
		var guard = Pos(0,0)
		//board.print()
		for (y in 0 until board.length) {
			for (x in 0 until board.width) {
				val p = Pos(x, y)
				if (board.peek(p) == '^') {
					guard = p
					break
				}
			}
		}
		val visited = p1(board, guard)
		//println(visited)
		val banned = listOf(visited[0], visited[1])
		var tried = listOf(visited[1])
		var loops = 0
		val nv = visited.toMutableList()
		while (nv.size > 0) {
			val v = nv.removeAt(0)
			if (nv.size % 100 == 0) println("nv: ${nv.size} tried: ${tried.size} v: $v")
			if (banned.contains(v)) continue
			if (tried.contains(v)) continue
			tried += v
			val b = Board(lines)
			val obstacles = b.getNeighbors(v)
			nv.plus(obstacles)
			b.board[v.y][v.x] = '#'
			//b.print()
			val x = p1(b, guard)
			if (x.isEmpty()) {
				loops++
			}
		}
		println("p1 ${visited.size}")
		println("p2 $loops")
	}
}
