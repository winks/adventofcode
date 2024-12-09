package org.f5n.aoc2024

class Day09 {
    fun run(args: Array<String>) {
        val lines = args[0].readLines()[0]
        println(lines)
        var file = true
        var id = 0
        val fs = emptyList<Long>().toMutableList()

        for (c in lines) {
            if (file) {
                for (i in 0 until "$c".toInt()) {
                    fs += id.toLong()
                }
                id++
            } else {
                for (i in 0 until "$c".toInt()) {
                    fs += -1
                }
            }
            file = !file
        }
        println(fs)
        val hasSpace = fun(x: List<Long>): Boolean {
            val sp = x.indexOfFirst { it == -1L }
            for (i in sp until x.size) {
                if (i > sp && x[i] > -1L) {
                    return true
                }
            }
            return false
        }
        while (hasSpace(fs)) {
            val pos = fs.indexOfFirst { it == -1L }
            val last = fs.indexOfLast { it > -1L }
            val x2 = fs[last]
            fs[pos] = x2
            fs[last] = -1L
        }
        println(fs)
        var p1 = 0L
        for (c in fs.indices) {
            if (fs.elementAt(c) == -1L) {
                continue
            }
            val r: Long = c * fs.elementAt(c)
            p1 += r
        }
        println()
        println(p1)
    }
}
