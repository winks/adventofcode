package org.f5n.aoc2024

class Day00 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines().map(String::toInt)
		lines.forEach {
			println("[$it]")
		}
	}
}
