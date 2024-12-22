package org.f5n.aoc2024

class Day22 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines().map(String::toLong)
		var p1 = 0L
		lines.forEach {
			var x = it
			for (i in 0..<2000) {
				x = fwd(x)
			}
			p1 += x
		}
		println("p1: $p1")
	}
	private fun fwd(i: Long) : Long {
		var x = mp(i, i * 64)
		x = mp(x, (x / 32))
		return mp(x, x * 2048)
	}
	private fun mp(i: Long, j: Long) : Long {
		return i.xor(j) % 16777216L
	}
}
