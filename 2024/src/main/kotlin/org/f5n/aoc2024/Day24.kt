package org.f5n.aoc2024

class Day24 {
	fun run(args: Array<String>) {
		val lines = args[0].readAll().split("\n\n")
		val wires = emptyMap<String, Int>().toMutableMap()
		val rules = emptyMap<List<String>, MutableList<String>>().toMutableMap()
		lines[0].split("\n").forEach {
			val (wire, value) = it.split(": ")
			wires[wire] = if (value == "1") 1 else 0
		}
		val re = Regex("^(\\w+) (AND|OR|XOR) (\\w+) -> (\\w+)$")
		lines[1].split("\n").forEach {
			val m = re.find(it)
			val le1 = m!!.groupValues[1]
			val op = m.groupValues[2]
			val le2 = m.groupValues[3]
			val right = m.groupValues[4]
			if (wires.containsKey(le1) && wires.containsKey(le2)) {
				wires[right] = calc(listOf(le1, op, le2), wires)
//				println("calc1: $le1  $op  $le2 -> $right :: ${wires[right]}")
			} else {
				val k = listOf(le1, op, le2)
				if (!rules.containsKey(k)) rules[k] = mutableListOf()
				rules[k]!!.add(right)
//				println("rule: $le1  $op  $le2 -> $right")
			}
		}
		val keys = rules.keys.toMutableList()
		while(keys.isNotEmpty()) {
			for (r in keys) {
				if (wires.containsKey(r[0]) && wires.containsKey(r[2])) {
					val nk = rules[r]!!
					for (k in nk) {
						wires[k] = calc(r, wires)
//						println("calc2: $r -> $nk :: ${wires[k]}")
					}
					keys.remove(r)
					break
				}
			}
		}
		var r = ""
		for (w in wires.keys.filter { it.startsWith("z") }.sorted().reversed()) {
			r += "${wires[w]}"
		}
//		println(r)
		var p1 = 0L
		for (i in r.length-1 downTo 0) {
			p1 += r[i].toString().toLong() * Math.pow(2.0, r.length-1-i.toDouble()).toLong()
		}
		println("p1: $p1")
	}
	private fun calc(x: List<String>, wires: Map<String, Int>) : Int {
		val r = when (x[1]) {
			"AND" -> if (wires[x[0]] == 1 && wires[x[2]] == 1) 1 else 0
			"OR" -> if (wires[x[0]] == 1 || wires[x[2]] == 1) 1 else 0
			"XOR" -> if (wires[x[0]] != wires[x[2]]) 1 else 0
			else -> 0
		}
		return r
	}
}
