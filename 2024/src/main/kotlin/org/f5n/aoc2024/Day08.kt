package org.f5n.aoc2024


class Day08 {
    fun run(args: Array<String>) {
        val board = Board(args[0].readLines())
        val result = emptySet<Pos>().toMutableSet()
        val result2 = emptySet<Pos>().toMutableSet()
        for (antenna in getAlnum()) {
            perms(2, board.getMatches(antenna).toList()).map { w ->
                board.getLineAll(w[0], w[1]).forEach {
                    val d1 = board.getDistance(it, w[0])
                    val d2 = board.getDistance(it, w[1])
                    result2.add(it)
                    if (2 * d1 == d2 || 2 * d2 == d1) {
                        result.add(it)
                    }
                }
            }
        }
        println("p1: ${result.size}\np2: ${result2.size}")
    }
}
