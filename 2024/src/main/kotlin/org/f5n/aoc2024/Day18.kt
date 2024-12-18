package org.f5n.aoc2024

import org.f5n.aoc2024.Day16.Tile

class Day18 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
			.map { it.split(",").map(String::toInt) }
		val dim = if (lines.size < 1000) 7 else 71
		val p1Round = if (lines.size < 1000) 11 else 1023
		val rounds = lines.size
		val board = Board.fromDim(dim.toLong(), dim.toLong())
//		board.print()
		board.board[0][0] = 'S'
		board.board[dim-1][dim-1] = 'E'
		var p1 = 0
		var p2 = ""
		for (i in 0 until rounds) {
			if (lines[i][0] > dim-1 || lines[i][1] > dim-1) {
				break
			}
			board.board[lines[i][1]][lines[i][0]] = '#'
			val (_, cost) = aStar(board, Pos(0,0), Pos(dim-1, dim-1))
			val cst = cost[Pos(dim-1, dim-1)]
//			println("$i  $cst ${lines[i]}")
			if (cst == null) {
				p2 = lines[i].joinToString(",")
				break
			}
			if (i == p1Round) p1 = cst
		}
//		board.print()
		println("p1: $p1")
		println("p2: $p2")
	}

	private fun aStar(board: Board, start: Pos, end: Pos): Pair<Map<Pos,Pos?>, Map<Pos, Int>> {
		val frontier = mutableMapOf<Int,List<Pos>>()
		frontier[0] = listOf(start)
		val cameFrom = emptyMap<Pos, Pos?>().toMutableMap()
		val costSoFar = emptyMap<Pos, Int>().toMutableMap()
		cameFrom[start] = null
		costSoFar[start] = 0

		while (frontier.isNotEmpty()) {
			val low = frontier.keys.min()
			val currentList = frontier.remove(low)
			val current = currentList!!.first()
			if (currentList.size > 1) {
				frontier[low] = currentList.drop(1)
			}
			if (current == end) {
				break
			}
			for (next in board.getNeighbors(current)) {
				if (board.board[next.y][next.x] == '#') continue
				var newCost = costSoFar[current]!! + 1

				if (!costSoFar.containsKey(next) || newCost < costSoFar[next]!!) {
					costSoFar[next] = newCost
					val priority = newCost ///+ heuristic(next, end)
					if (!frontier.containsKey(priority)) {
						frontier.put(priority, listOf(next))
					} else {
						frontier.put(priority, frontier[priority]!!.plus(next))
					}
					cameFrom[next] = current
				}
			}
		}
		return Pair(cameFrom, costSoFar)
	}
}
