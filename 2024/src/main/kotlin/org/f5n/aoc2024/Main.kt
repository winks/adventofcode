package org.f5n.aoc2024

import kotlin.system.exitProcess

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        println("Usage: dayXX [FILENAME]")
        exitProcess(0)
    }

    if (args[0] == "day01") {
        val d = Day01()
        d.run(arrayOf(args[1]))
        d.run2(arrayOf(args[1]))
    } else if (args[0] == "day02") {
        val d = Day02()
        d.run(arrayOf(args[1]))
        d.run(arrayOf(args[1]), true)
    } else if (args[0] == "day03") {
    }
}
