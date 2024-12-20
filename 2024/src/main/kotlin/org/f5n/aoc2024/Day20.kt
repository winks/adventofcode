package org.f5n.aoc2024

class Day20 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
		val s = board.getMatches("S").first()
		val e = board.getMatches("E").first()

		val (_, cost) = aStar(board, s, e)
		val base = cost[e]!!
		println("base cost: $base")
		val p1 = emptyMap<Int, MutableSet<Pair<Pos, Pos>>>().toMutableMap()
		for (y in 1..<board.length-1) {
			for (x in 1..<board.width-1) {
				val nc = mutate(board, x, x, y, y+1, base, s, e)
				if (nc < base) {
					val n = Pair(Pos(x, y), Pos(x, y+1))
					if (!p1.containsKey(nc)) {
						p1[nc] = emptySet<Pair<Pos, Pos>>().toMutableSet()
					}
					p1[nc]?.add(n)
				}
				val nc1 = mutate(board, x, x, y, y-1, base, s, e)
				if (nc1 < base) {
					val n = Pair(Pos(x, y), Pos(x, y-1))
					if (!p1.containsKey(nc1)) {
						p1[nc1] = emptySet<Pair<Pos, Pos>>().toMutableSet()
					}
					p1[nc1]?.add(n)
				}
				val nc2 = mutate(board, x, x+1, y, y, base, s, e)
				if (nc2 < base) {
					val n = Pair(Pos(x, y), Pos(x+1, y))
					if (!p1.containsKey(nc2)) {
						p1[nc2] = emptySet<Pair<Pos, Pos>>().toMutableSet()
					}
					p1[nc2]?.add(n)
				}
				val nc3 = mutate(board, x, x-1, y, y, base, s, e)
				if (nc3 < base) {
					val n = Pair(Pos(x, y), Pos(x-1, y))
					if (!p1.containsKey(nc3)) {
						p1[nc3] = emptySet<Pair<Pos, Pos>>().toMutableSet()
					}
					p1[nc3]?.add(n)
				}
			}
		}
//		p1.forEach{ println("${it.key}   ${base-it.key}  =  ${it.value.size}") }
//		p1[82]?.forEach { println(it) }
		println("p1 all: ${p1.map { it.value.size }.sum()}")
		println("p1 100: ${p1.filter { base-it.key >= 100 }.map { it.value.size }.sum()}")

	}
	private fun mutate (board: Board, x: Int, x2: Int, y: Int, y2: Int, cost: Int, s: Pos, e: Pos) : Int {
		val b = board.copy()
		if (b.peek(Pos(x, y)) == '#' && b.peek(Pos(x2, y2)) != '#') {
			b.board[y][x] = '.'
			b.board[y2][x2] = '.'
		}
		val (cf, c) = aStar(b, s, e)
		val nc = c[e]
		val p = getPath(cf, s, e)
		val cond = cf[Pos(x2, y2)] == Pos(x, y) && p.contains(Pos(x,y)) && p.contains(Pos(x2, y2))
//		if (nc != null && nc == cost -2 && cond) {
//			b.board[y][x] = '1'
//			b.board[y2][x2] = '2'
//			b.print()
//			println(" ${cf[Pos(x, y)]} ${cf[Pos(x2, y2)]} ")
//			println()
//		}
		if (nc != null && nc < cost && cond) {
			return nc
		}
		return cost
	}
	private fun getPath(cf: Map<Pos, Pos?>, start: Pos, final1: Pos) : List<Pos> {
		val p2l = emptyList<Pos>().toMutableList()
		var final = final1
		while (cf.containsKey(final) && cf[final] != null) {
			p2l.add(final)
			final = cf[final]!!
		}
		p2l.add(start)
		return p2l.reversed()
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
				val newCost = costSoFar[current]!! + 1

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
