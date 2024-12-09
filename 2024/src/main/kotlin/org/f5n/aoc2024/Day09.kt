package org.f5n.aoc2024

class Day09 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines()[0]
		println(lines)
		var file = true
		var id = 0
		var fs2 = ""

		for (c in lines) {
			if (file) {
				fs2 += "$id".repeat("$c".toInt())
				id++
			} else {
				fs2 += ".".repeat("$c".toInt())
			}
			file = !file
		}
		println(fs2)
		val re = Regex("\\.+\\d+")
		while (re.find(fs2) != null) {
			val pos = fs2.indexOfFirst{ it == '.'}
			val last = fs2.indexOfLast { it != '.' }
			val fs = fs2.substring(0, pos) + fs2.elementAt(last) + fs2.substring(pos+1, last) + '.' + fs2.substring(last+1)
			fs2 = fs
		}
		println(fs2.length)
		println(fs2)
		var p1 = 0L
		for (c in fs2.indices) {
			if (fs2.elementAt(c) == '.') {
				continue
			}
			val r : Long = c * fs2.elementAt(c).toString().toLong()
			p1 += r
		}
	println()
		println(p1)
		// 92349417108
	}
}
