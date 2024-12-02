package org.f5n.aoc2024

import kotlin.math.abs

class Day02 {
	fun run(args: Array<String>, threshold: Int = 0) {
		val lines = args[0].readLines().map { it.split(" ").map(String::toInt) }
		var result = 0
		lines.forEach {
			var last = it[0]
			var invalid = 0
			val asc = it[1] > last
			for (i in 1 until it.size) {
				if (invalid > 0) break
				if ((asc && it[i] <= last) || (!asc && it[i] >= last)) invalid++
				else if (abs(it[i] - last) > 3) invalid++
				else last = it[i]
			}
			if (invalid <= threshold) result++
		}
		println(result)
	}
	fun run2(args: Array<String>) {
		val lines = args[0].readLines().map { it.split(" ").map(String::toInt) }
		var result = 0
		lines.forEach {
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
			if (isAsc(it) && !isTooWide(it)) result++
			else if (isDesc(it) && !isTooWide(it)) result++
			else {
				val perms : MutableList<List<Int>> = mutableListOf()
				for (i in it.indices) {
					val c = it.toMutableList().filterIndexed { index, _ -> index != i }.toList()
					perms.add(c)
				}
				var found = 0
				perms.forEach {
					if (isAsc(it) && !isTooWide(it)) found++
					else if (isDesc(it) && !isTooWide(it)) found++
				}
				if (found > 0) result++
			}
		}
		println(result)
	}
}
