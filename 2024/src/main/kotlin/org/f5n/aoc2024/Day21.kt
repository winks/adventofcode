package org.f5n.aoc2024

class Day21 {
    val vals = mapOf(
        "UP" to "^",
        "LEFT" to "<",
        "DOWN" to "v",
        "RIGHT" to ">",
        "ENTER" to "A",
    )
    var dpad: Board = Board.fromDim(2, 2)

    enum class Direction {
        UP, DOWN, LEFT, RIGHT, ENTER
    }

    fun run(args: Array<String>) {
        val inputKeypad = listOf("789", "456", "123", " 0A").toTypedArray()
        val inputDpad = listOf(" ^A", "<v>").toTypedArray()
        val keypad = Board(inputKeypad)
        this.dpad = Board(inputDpad)
        keypad.print()
        dpad.print()
        val lines = args[0].readLines()
            .map { it.toCharArray() }
        lines.forEach { println(it.joinToString(" ")) }
        var p1 = 0
        var start = keypad.getMatches(vals[Direction.ENTER.toString()].toString()).first()
        val vEnter = vals["ENTER"]!!
        lines.forEach { line ->
            println("line: ${line.joinToString()}")
            val x2accAll = emptyMap<List<Direction>, List<List<Direction>>>().toMutableMap()
            val x2accAll2 = emptySet<List<Direction>>().toMutableSet()
            val x3accAll2 = emptySet<List<Direction>>().toMutableSet()
            val mut = emptyList<List<List<Direction>>>().toMutableList()
            line.forEach { step ->
                val end = keypad.getMatches(step.toString()).first()
                val (cf, co) = aStar(keypad, start, end)
                val x = co[end]!! + 1
                val p = getPath(cf, start, end)
                val ksp = senksp(keypad, p, x)
                val ksp1 = emptyList<List<Direction>>().toMutableList()
                for (xp in ksp.indices) {
                    val xpx = ksp[xp].windowed(2)
                        .map { this.translate(it[0], it[1], keypad) }
                        .plus(Direction.ENTER)
                    ksp1.add(xpx)
                }
                mut.add(ksp1)
                start = end
            }
            val x1accAll = perm(mut).map { it.flatten() }
            for (x in x1accAll) {
                println("${x.size} ${pp(x)}")
            }
            println("steps: ${x1accAll.size} * [${x1accAll[0].size}]")
            var s2 = dpad.getMatches(vEnter).first()
            x1accAll.forEach { x1acc ->
                val mut2 = emptyList<List<List<Direction>>>().toMutableList()
                x1acc.forEach { l2 ->
                    val e2 = dpad.getMatches(vals[l2.toString()]!!).first()
                    val (cf2, co2) = aStar(dpad, s2, e2)
                    val x2 = co2[e2]!! + 1
                    val p2 = getPath(cf2, s2, e2)
                    val ksp2 = senksp(keypad, p2, x2).toMutableList()
                    s2 = e2
                    val ksp22 = emptyList<List<Direction>>().toMutableList()
                    for (xp in ksp2.indices) {
                        val xpx = ksp2[xp].windowed(2)
                            .map { this.translate(it[0], it[1], keypad) }
                            .plus(Direction.ENTER)
                        ksp22.add(xpx)
                    }
                    mut2.add(ksp22)
                }
                x2accAll[x1acc] = perm(mut2).map { it.flatten() }
            }
            for (x in x2accAll.keys) {
                println("steps2: [${x.size}] ${x2accAll[x]!!.size} * [${x2accAll[x]!![0].size}] ${x2accAll[x]!!.size}")
                for (y in x2accAll[x]!!) {
                    x2accAll2.add(y)
                }
            }
            xacc.add(x2accAll2)
//            println("a2 ${x2accAll2.size} ${x2accAll2.first().size}")
            for (idx in 1..1) {
                var s3 = dpad.getMatches(vEnter).first()
                val min = xacc[idx-1].minOfOrNull { it.size } ?: 0
                println("idx $idx min $min")
                xacc[idx-1].forEach { x2acc ->
                    val mut3 = emptyList<List<List<Direction>>>().toMutableList()
                    if (x2acc.size == min) {
                        x2acc.forEach { l3 ->
                            val e3 = dpad.getMatches(vals[l3.toString()]!!).first()
                            val (cf3, co3) = aStar(dpad, s3, e3)
                            val x3 = co3[e3]!! + 1
                            val p3 = getPath(cf3, s3, e3)
                            val ksp3 = senksp(keypad, p3, x3).toMutableList()
                            s3 = e3
                            val ksp33 = emptyList<List<Direction>>().toMutableList()
                            for (xp in ksp3.indices) {
                                val xpx = ksp3[xp].windowed(2)
                                    .map { this.translate(it[0], it[1], keypad) }
                                    .plus(Direction.ENTER)
                                ksp33.add(xpx)
                            }
//                            println("ksp33 ${ksp33.size} ${ksp33.first().size}")
                            mut3.add(ksp33)
                        }
                        println("mut3 ${mut3.size} ${mut3.first().size}")
                        println(mut3.first())
                        for (x in perm(mut3.toList())) {
                            x3accAll2.add(x.flatten())
                        }
                    }
                }
            }
//            println("a3 ${x3accAll2.size} ${x3accAll2.first().size}")
            var row = x3accAll2.first().size
            for (x in x3accAll2) {
                if (x.size < row) {
                    row = x.size
                }
            }
            val parsed = line.joinToString("").replace("A", "").toInt()
            println("row: $row * $parsed")
            println("-----------------")
            row *= parsed
            p1 += row
        }
        println("p1: $p1")
    }

    fun pp(x: List<Direction>): String {
        var s = ""
        for (xx in x) {
            s += vals[xx.toString()]
        }
        return s
    }

    private fun <T> perm(x: List<List<T>>): List<List<T>> {
        val len = x.size // 3
        val wid = x.maxOfOrNull { it.size } ?: 0 // 4
        val combo = x.map { it.size }.reduce(Int::times) // 4 * 1 * 3
        val y = emptyList<MutableList<T>>().toMutableList()
        val xx = emptyList<MutableList<T>>().toMutableList()
        for (i in 0 until len) {
            val foo = MutableList(combo) { x[i] }.flatten().take(combo)
            xx.add(if (x[i].size == wid) foo.toMutableList() else foo.sortedBy { it.toString() }.toMutableList())
        }
        for (j in 0 until combo) {
            y.add(emptyList<T>().toMutableList())
            for (i in 0 until len) {
                y[j].add(xx[i][j])
            }
        }
        return y
    }

    private fun translate(a: Pos, b: Pos, keypad: Board): Direction =
        when (keypad.getDirection(a, b)) {
            Board.directionAll.N -> Direction.UP
            Board.directionAll.E -> Direction.RIGHT
            Board.directionAll.S -> Direction.DOWN
            Board.directionAll.W -> Direction.LEFT
            else -> Direction.ENTER
        }

    private fun getPath(cf: Map<Pos, Pos?>, start: Pos, final1: Pos): List<Pos> {
        val p2l = emptyList<Pos>().toMutableList()
        var final = final1
        while (cf.containsKey(final) && cf[final] != null) {
            p2l.add(0, final)
            final = cf[final]!!
        }
        p2l.add(0, start)
        return p2l
    }

    private fun aStar(board: Board, start: Pos, end: Pos): Pair<Map<Pos, Pos?>, Map<Pos, Int>> {
        val frontier = mutableMapOf<Int, List<Pos>>()
        frontier[0] = listOf(start)
        val cameFrom = emptyMap<Pos, Pos?>().toMutableMap()
        val costSoFar = emptyMap<Pos, Int>().toMutableMap()
        cameFrom[start] = null
        costSoFar[start] = 0

        while (frontier.isNotEmpty()) {
            val low = frontier.keys.min()
            val currentList = frontier.remove(low)
            val current = currentList!!.first()
            if (currentList.size > 1) {
                frontier[low] = currentList.drop(1)
            }
            if (current == end) {
                break
            }
            for (next in board.getNeighbors(current)) {
                if (board.board[next.y][next.x] == ' ') continue
                val newCost = costSoFar[current]!! + 1

                if (!costSoFar.containsKey(next) || newCost < costSoFar[next]!!) {
                    costSoFar[next] = newCost
                    val priority = newCost ///+ heuristic(next, end)
                    if (!frontier.containsKey(priority)) {
                        frontier.put(priority, listOf(next))
                    } else {
                        frontier.put(priority, frontier[priority]!!.plus(next))
                    }
                    cameFrom[next] = current
                }
            }
        }
        return Pair(cameFrom, costSoFar)
    }

    private fun senksp(board: Board, ksp1: List<Pos>, minCost: Int): List<List<Pos>> {
        val found = listOf(ksp1).toMutableList()

        for (i in ksp1.indices) {
            if (i == 0) continue
            if (i == ksp1.size - 1) continue
            val nope = ksp1[i]
            val o = board.board[nope.y][nope.x]
            board.board[nope.y][nope.x] = ' '
//			board.print()
            val (cf, cost) = aStar(board, ksp1[0], ksp1[ksp1.size - 1])
            board.board[nope.y][nope.x] = o
            val lowest = low(ksp1[ksp1.size - 1], cost)
            val p = getPath(cf, ksp1[0], lowest.second)
//			println(p)
//			println("------ $minCost ${lowest.first}")
            if (lowest.first + 1 == minCost && !found.contains(p)) {
                found.add(p)
            }
        }
        return found
    }

    private fun low(end: Pos, cost: Map<Pos, Int>): Pair<Int, Pos> {
        var lowest = 0
        var final = end
        var cur1 = end
        if (cost[cur1] != null) {
            val r = cost[cur1]!!
            if (r < lowest || lowest == 0) {
                lowest = r
                final = cur1
            }
        }
        return Pair(lowest, final)
    }
}
// 173472 high
//<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
//v<<A>>^A<A>AvA<^AA>A<vAAA>^A