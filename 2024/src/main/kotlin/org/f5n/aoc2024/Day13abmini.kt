package org.f5n.aoc2024

class Day13abmini {
	data class Pos2(val x: Long, val y: Long)
	data class Button(val x: Long, val y: Long)
	data class Setup(val a: Button, val b: Button, val prize: Pos2)
	fun run(args: Array<String>) {
		val m = args[0].readAll().split("\n\n").filter { it.contains("X") }.map {
			val p = it.split("\n").map( fun(line: String) = line.replace(Regex("[XY=,+]"), "").split(" ") )
			Setup(Button(p[0][2].toLong(), p[0][3].toLong()), 
				  Button(p[1][2].toLong(), p[1][3].toLong()),
				  Pos2(p[2][1].toLong(), p[2][2].toLong()))
		}
		var p1 = 0L
		var p2 = 0L

		val solve = fun(it: Setup, pp: Long) : Pair<Long, Long>? {
			val sbx : Long = it.b.y * it.b.x
			val sby = -1L * it.b.x * it.b.y
			if(sbx + sby != 0L) return null
			val l = ( it.b.y * it.a.x ) - ( it.b.x * it.a.y )
			val r = ( it.b.y * (it.prize.x + pp) ) - ( it.b.x * (it.prize.y + pp) )
			val a = r / l
			if (l * a != r) return null
			val b = ((it.prize.x + pp) - a * it.a.x) / it.b.x
			if ( ( a * it.a.x + b * it.b.x ) == it.prize.x + pp) {
				return Pair(a, b)
			}
			return null
		}

		m.forEach { solve(it, 0)?.let { ii -> p1 += 3 * ii.first + ii.second } }
		println("p1: $p1")

		m.forEach {
			solve(it, 10000000000000L)?.let { w ->
				if (w.first < 100L) {
					solve(Setup(it.b, it.a, it.prize), 10000000000000L)?.let { v ->
						p2 += 3 * v.first + v.second
					}
				} else {
					p2 += 3 * w.first + w.second
				}
			}
		}
		println("p2: $p2")
	}
}