package org.f5n.aoc2024

import kotlin.math.abs

typealias PosDir = Pair<Pos, Board2.direction>

class Day16 {
	data class Tile(val value: Char, val direction: Board2.direction = Board2.direction.E)

	fun run(args: Array<String>) {
		val consFn = fun(x: Char): Tile {
			return when (x) {
				'.' -> Tile(x, Board2.direction.E)
				'S' -> Tile(x, Board2.direction.E)
				'E' -> Tile(x, Board2.direction.E)
				'#' -> Tile(x, Board2.direction.E)
				else -> throw Exception("Invalid tile")
			}
		}
		val pp = fun(b: Board2<Tile>) {
			for (y in 0 until b.length) {
				for (x in 0 until b.width) {
					val s = b.board[y][x].first()
					print(s.value)
					if (s.value == 'S') print(s.direction.toString().toLowerCase()) else print(" ")
				}
				println()
			}
		}
		val getMatches = fun(s: Char, board: Board2<Tile>) : List<Pos> {
			var rv: List<Pos> = emptyList<Pos>().toMutableList()
			for (y in 0 until board.length) {
				for (x in 0 until board.width) {
					if (board.board[y][x].first().value == s) {
						rv = rv.plus(Pos(x, y))
					}
				}
			}
			return rv.toList()
		}

		val lines = args[0].readLines()
		val board = Board2.from(lines, consFn)
//		pp(board)
		val start = getMatches('S', board).first()
		val end = getMatches('E', board).first()
		println("start: $start end: $end")

		val (cf, cost) = aStar(board, Pair(start, Board2.direction.E), end)
//		println(cf)
//		println(cost)
		for (dd in listOf(Board2.direction.N, Board2.direction.E, Board2.direction.S, Board2.direction.S)) {
			var cur1 = Pair(end, dd)
			if(cost[cur1] != null) {
				val r = cost[cur1]!!
				println("co1 $dd $cur1 ${r}")
//				while (cf.containsKey(cur1) && cf[cur1] != null) {
//					println("$cur1 <- ${cf[cur1]} (${cost[cur1]})")
//					cur1 = cf[cur1]!!
//				}
//				println("co1 $dd ${r}")
			}
		}
	}

	fun heuristic(p1: Pos, p2: Pos): Int {
		return abs(p1.x - p2.x) + abs(p1.y - p2.y)
	}

	fun aStar(board: Board2<Tile>, start: PosDir, end: Pos): Pair<Map<PosDir,PosDir?>, Map<PosDir, Int>> {
		val frontier = mutableMapOf<Int,List<PosDir>>()
		frontier.put(0, listOf(start))
		val cameFrom = emptyMap<PosDir, PosDir?>().toMutableMap()
		val costSoFar = emptyMap<PosDir, Int>().toMutableMap()
		cameFrom[start] = null
		costSoFar[start] = 0

		while (frontier.isNotEmpty()) {
			val low = frontier.keys.min()
			val currentList = frontier.remove(low)
			val current = currentList!!.first()
			if (currentList.size > 1) {
				frontier.put(low, currentList.drop(1))
			}
			if (current.first == end) {
				break
			}
			for (next in board.getNeighbors(current.first)) {
				if (board.board[next.y][next.x].first().value == '#') continue
				var newCost = costSoFar[current]!! + 1
				val dir = board.getDirection(current.first, next)
				val curDir = current.second
				val p = Pair(curDir, dir)
				if (curDir != dir) {
					newCost += when (p) {
						Pair(Board2.direction.E, Board2.direction.S) -> 1000
						Pair(Board2.direction.E, Board2.direction.N) -> 1000
						Pair(Board2.direction.S, Board2.direction.E) -> 1000
						Pair(Board2.direction.S, Board2.direction.W) -> 1000
						Pair(Board2.direction.W, Board2.direction.S) -> 1000
						Pair(Board2.direction.W, Board2.direction.N) -> 1000
						Pair(Board2.direction.N, Board2.direction.E) -> 1000
						Pair(Board2.direction.N, Board2.direction.W) -> 1000

						Pair(Board2.direction.E, Board2.direction.W) -> 2000
						Pair(Board2.direction.S, Board2.direction.N) -> 2000
						Pair(Board2.direction.W, Board2.direction.E) -> 2000
						Pair(Board2.direction.N, Board2.direction.S) -> 2000
						else -> 0
					}
				}

				val np = Pair(next, dir)
//				println("cur: $current next: $next ${board.board[next.y][next.x].first().value} - cost $newCost - np $np")
				if (!costSoFar.containsKey(np) || newCost < costSoFar[np]!!) {
					costSoFar[np] = newCost
					val priority = newCost ///+ heuristic(next, end)
					if (!frontier.containsKey(priority)) {
						frontier.put(priority, listOf(np))
					} else {
						frontier.put(priority, frontier[priority]!!.plus(np))
					}
					cameFrom[np] = current
				}
			}
		}
		return Pair(cameFrom, costSoFar)
	}
}
