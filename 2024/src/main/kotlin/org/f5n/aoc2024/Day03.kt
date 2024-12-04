package org.f5n.aoc2024

class Day03 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		var result1 = 0
		var result2 = 0
		val re = Regex("(mul|do|don't)\\(((\\d+),\\s?(\\d+))?\\)")
		var enabled = true
		lines.forEach {
			val m = re.findAll(it)
			m.forEach {
				if (it.groupValues[1] == "do") {
					enabled = true
				} else if (it.groupValues[1] == "don't") {
					enabled = false
				} else if (it.groupValues[1] == "mul") {
					val cur = it.groupValues[3].toInt() * it.groupValues[4].toInt()
					result1 += cur
					if (enabled) result2 += cur
				}
			}
		}
		println(result1)
		println(result2)
	}
}
