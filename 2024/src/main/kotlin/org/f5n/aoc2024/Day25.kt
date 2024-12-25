package org.f5n.aoc2024

class Day25 {
	fun run(args: Array<String>) {
		val inputs = args[0].readAll().split("\n\n")
		val locks = emptyList<MutableList<Int>>().toMutableList()
		val keys = emptyList<MutableList<Int>>().toMutableList()
		inputs.forEach {
			val lines = it.trim().split("\n")
			val lockKey = mutableListOf(0, 0, 0, 0, 0)
			for (line in 1 until lines.size-1) {
				for (i in lockKey.indices) {
					if (lines[line][i] == '#') lockKey[i]++
				}
			}
			if (it.startsWith("#####")) {
				locks.add(lockKey)
			} else if (it.endsWith("#####")) {
				keys.add(lockKey)
			}
		}
		var p1 = 0
		for (k in keys) {
			for (l in locks) {
				if (k.zip(l).map{ it.toList().sum()}.all { it <= 5 }) p1++
			}
		}
		println("p1: $p1")
	}
}
