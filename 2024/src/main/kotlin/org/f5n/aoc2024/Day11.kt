package org.f5n.aoc2024

class Day11b {
	fun run(args: Array<String>, num: Long) {
		val line2 = args[0].readLines().get(0).split(' ').map(String::toLong)
		var line = emptyMap<Long, Long>().toMutableMap()
		line2.forEach { line[it] = 1 }
//		println(line2)
		for (i in 0 until num) {
			val ln = emptyMap<Long, Long>().toMutableMap()
			for (k in line.keys) {
				if (k == 0L) {
					val n = 1L
					if (!ln.containsKey(n)) ln[n] = 0
					ln[n] = ln[n]!! + line[k]!!
				} else if (k.toString().length % 2 == 0 ) {
					val (a, b) = k.toString().chunked(k.toString().length / 2).map(String::toLong)
					if (!ln.containsKey(a)) ln[a] = 0
					ln[a] = ln[a]!! + line[k]!!
					if (!ln.containsKey(b)) ln[b] = 0
					ln[b] = ln[b]!! + line[k]!!
				} else {
					val n = 2024 * k
					if (!ln.containsKey(n)) ln[n] = 0
					ln[n] = ln[n]!! + line[k]!!
				}
			}
			line = ln.toMutableMap()
		}
		println("result $num: ${line.map{ it.value }.sum()}")
	}
}
