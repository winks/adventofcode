package org.f5n.aoc2024

class Day10 {
	fun dfs(board: Board, p: Pos, visited: MutableSet<Pos>): MutableSet<Pos> {
		visited.add(p)
		val ne = board.getNeighbors(p)
			.filterNot { board.peek(it) == '.' }
			.filter { board.value(it) == board.value(p) + 1 }
			.filter { !visited.contains(it) }
		for (n in ne) {
			if (board.value(n) == 9) {
				visited.add(n)
			}
			else dfs(board, n, visited)
		}
		return visited
	}
	fun dfs2(board: Board, p: Pos, visited: MutableSet<Pos>, cur: MutableList<Pos>, trails: MutableList<MutableList<Pos>>): MutableList<MutableList<Pos>> {
		visited.add(p)
		cur.add(p)
		val ne = board.getNeighbors(p)
			.filterNot { board.peek(it) == '.' }
			.filter { board.value(it) == board.value(p) + 1 }
			//.filter { !visited.contains(it) }
		for (n in ne) {
			var cur2 : MutableList<Pos> = cur.toMutableList()
			if (board.value(n) == 9) {
				visited.add(n)
				cur.add(n)
				trails.add(cur)
				cur2 = mutableListOf()
			}
			else dfs2(board, n, visited, cur2, trails)
		}
		return trails
	}
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
//		board.print()
		var result = 0
		for (y in 0 until board.length) {
			for (x in 0 until board.width) {
				val p = Pos(x, y)
				if (board.peek(p) == '.') continue
				if (board.value(p) == 0) {
//					println("trailhead at $p")
					val a = dfs(board, p, mutableSetOf())
					result += a.filter { board.value(it) == 9 }.size
				}
			}
		}
		println("p1: $result")
	}
	fun run2(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
		var result = 0
		for (y in 0 until board.length) {
			for (x in 0 until board.width) {
				val p = Pos(x, y)
				if (board.peek(p) == '.') continue
				if (board.value(p) == 0) {
//					println("trailhead at $p")
					val a = dfs2(board, p, mutableSetOf(), mutableListOf(), mutableListOf(mutableListOf(p)))
						.filter { it.size > 1 }
//					println(a)
					result += a.size
				}
			}
		}
		println("p2: $result")
	}
}
