package org.f5n.aoc2024


class Day05 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		val rules: MutableMap<Int, List<Int>> = mutableMapOf()
		val rules2: MutableMap<Int, List<Int>> = mutableMapOf()
		var s2 = false
		var result1 = 0
		var result2 = 0
		lines.forEach {
			if (it.isEmpty()) {
				s2 = true
			}
			if (!s2) {
				val (k, v) = it.split("|")
				if (!rules.containsKey(k.toInt())) rules[k.toInt()] = listOf(v.toInt())
				else rules[k.toInt()] = rules[k.toInt()]!!.plus(v.toInt())
				if (!rules2.containsKey(v.toInt())) rules2[v.toInt()] = listOf(k.toInt())
				else rules2[v.toInt()] = rules2[v.toInt()]!!.plus(k.toInt())
			} else {
				if (it.isEmpty()) return@forEach
				val ord = it.split(",").map { it.toInt() }
				var valid = true
				for (i in ord.indices) {
					if (rules2.containsKey(ord[i])) {
						for (j in ord.indices) {
							if (j <= i ) continue
							if (rules2[ord[i]]?.contains(ord[j]) == true) {
								valid = false
							}
						}
					}
				}

				if (valid) {
					result1 += ord[(ord.size-1)/2]
					println(it)
				}
			}
		}
		println(result1)
	}
}
