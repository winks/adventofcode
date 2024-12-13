package org.f5n.aoc2024

class Day13 {
	data class Pos2(val x: Long, val y: Long)
	data class Button(val x: Long, val y: Long)
	data class Setup(val a: Button, val b: Button, val prize: Pos2)
	fun run(args: Array<String>) {
		val m = mutableListOf<Setup>()
		val lines = args[0].readLines()
		var i = 0
		while (i < lines.size) {
			var line = lines[i]
			var parts = line.replace(Regex("[XY=,+]"), "").split(" ")
//			println(parts)
			var a = Button(0, 0)
			var b = Button(0, 0)
			var s = Setup(a, b, Pos2(0, 0))
			if (line.contains("A")) {
				a = Button(parts[2].toLong(), parts[3].toLong())
				i++
				line = lines[i]
				parts = line.replace(Regex("[XY=,+]"), "").split(" ")
			}
			if (line.contains("B")) {
				b = Button(parts[2].toLong(), parts[3].toLong())
				i++
				line = lines[i]
				parts = line.replace(Regex("[XY=,+]"), "").split(" ")
			}
			if (line.contains("Prize")) {
				s = Setup(a, b, Pos2(parts[1].toLong(), parts[2].toLong()))
				i += 2
			}
//			println("[$s]")
			m.add(s)
		}
		var p1 = 0L
		var p2 = 0L
		m.forEach {
			val sol = mutableListOf<Pair<Long, Long>>()
			for (a in 0 until 101) {
				for (b in 0 until 101) {
					if (a * it.a.x + b * it.b.x == it.prize.x && a * it.a.y + b * it.b.y == it.prize.y) {
						sol.add(Pair(a.toLong(), b.toLong()))
//						println("[$a, $b]")
					}
				}
			}
			sol.minOfOrNull { it.first * 3 + it.second }?.let { p1 += it }
		}
		println("p1: $p1")

		val solve = fun(it: Setup) : Pair<Long, Long>? {
			val pp = 10000000000000L
//			println("  $it")
			val rx : Long = it.b.y * (it.prize.x + pp)
			val sax : Long = it.b.y * it.a.x
			val sbx : Long = it.b.y * it.b.x

			val ry = -1L * it.b.x * (it.prize.y + pp)
			val say = -1L * it.b.x * it.a.y
			val sby = -1L * it.b.x * it.b.y
//			println("  $sbx $sby $sax $say ")
			if(sbx + sby == 0L) {
				val l = sax + say
				val r = rx + ry
				val a = r / l
				if (l * a == r) {
					val b = ((it.prize.x + pp) - a * it.a.x) / it.b.x
					val c = a * it.a.x + b * it.b.x
					if (c == it.prize.x + pp )  {
						if (a < 100) return Pair(0, 0)
						else return Pair(a, b)
					}
//					else println("nope $c != ${it.prize.x + pp}")
//					if (c == it.prize.x + pp) println("  aaa $a $b $c")
//					if (a < 100 || b < 100) println("  aaaa $a $b ")
				}
			}
			return null
		}

		m.forEach {
			val r = solve(it)
			if (r != null) {
				if (r.first == 0L) {
					val r2 = solve(Setup(it.b, it.a, it.prize))
					if (r2 != null) {
						p2 += 3 * r2.first + r2.second
					}
				} else {
					p2 += 3 * r.first + r.second
				}
			}

		}
		println("p2: $p2")
	}
}