package org.f5n.aoc2024

typealias Robot14 = Pair<Pos, Pos>

class Day14 {
	fun run(args: Array<String>) {
		val robots = args[0].readLines()
			.map { it.split(" ") }
			.map {
				val p = it[0].replace("p=","").split(",").map(String::toInt)
				val m = it[1].replace("v=","").split(",").map(String::toInt)
				Pair(Pos(p[0], p[1]), Pos(m[0], m[1]))
			}
		val ww = 101
		val hh = 103
		var b = Board2<Robot14>(ww, hh)
		var b1 = Board2<Robot14>(ww, hh)
		var b2 = Board2<Robot14>(ww, hh)
//		b.print()
		robots.forEach {
//			println("[$it]")
			b.board[it.first.y][it.first.x].add(it)
		}
		var p2 = 0
		for (tick in 1 until 10000) {
			b2 = Board2<Robot14>(ww, hh)
			for (y in 0 until b.length) {
				for (x in 0 until b.width) {
					val r = b.board[y][x]
					r.forEach {
						val p = it.first
						val m = it.second
						val np = Pos(p.x + m.x, p.y + m.y)
						if (b2.valid(np)) {
							b2.board[np.y][np.x].add(Pair(np, m))
						} else {
							val npx = if (np.x < 0) np.x + b.width else if (np.x >= b.width) np.x - b.width else np.x
							val npy = if (np.y < 0) np.y + b.length else if (np.y >= b.length) np.y - b.length else np.y
							val np2 = Pos(npx, npy)
							b2.board[npy][npx].add(Pair(np2, m))
						}

					}
				}
			}
			if (tick == 100) b1.copyFrom(b2)
			if (tick > 7000) {
				val x = b2.getNeighbors(Pos(35, 25)).filter { b2.board[it.y][it.x].isNotEmpty() }
				if (x.size == 4) {
//					println("tick: $tick")
					for (y in 16 until 51) {
						for (x in 19 until 50) {
							val s = b2.board[y][x].size
							if(s > 0) print("$s ") else print("  ")
							p2 = tick
						}
						println()
					}
					break
				}
			}
			b.copyFrom(b2)
		}

		val w2 = b1.width / 2
		val h2 = b1.length / 2
		val p1 = emptyList<Int>().toMutableList()
		var tmp = 0
		for (y in 0 until h2) {
			for (x in 0 until w2) {
				tmp += b1.board[y][x].size
			}
		}
		p1.add(tmp)
		tmp = 0
		for (y in 0 until h2) {
			for (x in w2+1 until b.width) {
				tmp += b1.board[y][x].size
			}
		}
		p1.add(tmp)
		tmp = 0
		for (y in h2+1 until b1.length) {
			for (x in 0 until w2) {
				tmp += b1.board[y][x].size
			}
		}
		p1.add(tmp)
		tmp = 0
		for (y in h2+1 until b1.length) {
			for (x in w2+1 until b1.width) {
				tmp += b1.board[y][x].size
			}
		}
		p1.add(tmp)
//		println(p1)
		println("p1 : ${p1.reduce {a, b -> a * b}}")
		println("p2 : ${p2}")
	}
}
