package org.f5n.aoc2024

data class Button(val x: Int, val y: Int)
data class Setup(val a: Button, val b: Button, val prize: Pos)

class Day13 {
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
			var s = Setup(a, b, Pos(0,0))
			if (line.contains("A")) {
				a = Button(parts[2].toInt(), parts[3].toInt())
				i++
				line = lines[i]
				parts = line.replace(Regex("[XY=,+]"), "").split(" ")
			}
			if (line.contains("B")) {
				b = Button(parts[2].toInt(), parts[3].toInt())
				i++
				line = lines[i]
				parts = line.replace(Regex("[XY=,+]"), "").split(" ")
			}
			if (line.contains("Prize")) {
				s = Setup(a, b, Pos(parts[1].toInt(), parts[2].toInt()))
				i += 2
			}
//			println("[$s]")
			m.add(s)
		}
		var p1 = 0
		m.forEach {
//			println(it)
			val sol = mutableListOf<Pair<Long, Long>>()
			for (a in 0 until it.prize.x) {
				for (b in 0 until it.prize.y) {
					if (a * it.a.x + b * it.b.x > it.prize.x || a * it.a.y + b * it.b.y > it.prize.y) {
						//break
					}
					if (a * it.a.x + b * it.b.x == it.prize.x && a * it.a.y + b * it.b.y == it.prize.y) {
						sol.add(Pair(a.toLong(), b.toLong()))
//						println("[$a, $b]")
					}
				}
			}
			var r = sol.map { it.first * 3 + it.second }.minOrNull()
//			println("[${r}]")
			if (r != null) {
				p1 += r.toInt()
			}
		}
		println("p1: $p1")
	}
}
