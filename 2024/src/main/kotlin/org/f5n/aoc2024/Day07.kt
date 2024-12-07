package org.f5n.aoc2024

import java.math.BigDecimal

class Day07 {
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		
		val add = fun(a: BigDecimal, b: BigDecimal) : BigDecimal { return a + b }
		val mul = fun(a: BigDecimal, b: BigDecimal) : BigDecimal { return a * b }
		val cat = fun(a: BigDecimal, b: BigDecimal) : BigDecimal { return BigDecimal("${a}${b}") }
		val po  = fun(f: (BigDecimal, BigDecimal) -> BigDecimal) : String { if (f == cat) return "||" else if (f == mul) return "* " else return "+ " }

		var result1 = BigDecimal(0)
		val ops = listOf(add, mul)
		lines.forEach {
			val parts = it.split(": ")
			val result = BigDecimal(parts[0])
			val operands = "${parts[1]}".split(" ").map { BigDecimal(it) }
			val myOps = nonexhaustivePermutations(operands.size-1, ops)
			var done = false
			for (opList in myOps) {
				if (done) break
				var r = BigDecimal(0)
				for (o in opList.indices) {
					if (o == 0) r = opList[o](operands[0], operands[1])
					else r = opList[o](r, operands[o+1])

					if (r == result) done = true
				}
			}
			if (done) result1 += result
		}
		println(result1)

		var result2 = BigDecimal(0)
		val ops2 = listOf(add, mul, cat)
		lines.forEach {
			val parts = it.split(": ")
			val result = BigDecimal(parts[0])
			val operands = "${parts[1]}".split(" ").map { BigDecimal(it) }
			val myOps = nonexhaustivePermutations(operands.size-1, ops2)
			var done = false
			for (opList in myOps) {
				if (done) break
				var r = BigDecimal(0)
				for (o in opList.indices) {
					if (o == 0) {
						r = opList[o](operands[0], operands[1])
						// println("[$result] $r = ${operands[0]} ${po(opList[o])} ${operands[1]}")
					} else {
						val rold = r
						r = opList[o](r, operands[o+1])
						// println("[$result] $r = ${rold} ${po(opList[o])} ${operands[o+1]}")
					}
					if (r == result && o >= opList.size-1) {
						done = true
						// println(operands)
						break
					}
				}
			}
			if (done) result2 += result
		}
		println(result2)
	}
}