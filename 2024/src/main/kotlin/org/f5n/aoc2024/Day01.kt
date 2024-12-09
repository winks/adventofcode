package org.f5n.aoc2024

import kotlin.math.abs

class Day01 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		var left = emptyList<Int>().toTypedArray()
		var right = emptyList<Int>().toTypedArray()
		lines.forEach {
			val parts = it.split(" ")
			left = left.plus(parts[0].toInt())
			right = right.plus(parts[parts.size-1].toInt())
		}
		val max1 = left.max()+1
		val max2 = right.max()+1
		var result = emptyList<Int>()
		var pos1 = 0
		while (left.filterNot { it == max1 }.isNotEmpty()) {
			if (left[pos1] == left.min()) {
				var pos2 = 0
				while (right[pos2] != right.min()) {
					pos2++
				}
				var x = abs(left[pos1]-right[pos2])
				result = result.plus(x)
				left[pos1] = max1
				right[pos2] = max2
				pos1 = 0
			} else {
				pos1++
			}
		}
		println(result.sum())
	}

	fun run2(args: Array<String>) {
		val lines = args[0].readLines()
		var left = emptyList<Int>().toTypedArray()
		var right = emptyList<Int>().toTypedArray()
		lines.forEach {
			val parts = it.split(" ")
			left = left.plus(parts[0].toInt())
			right = right.plus(parts[parts.size-1].toInt())
			//println(parts.size)
		}
		var result = emptyList<Int>()
		left.forEach {
			val cur = it
			val x = right.filter { it == cur }.size
			result = result.plus(x*cur)
		}
		println(result.sum())
	}
}
