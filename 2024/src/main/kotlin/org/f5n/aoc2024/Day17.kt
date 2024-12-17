package org.f5n.aoc2024

import java.lang.Math.pow

class Day17 {
	fun run(args: Array<String>) {
		val lines = args[0].readAll().split("\n\n")
		val instr = lines[1].split(" ")[1].split(",").map { it.toInt() }
		val init = lines[0].split("\n").map { it.split(" ") }

		val reg = mutableMapOf<String, Long>()
		reg["a"] = init[0][2].toLong()
		reg["b"] = init[1][2].toLong()
		reg["c"] = init[2][2].toLong()

		println(reg)
		println(instr)
		val out = emptyList<Long>().toMutableList()
		var ptr = 0
		var j2 = false

		while (ptr <= instr.size - 2 || ptr == 0) {
			val op = instr[ptr+1]
			val com = when (op) {
				0 -> 0
				1 -> 1
				2 -> 2
				3 -> 3
				4 -> reg["a"]!!.toLong()
				5 -> reg["b"]!!.toLong()
				6 -> reg["c"]!!.toLong()
				else -> -1111
			}
			println("### ptr at $ptr, ins is ${instr[ptr]}")
			when (instr[ptr]) {
				0 -> {
					var num = reg["a"]!!
					var den = pow(2.0, com.toDouble())
					var r = num / den
					reg["a"] = r.toLong()
					println("adv")
				}
				1 -> {
					val num = reg["b"]!!
					val r = num.xor(op.toLong())
					reg["b"] = r
					println("bxl rb to $r")
				}
				2 -> {
					val r = com % 8
					reg["b"] = r
					println("bst: rb ${reg["b"]} to $r")
				}
				3 -> {
					val num = reg["a"]!!
					println("jnz1 to $op / num $num / j2 $j2")
					if (num != 0L) {
						ptr = op
						j2 = true
					}
					println("jnz2 to $op / num $num / j2 $j2")
				}
				4 -> {
					val r = reg["b"]!!.xor(reg["c"]!!)
					reg["b"] = r
					println("bxc rb to $r")
				}
				5 -> {
					val r = com % 8
					out.add(r)
					println("out: $r")
				}
				6 -> {
					val num = reg["a"]!!
					val den = pow(2.0, com.toDouble())
					val r = num / den
					reg["b"] = r.toLong()
					println("bdv rb to $r")
				}
				7 -> {
					val num = reg["a"]!!
					val den = pow(2.0, com.toDouble())
					val r = num / den
					reg["c"] = r.toLong()
					println("cdv rb to $r")
				}
			}
			if (!j2)  {
				ptr += 2
			} else {
				j2 = false
			}
		}
		print("-----\nout: ")
		println(out.joinToString(","))
		reg.keys.sorted().forEach { println("${it.toUpperCase()}: ${reg[it]}") }
	}
}
