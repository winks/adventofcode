package org.f5n.aoc2024

class Day19 {
	fun run(args: Array<String>) {
		val lines = args[0].readAll().split("\n\n")
		val towels = lines[0].split(", ")
		val todo = lines[1].split("\n")
//		println(towels)
//		println(todo)
		val re = Regex("^(" + towels.joinToString("|") + ")+$")
//		println(re)
		val p1 = todo.filter { re.containsMatchIn(it) }.size
		println(p1)
	}
}
