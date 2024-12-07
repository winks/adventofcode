package org.f5n.aoc2024

import java.io.File
import java.io.InputStream

fun String.readLines(): Array<String> =
    File(this).inputStream().bufferedReader().readLines().toTypedArray()

fun String.readLinesToInt(): Array<Int> {
    val stream: InputStream = File(this).inputStream()
    val lines = mutableListOf<Int>()
    stream.bufferedReader().readLines().forEach {
        lines.add(Integer.parseInt(it))
    }
    println("readLinesToInt: ${lines.size}")
    return lines.toTypedArray()
}

class Pos(val x: Int, val y: Int) {
    override fun toString(): String {
        return "($x, $y)"
    }
    override fun equals(other: Any?): Boolean {
        if (other is Pos) {
            return x == other.x && y == other.y
        }
        return false
    }

    override fun hashCode(): Int {
        return x * 1000 + y
    }
}

class Board(input: Array<String>) {
    val width = input[0].length
    val length = input.size
    var board = Array(length) { Array(width) { ' ' } }
    enum class direction { N, E, S, W }
    enum class directionAll { N, E, S, W, NE, SE, SW, NW }

    init {
        for (y in 0 until length) {
            for (x in 0 until width) {
                board[y][x] = input[y][x]
            }
        }
    }

    fun print(wide: Boolean = true) {
        for (y in 0 until length) {
            for (x in 0 until width) {
                print(board[y][x])
                if (wide) print(" ")
            }
            println()
        }
    }

    fun valid(p: Pos): Boolean {
        return p.x in 0..<width && p.y in 0 ..<length
    }
    fun peek(p: Pos): Char {
        return board[p.y][p.x]
    }

    fun getNeighbors(p: Pos): List<Pos> {
        val rv = mutableListOf<Pos>()
        if (p.x > 0) {
            rv.add(Pos(p.x - 1, p.y))
        }
        if (p.x < width - 1) {
            rv.add(Pos(p.x + 1, p.y))
        }
        if (p.y > 0) {
            rv.add(Pos(p.x, p.y - 1))
        }
        if (p.y < length - 1) {
            rv.add(Pos(p.x, p.y + 1))
        }
        return rv
    }

    fun getNeighbor(p: Pos, dir: direction) : Pos {
        return when (dir) {
            direction.N -> Pos(p.x, p.y - 1)
            direction.E -> Pos(p.x + 1, p.y)
            direction.S -> Pos(p.x, p.y + 1)
            direction.W -> Pos(p.x - 1, p.y)
        }
    }

    fun getNeighborsAll(p: Pos): List<Pos> {
        val rv = getNeighbors(p).toMutableList()
        if (p.x > 0) {
            if (p.y > 0) {
                rv.add(Pos(p.x - 1, p.y - 1))
            }
            if (p.y < length - 1) {
                rv.add(Pos(p.x - 1, p.y + 1))
            }
        }
        if (p.x < width - 1) {
            if (p.y > 0) {
                rv.add(Pos(p.x + 1, p.y - 1))
            }
            if (p.y < length - 1) {
                rv.add(Pos(p.x + 1, p.y + 1))
            }
        }
        return rv
    }

    fun getDirection(p1: Pos, p2: Pos): directionAll {
        if (p1.x == p2.x) {
            if (p1.y > p2.y) {
                return directionAll.N
            } else {
                return directionAll.S
            }
        }
        if (p1.y == p2.y) {
            if (p1.x > p2.x) {
                return directionAll.W
            } else {
                return directionAll.E
            }
        }
        if (p1.x > p2.x) {
            if (p1.y > p2.y) {
                return directionAll.NW
            } else {
                return directionAll.SW
            }
        } else {
            if (p1.y > p2.y) {
                return directionAll.NE
            } else {
                return directionAll.SE
            }
        }
    }

    fun getOpposite(p: Pos, dir: directionAll): Pos {
        return when (dir) {
            directionAll.N -> Pos(p.x, p.y + 1)
            directionAll.E -> Pos(p.x - 1, p.y)
            directionAll.S -> Pos(p.x, p.y - 1)
            directionAll.W -> Pos(p.x + 1, p.y)
            directionAll.NE -> Pos(p.x - 1, p.y + 1)
            directionAll.SE -> Pos(p.x - 1, p.y - 1)
            directionAll.SW -> Pos(p.x + 1, p.y - 1)
            directionAll.NW -> Pos(p.x + 1, p.y + 1)
        }
    }
}

fun <T> nonexhaustivePermutations(length: Int, components: List<T>): List<List<T>> =
    if (components.isEmpty() || length <= 0) listOf(emptyList())
    else nonexhaustivePermutations(length - 1, components)
        .flatMap { sub -> components.map { sub + it } }