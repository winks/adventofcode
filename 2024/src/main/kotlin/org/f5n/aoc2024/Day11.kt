package org.f5n.aoc2024


class Day11 {
	fun loop(line2: MutableList<Long>) : MutableList<Long> {
		var k = 0
		var line : MutableList<Long> = line2.toMutableList()
		while (k < line.size) {
			if (line[k] == 0L) {
				line[k] = 1
				k++
			} else if (line[k].toString().length % 2 == 0 ) {
				val (a, b) = line[k].toString().chunked(line[k].toString().length / 2)
				line[k] = a.toLong()
				line.add(k+1, b.toLong())
				k += 2
			} else {
				line[k] = 2024 * line[k]
				k++
			}
		}
		return line
	}
	fun run(args: Array<String>) {
		val line = args[0].readLines().get(0).split(' ').map(String::toLong)
		var line2 = line.toMutableList()
		for (i in 0 until 25) {
			line2 = loop(line2)
		}
		println("p1: ${line2.size}")
	}
}
