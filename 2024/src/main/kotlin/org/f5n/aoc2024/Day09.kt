package org.f5n.aoc2024

class Day09 {
    private fun li(args: Array<String>): MutableList<Long> {
        val line = args[0].readLines()[0]
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
        return fs
    }

    fun run(args: Array<String>) {
        val fs = li(args)

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
        var p1 = 0L
        for (c in fs.indices) {
            if (fs.elementAt(c) != -1L) {
                p1 += c * fs.elementAt(c)
            }
        }
        println()
        println("p1: $p1")
   }

   fun run2(args: Array<String>) {
         val fs2 = li(args)

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
        var doneIndex = fs2.size
        var searchIndex = 0
        var endIndex = fs2.size
        val lastNums = emptySet<Long>().toMutableList()
        while (doneIndex > 0) {
            val b = findBlock(fs2, endIndex)
            if (fs2[b.first] == 0L) {
                break
            }
            if (lastNums.contains(fs2[b.first])) {
                endIndex = b.first
                continue
            }
            if (fs2[b.first] >= endIndex) {
                searchIndex = 0
            }
            val s = findSpace(fs2, searchIndex)
            if (s.second-s.first+1 < b.second-b.first+1) {
                searchIndex = s.second+1
//                println("no space at $searchIndex / ${fs.size}")
                if (searchIndex >= fs2.size) {
                    searchIndex = 0
                    endIndex = b.first
                }
                continue
            } else if (s.first >= b.first) {
                endIndex = b.first
                searchIndex = 0
                continue
            } else if (s.second - s.first + 1 >= b.second - b.first + 1) {
//                println("found space at ${s.first}")
                lastNums.add(fs2[b.first])
                for (sx in s.first..(s.first+b.second-b.first)) {
                    fs2[sx] = fs2[b.first]
                }
                for (bx in b.first..b.second) {
                    fs2[bx] = -1
                }
                doneIndex = b.first
                searchIndex = 0
                endIndex = b.first
            }
//            println(fs2)
        }

        var p2 = 0L
        for (c in fs2.indices) {
            if (fs2.elementAt(c) != -1L) {
                p2 += c * fs2.elementAt(c)
            }
        }
//        println(line)
//        println(fs)
//        println(fs2)
        println()
        println("p2: $p2")

    }
}
