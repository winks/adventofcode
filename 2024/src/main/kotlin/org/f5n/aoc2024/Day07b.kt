package org.f5n.aoc2024

import java.math.BigDecimal

class Day07b {
	fun run(args: Array<String>) {
		println("p1: " + args[0].readLines()
			.map { it.split(": ") }
			.map { (left: String, right: String) -> Pair(BigDecimal(left), right.split(" ").map { BigDecimal(it) })}
			.map { a -> Pair(
					a.first,
					nonexhaustivePermutations(a.second.size-1, listOf(
						fun(a: BigDecimal, b: BigDecimal) : BigDecimal { return a + b }, 
						fun(a: BigDecimal, b: BigDecimal) : BigDecimal { return a * b }))
						.map { op -> a.second.takeLast(a.second.size-1).foldIndexed(a.second.get(0)) {idx, acc, elem -> op[idx](acc, elem) } }
						.filter { it == a.first }
				) }
			.filter{ it.second.size > 0 && it.first == it.second.get(0) }
			.map { it.first }
			.reduce { a, n -> a + n })
	}
}