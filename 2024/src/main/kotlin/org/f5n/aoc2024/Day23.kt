package org.f5n.aoc2024

class Day23 {
    fun run(args: Array<String>) {
        val lines = args[0].readLines().map { it.split("-") }
        val dir = emptyMap<String, MutableSet<String>>().toMutableMap()
        val dir2 = emptyMap<Set<String>, Int>().toMutableMap()
        val all = emptySet<String>().toMutableSet()
        lines.forEach {
            if (!dir.containsKey(it[0])) {
                dir[it[0]] = emptySet<String>().toMutableSet()
            }
            if (!dir.containsKey(it[1])) {
                dir[it[1]] = emptySet<String>().toMutableSet()
            }
            dir[it[0]]!!.add(it[1])
            dir[it[1]]!!.add(it[0])
            dir2[setOf(it[0], it[1])] = 1
            all.addAll(it)
        }

        val tri = emptySet<Set<String>>().toMutableSet()
        for (k1 in all) {
            for (k2 in all) {
                if (k1 == k2) continue
                for (k3 in all) {
                    if (k1 == k3) continue
                    if (k2 == k3) continue
                    if (dir2.containsKey(setOf(k1, k2)) &&
                        dir2.containsKey(setOf(k2, k3)) &&
                        dir2.containsKey(setOf(k1, k3))
                    ) {
                        tri.add(setOf(k1, k2, k3))
                    }
                }
            }
        }
        val p1 = tri.filter { it.any { x -> x.startsWith("t") } }
        val p2 = bk(emptySet(), all, emptySet(), dir)
        println("p1 ${p1.size}")
        println("p2 ${p2.maxByOrNull { it.size }?.sorted()?.joinToString(",")}")
    }
    private fun dfs(board: Map<String, Set<String>>, p: String, visited: MutableSet<String>): MutableSet<String> {
        visited.add(p)
        val ne = board[p]!!.filter { !visited.contains(it) }
        if (p == "co") println("$p 1 $ne - [$visited]")
        for (n in ne) {
            var others = board[n]!!.filter { it != p }
            //others = ne.filter { it != p }
            if (p == "co") println("$p $n / $ne - $others - [$visited]")
            if (board[n]!!.contains(p) && others.intersect(ne).size > 1) {
                visited.add(n)
            }
            else dfs(board, n, visited)
        }
        return visited
    }
    // Bron-Kerbosch
    private fun bk(R: Set<String>, P: Set<String>, X: Set<String>, m: Map<String, Set<String>>) : Set<Set<String>> {
        val cliques = emptySet<Set<String>>().toMutableSet()
        if (P.isEmpty() && X.isEmpty()) {
            cliques.add(R)
        }
        var p = P
        var x = X
        while (p.isNotEmpty()) {
            val v = p.first()
            val r2 = R.plus(v)
            val ne = m[v]!!
            val p2 = p.intersect(ne)
            val x2 = x.intersect(ne)
            cliques.addAll(bk(r2, p2, x2, m))
            p = p.minus(v)
            x = x.plus(v)
        }
        return cliques
    }
}
