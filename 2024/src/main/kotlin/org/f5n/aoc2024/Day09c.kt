package org.f5n.aoc2024

class Day09c {
    fun run(args: Array<String>) {
        val line = args[0].readLines()[0]
        var file = true
        var id = 0
        val fs = emptyList<Pair<Long, Long>>().toMutableList()

        for (c in line) {
            if (file) fs.add(Pair(id.toLong(), c.toString().toLong()))
            else fs.add(Pair(-1, c.toString().toLong()))
            if (file) id++
            file = !file
        }
//        println(fs)
        println(fs.size)

        val hasSpace = fun(x: List<Pair<Long, Long>>): Boolean {
            return x.indexOfFirst { it.first == -1L } != -1
        }
        var i = 0
        while (hasSpace(fs)) {
            val pos = fs.indexOfFirst { it.first == -1L }
            val last = fs.indexOfLast { it.first > -1L }
            println("$pos ${fs[pos]} $last ${fs[last]} / ${fs.size}")

            var las = fs[last]
            if (last >= fs.size - 1) {
                println("at end")
                fs.removeAt(last)
                fs.add(last, Pair(las.first, las.second - 1))
                fs.add(last + 1, Pair(-1, 1))
            } else {
                var next = fs[last + 1]
                println(" $next")
                if (next.first == -1L) {
                    next = fs.removeAt(last + 1)
//                    fs.add(last, Pair(las.first, las.second - 1))
                    fs.add(last + 1, Pair(next.first, next.second + 1))
                } else {
                    fs.removeAt(last)
                    fs.add(last, Pair(las.first, las.second - 1))
                    fs.add(last + 1, Pair(-1, 1))
                }

                fs.add(last, Pair(las.first, las.second - 1))
                fs.add(last + 1, Pair(-1, 1))
            }
            val po = fs.removeAt(pos)
            fs.add(pos, Pair(las.first, 1))
            fs.add(pos + 1, Pair(po.first, po.second - 1))
            println(fs)

            if (i > 1) break
            i++
            val x2 = fs[last]
            //fs[pos] = x2
            //fs[last] = -1L
        }
        var p1 = 0L
        var idx = 0L
        for (c in fs.indices) {
            val e = fs.elementAt(c)
            if (e.first != -1L) {
                for (ee in 0 until e.second) {
                    p1 += idx * e.first
                    idx++
                }
            } else {
                idx += e.second
            }
        }
        println()
        println("p1: $p1")
        println(p1 == 1928L)
        println(p1 == 6471961544878L)
    }

    fun run2(args: Array<String>) {
        val line = args[0].readLines()[0]
        var file = true
        var id = 0
        val fs2 = emptyList<Pair<Long, Long>>().toMutableList()

        for (c in line) {
            if (file) fs2.add(Pair(id.toLong(), c.toString().toLong()))
            else fs2.add(Pair(-1, c.toString().toLong()))
            if(file) id++
            file = !file
        }
//        println(fs2)
//        println(fs2.size)

        val findBlock = fun(x: List<Pair<Long,Long>>, end: Int) : Int {
            return x.take(end).indexOfLast { it.first != -1L }
        }
        val findSpace2 = fun(x: List<Pair<Long,Long>>, size: Long): List<Pair<Long, Long>> {
            return x.filter { it.first == -1L }.filter{ it.second >= size }
        }
        val render = fun(x: List<Pair<Long,Long>>) {
            var s = ""
            for (ii in x) {
                for (j in 0 until ii.second) s += if (ii.first == -1L) "." else ii.first
            }
            println()
            println(s)
        }

//        var startIndex = 0
        var endIndex = fs2.size
        val done = emptySet<Long>().toMutableList()
        println("--------------------")
        while (endIndex > 0) {
//            println(fs2)
//            render(fs2)
            val b = findBlock(fs2, endIndex)
//            println("  ei is $endIndex /  ${fs.size} - b is ${fs2[b]} @ $b")
            if (b == -1 || done.contains(fs2[b].first)) {
                endIndex = b
                continue
            }

            val sa = findSpace2(fs2, fs2[b].second)
            if (sa.isEmpty() || fs2.indexOf(sa.first()) > fs2.indexOf(fs2[b])) {
                endIndex = b
//                println("!space for ${fs2[b]} @ $b")
                continue
            }
            val s = fs2.indexOf(sa.first())
            if (fs2[b].second == fs2[s].second) {
//                println("space= for ${fs2[b]} @ $b at ${fs2[s]} @ $s")
                val bb = fs2.removeAt(b)
                fs2.add(b, Pair(-1, bb.second))
                fs2.removeAt(s)
                fs2.add(s, Pair(bb.first, bb.second))
                done.add(bb.first)
                endIndex = b
                continue
            } else if (fs2[b].second < fs2[s].second) {
//                println("space+ for ${fs2[b]} @ $b at ${fs2[s]} @ $s")
                val bb = fs2.removeAt(b)
                fs2.add(b, Pair(-1, bb.second))
                // @TODO merge
                done.add(bb.first)

                val ss = fs2.removeAt(s)
                fs2.add(s, Pair(bb.first, bb.second))
                fs2.add(s+1, Pair(-1, ss.second-bb.second))
                endIndex = b
                continue
            } else {
                    endIndex = b
            }
        }

        var p2 = 0L
        var idx2 = 0L
        for (c in fs2.indices) {
            val e = fs2.elementAt(c)
            if (e.first != -1L) {
                for (ee in 0 until e.second) {
                    p2 += idx2 * e.first
                    idx2++
                }
            } else {
                idx2 += e.second
            }
        }
        println()
        println("p2: $p2")
        println(p2 == 6511178035564L)
    }
}
