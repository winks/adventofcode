package org.f5n.aoc2024

class Day09 {
    fun run(args: Array<String>) {
        val line = args[0].readLines()[0]
        println(line)
        var file = true
        var id = 0
        val fs = emptyList<Long>().toMutableList()

        for (c in line) {
            for (i in 0 until "$c".toInt()) {
                fs += if (file) {
                    id.toLong()
                } else {
                    -1
                }
            }
            if(file) id++
            file = !file
        }
        println(fs)
        val fs2 = fs.toMutableList()

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

        val findBlock = fun(x: List<Long>, endx: Int) : Pair<Int,Int> {
            val end = x.take(endx).indexOfLast { it != -1L }
            var start = 0
            for (i in end-1 downTo 0) {
                if (x[i] != x[end]) {
                    start = i+1
                    break
                }
            }
            //println("\nblock of ${x[end]} from $start to $end = ${end-start+1}")
            return Pair(start, end)
        }
        val findSpace = fun(x: List<Long>, startx: Int) : Pair<Int, Int> {
            if (startx >= x.size) {
                return Pair(0, 0)
            }
            val start = x.takeLast(x.size-startx).indexOfFirst { it == -1L } + startx
            var end = x.size
            for (i in start+1 until x.size) {
                if (x[i] != -1L) {
                    end = i-1
                    break
                }
            }
            //println("space from $start to $end = ${end-start+1} skipped $startx")
            return Pair(start, end)
        }
        var i = fs2.size
        var ss = 0
        var ee = fs.size
        var lastBlock : Long = 0
        while (i > 0) {
            val b = findBlock(fs2, ee)
            if (fs[b.first] == 0L) {
                break
            }
            if (fs[b.first] != lastBlock) {
                ss = 0
                lastBlock = fs[b.first]
            }
            val s = findSpace(fs2, ss)
            if (s.second-s.first+1 < b.second-b.first+1) {
                ss = s.second+1
                //println("no space $ss ${fs.size}")
                if (ss >= fs.size) {
                    ss = 0
                    ee = b.first
                    lastBlock = fs[b.first]
                }
                continue
            } else if (s.first >= b.second) {
                ee = b.first
                ss = 0
                continue
            }
            if (b.second - b.first + 1 <= s.second - s.first + 1) {
                //println("found space")
                for (sx in s.first..(s.first+b.second-b.first)) {
                    fs2[sx] = fs2[b.first]
                }
                for (bx in b.first..b.second) {
                    fs2[bx] = -1
                }
                i = b.first
                ss = 0
                ee = b.first
            }
            //println(fs2)
        }
        var p1 = 0L
        var p2 = 0L
        for (c in fs.indices) {
            if (fs.elementAt(c) != -1L) {
                p1 += c * fs.elementAt(c)
            }
            if (fs2.elementAt(c) != -1L) {
                p2 += c * fs2.elementAt(c)
            }
        }
        println(fs)
        println(fs2)
        println()
        println("p1: $p1")
        println("p2: $p2")

    }
}
