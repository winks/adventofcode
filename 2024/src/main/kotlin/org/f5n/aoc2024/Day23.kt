package org.f5n.aoc2024

class Day23 {
    fun run(args: Array<String>) {
        val lines = args[0].readLines().map { it.split("-") }
        val dir = emptyMap<String, MutableSet<String>>().toMutableMap()
        val dirSet = emptyMap<Set<String>, Int>().toMutableMap()
        val dirSet2 = emptyMap<Set<String>, Int>().toMutableMap()
        lines.forEach {
            if (!dir.containsKey(it[0])) {
                dir[it[0]] = emptySet<String>().toMutableSet()
            }
            if (!dir.containsKey(it[1])) {
                dir[it[1]] = emptySet<String>().toMutableSet()
            }
            dir[it[0]]!!.add(it[1])
            dir[it[1]]!!.add(it[0])
            dirSet[setOf(it[0], it[1])] = 1
        }

        for (k1 in dir.keys) {
            val v = dir[k1]!!.toList()
            for (k2 in v.indices) {
                for (k3 in v.indices) {
                    if (k2 == k3) continue
                    val d = setOf(v[k2], v[k3])
                    if (dirSet.containsKey(d)) {
                        dirSet2[d.plus(k1)] = 1
                    }
                }
            }
        }
        val p1 = dirSet2.keys.toSet().filter { it.any { it.startsWith("t") } }
        println("p1 ${p1.size}")
        val p2 = bk(emptySet(), dir.keys, emptySet(), dir)
        println("p2 ${p2.maxByOrNull { it.size }?.sorted()?.joinToString(",")}")
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
