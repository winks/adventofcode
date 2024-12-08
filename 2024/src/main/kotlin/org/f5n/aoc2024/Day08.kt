package org.f5n.aoc2024


class Day08 {
    fun run(args: Array<String>) {
        val lines = args[0].readLines()
        var board = Board(lines)
        board.print()
        val result = emptySet<Pos>().toMutableSet()
        val result2 = emptySet<Pos>().toMutableSet()
        for (antenna in getAlnum()) {
            val m = board.getMatches(antenna)
            println("Matches for $antenna: $m")
            perms(2, m.toList()).map { w ->
                println(w)
                println(board.getLine(w[0], w[1]))
                val line = board.getLineAll(w[0], w[1])
                println("line: $line")
                line.forEach {
                    val c = it
                    val d1 = board.getDistance(c, w[0])
                    val d2 = board.getDistance(c, w[1])
                    if (line.contains(c) && (2 * d1 == d2 || 2 * d2 == d1)) {
                        println("anti: $c")
                        result.add(c)
                    }
                }
            }

        }
        println("p1: ${result.size}")
    }
}
