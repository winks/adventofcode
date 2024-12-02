package org.f5n.aoc2024

import kotlin.math.abs

class Day02 {
	val isAsc = fun(li: List<Int>) : Boolean {
		for (i in 1 until li.size) {
			if (li[i] <= li[i-1]) return false
		}
		return true
	}
	val isDesc = fun(li: List<Int>) : Boolean {
		for (i in 1 until li.size) {
			if (li[i] >= li[i-1]) return false
		}
		return true
	}
	val isTooWide = fun(li: List<Int>) : Boolean {
		for (i in 1 until li.size) {
			if (abs(li[i] - li[i-1]) > 3) return true
		}
		return false
	}
	fun run(args: Array<String>, useDampener : Boolean = false) {
		val lines = args[0].readLines().map { it.split(" ").map(String::toInt) }
		var result = 0
		val (ok, nope) = lines.partition { !isTooWide(it) && (isAsc(it) || isDesc(it)) }
		result += ok.size
		if (useDampener) {
			nope.forEach {
				val perms : MutableList<List<Int>> = mutableListOf()
				for (i in it.indices) {
					val c = it.toMutableList().filterIndexed { index, _ -> index != i }.toList()
					perms.add(c)
				}
				perms.filterNot(isTooWide).any { isAsc(it) || isDesc(it) }.also { if (it) result++ }
			}
		}
		println(result)
	}
}
