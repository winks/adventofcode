package org.f5n.aoc2024

import jdk.internal.org.jline.utils.Colors.s

class Day12 {
	fun getArea(b: Board): MutableSet<Pos> {
		val area = emptySet<Pos>().toMutableSet()
		for (y in 0 until b.length) {
			for (x in 0 until b.width) {
				val p = Pos(x, y)
				if (b.peek(p) == '.') continue
				area.add(p)
			}
		}
		return area
	}
	fun getPeri(b: Board, area: Set<Pos>): MutableSet<Pos> {
		val peri = emptySet<Pos>().toMutableSet()
		for (y in 0 until b.length) {
			for (x in 0 until b.width) {
				val p = Pos(x, y)
				if (b.peek(p) == '.') continue
				if (!area.contains(p)) continue
				b.getNeighbors(p).forEach {
					if (b.peek(it) == '.') peri.add(it)
				}
			}
		}
		return peri
	}
	fun run1(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
		val visited = emptySet<Pos>().toMutableSet()
		val clusters = emptySet<Set<Pos>>().toMutableSet()
		println("length ${board.length} width ${board.width}")
		for (y in 0 until board.length) {
			for (x in 0 until board.width) {
				val pos = Pos(x, y)
//				println(pos)
				if (visited.contains(pos)) continue
				val cl = board.getCluster(pos)
//				println(cl)
//				println(cl.size)
				val bb = board.from(cl.toList(), board.peek(pos).toString())
				bb.print()
				visited.addAll(cl)
				if (!clusters.contains(cl)) clusters.add(cl)
			}
		}
		println("clusters: ${clusters.size}")
		var p1 = 0
		var p2 = 0
		for (c in clusters) {
			val b = board.from(c.toList())
			val area = getArea(b)
			val peri = getPeri(b, area)
			var ps = peri.size
			var ps2 = peri.size
			peri.forEach { p ->
				val ne = b.getNeighbors(p)
//				println("$p ${ne.filter { b.valid(it) }}")
//				println("$p ${ne.filter { b.valid(it) && b.peek(it) == ks[0] }}")
				val s =  ne.filter { b.valid(it) && b.peek(it) == 'A' }.size
				if (s > 1) {
					ps += (s-1)
				}
			}
			println("area ${area.size} peri ${ps}")
			p1 += area.size * ps
			p2 += area.size * ps2
		}
		println(clusters.size)
		println("p1: $p1")
		println("p2: $p2")

	}
	fun run(args: Array<String>) {
		val lines = args[0].readLines()
		val board = Board(lines)
//		board.print()
		val m = emptyMap<String, List<Pos>>().toMutableMap()
		for (y in 0 until board.length) {
			for (x in 0 until board.width) {
				val pos = Pos(x, y)
				val c = board.peek(pos)
				if (!m.containsKey(c.toString())) m[c.toString()] = listOf(pos)
				else m[c.toString()] = m[c.toString()]!!.plus(pos)
			}
		}
//		println(m)
		var p1 = 0
		var remote = emptyList<Set<Pos>>().toMutableList()
		for (k in 'A'.toChar()..'Z'.toChar()) {
			val ks = k.toString()
			if (!m.containsKey(ks)) continue
			val b = board.from(m[ks]!!)
//			b.print()

			val area = getArea(b)
			val clusters = emptyMap<Int, Set<Pos>>().toMutableMap()
			for (e in area) {
				val c = b.getCluster(e)
				clusters[c.size] = c
			}
			if (clusters.keys.size > 1) {
				println("clusters ${clusters}")
				clusters.keys.sorted().take(clusters.keys.size - 1).forEach {
					remote.add(clusters[it]!!)
					area.removeAll(clusters[it]!!)
					println("added ${clusters[it]!!} to remote")
				}
			}
//			println(area.sortedBy { it.y }.sortedBy { it.x })
//			println(peri.sortedBy { it.y }.sortedBy { it.x })
			val peri = getPeri(b, area)
			var ps = peri.size
			peri.forEach { p ->
				val ne = board.getNeighbors(p)
//				println("$p ${ne.filter { b.valid(it) }}")
//				println("$p ${ne.filter { b.valid(it) && b.peek(it) == ks[0] }}")
				val s =  ne.filter { b.valid(it) && b.peek(it) == 'A' }.size
				if (s > 1) {
					ps += (s-1)
				}
			}
			println("xx $ks ${area.size} * ${peri.size} / $ps = ${ps * area.size}")
			println("----------")
			p1 += ps * area.size
		}
		println(remote)
		for (k in remote) {
			println("remote ${k}")
			val b = board.from(k.toList())
//			b.print()
			val area = getArea(b)
			val peri = getPeri(b, area)
			var ps = peri.size
			peri.forEach { p ->
				val ne = board.getNeighbors(p)
				val s =  ne.filter { b.valid(it) && b.peek(it) == 'A' }.size
				if (s > 1) {
					ps += (s-1)
				}
			}
			p1 += ps * area.size

		}
		println("p1: $p1")
	}
}
