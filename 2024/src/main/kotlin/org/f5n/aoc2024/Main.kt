package org.f5n.aoc2024

import kotlin.time.measureTime
import kotlin.system.exitProcess

fun main(args: Array<String>) {
    if (args.isEmpty()) {
        println("Usage: dayXX [FILENAME]")
        exitProcess(0)
    }
    val day = if (args[0].length < 5) "day0${args[0].replace("day", "")}" else args[0]
    val inputFile = if (args.size < 2) "input/${day}/input.txt" else args[1]

    measureTime {
        if (day == "day01") {
            val d = Day01()
            d.run(arrayOf(inputFile))
            d.run2(arrayOf(inputFile))
        } else if (day == "day02") {
            val d = Day02()
            d.run(arrayOf(inputFile))
            d.run(arrayOf(inputFile), true)
        } else if (day == "day03") {
            val d = Day03()
            d.run(arrayOf(inputFile))
        } else if (day == "day04") {
            val d = Day04()
            d.run(arrayOf(inputFile))
        } else if (day == "day05") {
            val d = Day05()
            d.run(arrayOf(inputFile))
        } else if (day == "day06") {
            val d = Day06()
            d.run(arrayOf(inputFile))
        } else if (day == "day07") {
            val d = Day07()
            d.run(arrayOf(inputFile))
        } else if (day == "day07b") {
            val d = Day07b()
            d.run(arrayOf(inputFile))
        } else if (day == "day08") {
            val d = Day08()
            d.run(arrayOf(inputFile))
        } else if (day == "day09") {
            val d = Day09()
            d.run(arrayOf(inputFile))
            // p2 needs 11 min
            //d.run2(arrayOf(inputFile))
            val d2 = Day09c()
            // p1 is not implemented
            d2.run2(arrayOf(inputFile))
        } else if (day == "day09c") {
            val d = Day09c()
            d.run(arrayOf(inputFile))
//            d.run2(arrayOf(inputFile))
        } else if (day == "day10") {
            val d = Day10()
            d.run(arrayOf(inputFile))
            d.run2(arrayOf(inputFile))
        } else if (day == "day11") {
            val d = Day11()
            d.run(arrayOf(inputFile), 25)
            d.run(arrayOf(inputFile), 75)
        } else if (day == "day12") {
            val d = Day12()
            d.run1(arrayOf(inputFile))
        } else if (day == "day13") {
            val d = Day13()
            d.run(arrayOf(inputFile))
        } else if (day == "day13abmini") {
            val d = Day13abmini()
            d.run(arrayOf(inputFile))
        } else if (day == "day14") {
            val d = Day14()
            d.run(arrayOf(inputFile))
        } else if (day == "day15") {
            val d = Day15()
            d.run(arrayOf(inputFile))
            d.run2(arrayOf(inputFile))
        } else if (day == "day16") {
            val d = Day16()
            d.run(arrayOf(inputFile))
        } else if (day == "day17") {
            val d = Day17()
            d.run(arrayOf(inputFile))
        } else if (day == "day18") {
            val d = Day18()
            d.run(arrayOf(inputFile))
        } else if (day == "day19") {
            val d = Day19()
            d.run(arrayOf(inputFile))
        } else if (day == "day20") {
            val d = Day20()
            d.run(arrayOf(inputFile))
        } else if (day == "day21") {
            val d = Day21()
            d.run(arrayOf(inputFile))
        } else if (day == "day22") {
            val d = Day22()
            d.run(arrayOf(inputFile))
        }
    }.let { println(it) }
}
