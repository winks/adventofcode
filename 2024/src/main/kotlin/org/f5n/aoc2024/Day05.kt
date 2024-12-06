package org.f5n.aoc2024

class Day05 {
    fun run(args: Array<String>) {
        val lines = args[0].readLines()
        val rules: MutableMap<Pair<Int, Int>, Int> = mutableMapOf()
        var s2 = false
        var result1 = 0
        var result2 = 0
        val iv = fun(ord: List<Int>, rules: MutableMap<Pair<Int, Int>, Int>): Pair<Int, Int>? {
            for (i in ord.indices) {
                for (j in i + 1 until ord.size) {
                    if (rules.containsKey(Pair(ord[i], ord[j]))) {
                        return Pair(i, j)
                    }
                }
            }
            return null
        }
        lines.forEach {
            if (it.isEmpty()) {
                s2 = true
            }
            if (!s2) {
                val (k, v) = it.split("|")
                rules[Pair(v.toInt(), k.toInt())] = 0
            } else {
                if (it.isEmpty()) return@forEach
                val ord = it.split(",").map { it.toInt() }.toTypedArray()
                var check: Pair<Int, Int>? = iv(ord.toList(), rules)
                if (check == null) {
                    result1 += ord[(ord.size - 1) / 2]
                } else {
                    //println("\n# ${ord.toList()} $check")
                    var i = 1
                    while (check != null) {
                        val a = check.first
                        val b = check.second
                        val tmp = ord[b]
                        ord[b] = ord[a]
                        ord[a] = tmp
                        check = iv(ord.toList(), rules)
                    }
                    result2 += ord[(ord.size - 1) / 2]
                }
            }
        }
        println(result1)
        println(result2)
    }
}