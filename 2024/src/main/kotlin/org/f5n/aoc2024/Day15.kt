package org.f5n.aoc2024

import kotlin.math.abs

class Day15 {
    val BOX = 'O'
    val WALL = '#'
    val UP = '^'
    val DOWN = 'v'
    val LEFT = '<'
    val RIGHT = '>'
    val BOXL = '['
    val BOXR = ']'

    private fun move(board: Board, step: Char, fn: (Board, Char, List<Pos>, Pos) -> Board) : Board {
        val robot = board.getMatches("@")[0]
        val line =
            when (step) {
                LEFT, RIGHT -> board.getLineAll(robot, Pos(robot.x + 1, robot.y)).toList().sortedBy { it.x }
                else -> board.getLineAll(robot, Pos(robot.x, robot.y + 1)).toList().sortedBy { it.y }
            }
        val nxt = line[line.indexOf(robot) + if (step == LEFT || step == UP) -1 else 1]
        if (board.peek(nxt) == WALL) {
            return board
        } else if (board.peek(nxt) == '.') {
            board.board[robot.y][robot.x] = '.'
            board.board[nxt.y][nxt.x] = '@'
            return board
        }
        return fn(board, step, line, nxt)
    }

    fun box(board: Board, step: Char, line: List<Pos>, nxt: Pos) : Board {
        val robot = board.getMatches("@")[0]
        val rest = if (step == LEFT || step == UP) {
            val r = line.subList(0, line.indexOf(nxt))
            val s = r.lastOrNull { board.peek(it) == WALL }
            if (s != null) {
                r.subList(r.indexOf(s), r.size)
            } else {
                r
            }
        } else {
            val r = line.subList(line.indexOf(nxt), line.size)
            val s = r.firstOrNull { board.peek(it) == WALL }
            if (s != null) {
                r.subList(0, r.indexOf(s))
            } else {
                r
            }
        }
        val free = if (step == LEFT || step == UP) rest.lastOrNull { board.peek(it) == '.' } else rest.firstOrNull { board.peek(it) == '.' }
        if (free == null) {
            return board
        } else {
            val nxt2 = line[line.indexOf(nxt) + if (step == LEFT || step == UP) -1 else 1]
            if (board.peek(nxt2) == '.') {
                board.board[robot.y][robot.x] = '.'
                board.board[nxt.y][nxt.x] = '@'
                board.board[nxt2.y][nxt2.x] = BOX
            } else {
                board.board[robot.y][robot.x] = '.'
                board.board[nxt.y][nxt.x] = '@'
                board.board[free.y][free.x] = BOX
            }
            return board
        }
    }

    fun box2(board: Board, step: Char, line: List<Pos>, nxt: Pos) : Board {
        val robot = board.getMatches("@")[0]
        val rest = if (step == LEFT || step == UP) {
            val r = line.subList(0, line.indexOf(nxt))
            val s = r.lastOrNull { board.peek(it) == WALL }
//            println("r is $r / s is $s")
            if (s != null) {
                r.subList(r.indexOf(s), r.size)
            } else {
                r
            }
        } else {
            val r = line.subList(line.indexOf(nxt), line.size)
            val s = r.firstOrNull { board.peek(it) == WALL }
//            println("r is $r / s is $s")
            if (s != null) {
                r.subList(0, r.indexOf(s))
            } else {
                r
            }
        }
        val free = if (step == LEFT || step == UP) rest.lastOrNull { board.peek(it) == '.' } else rest.firstOrNull { board.peek(it) == '.' }
        if (free == null) {
            // do nothing
            return board
        } else {
            when (step) {
                LEFT -> {
                    var left = true
                    for (i in free.x until robot.x-1) {
                        board.board[free.y][i] = if (left) BOXL else BOXR
                        left = !left
                    }
                    board.board[robot.y][robot.x] = '.'
                    board.board[nxt.y][nxt.x] = '@'
                }
                RIGHT -> {
                    var left = false
                    for (i in robot.x+1 until free.x+1) {
                        board.board[free.y][i] = if (left) BOXL else BOXR
                        left = !left
                    }
                    board.board[robot.y][robot.x] = '.'
                    board.board[nxt.y][nxt.x] = '@'
                }
                UP, DOWN -> {
//                    println("free $free - robot $robot")
                    val todo = mutableSetOf(robot)
                    var loop_start = if (step == UP) robot.y-1 else robot.y+1
                    var loop_end = if (step == UP) 0 else board.length
                    val offset = if (step == UP) 1 else -1
                    var yy = loop_start
                    while (yy != loop_end) {
                        val li = todo.toList().sortedBy { it.x }.filter { it.y == yy+offset }
//                        println("prep: $yy ($loop_start, $loop_end) li $li")
                        if (abs(yy - robot.y) == 1) {
                            if (board.board[yy][robot.x] == BOXL) {
                                todo.add(Pos(robot.x, yy))
                            } else {
                                todo.add(Pos(robot.x-1, yy))
                            }
                            todo.remove(robot)
//                            println("robot todo $todo")
                        } else {
                            for(ll in li) {
                                // []
                                // []
                                if (board.board[yy][ll.x] == BOXL) {
                                    todo.add(Pos(ll.x, yy))
                                }
                                // []
                                //  []
                                if (board.board[yy][ll.x] == BOXR ) {
                                    todo.add(Pos(ll.x-1, yy))
                                }
                                //  []
                                // []
                                if (board.board[yy][ll.x+1] == BOXL) {
                                    todo.add(Pos(ll.x+1, yy))
                                }
                            }
                        }
                        if (step == UP) yy-- else yy++
                    }
//                    println("end todo $todo")
                    // start test run
                    var canDo = true
                    loop_start = if (step == DOWN) board.length else 0
                    loop_end = if (step == DOWN) robot.y+1 else robot.y-offset
                    yy = loop_start
                    while (yy != loop_end) {
                        val li = todo.toList().filter { it.y == yy+offset }
                        for(a in li) {
                            if (board.board[yy][a.x] == WALL || board.board[yy][a.x+1] == WALL) {
                                println("abort1: wall at ${a.x}, ${yy} during $step")
                                canDo = false
                            }
                            if (board.board[yy][a.x+1] == BOXL && !todo.contains(Pos(a.x+1, yy))) {
                                println("abort2: box at ${a.x+1}, ${yy} during $step")
                                canDo = false
                            }
                            if (board.board[yy][a.x] == BOXR && !todo.contains(Pos(a.x-1, yy))) {
                                println("abort3: box at ${a.x+1}, ${yy} during $step")
                                canDo = false
                            }
                        }
                        if (step == UP) yy++ else yy--
                    }
                    if (!canDo) return board
                    // end test run
                    loop_start = if (step == DOWN) board.length else 0
                    loop_end = if (step == DOWN) robot.y+1 else robot.y-offset
                    yy = loop_start
                    while (yy != loop_end) {
//                        println("print: $yy ($loop_start, $loop_end)")
                        val li = todo.toList().filter { it.y == yy+offset }
//                        println("li $li")
                        for(a in li) {
                            if (board.board[yy][a.x] == WALL || board.board[yy][a.x+1] == WALL) {
                                println("abort1: wall at ${a.x}, ${yy} during $step")
                                return board
                            }
                            if (board.board[yy][a.x+1] == BOXL && !todo.contains(Pos(a.x+1, yy))) {
                                println("abort2: box at ${a.x+1}, ${yy} during $step")
                                return board
                            }
                            if (board.board[yy][a.x] == BOXR && !todo.contains(Pos(a.x-1, yy))) {
                                println("abort3: box at ${a.x+1}, ${yy} during $step")
                                return board
                            }
                        }
                        for(a in li) {
                            board.board[yy][a.x] = board.board[yy+offset][a.x]
                            board.board[yy][a.x+1] = board.board[yy+offset][a.x+1]
                            board.board[yy+offset][a.x] = '.'
                            board.board[yy+offset][a.x+1] = '.'
                        }
                        if (step == UP) yy++ else yy--
                    }
                    board.board[robot.y][robot.x] = '.'
                    board.board[nxt.y][nxt.x] = '@'
                }
                else -> {
                }
            }
            return board
        }
    }

    fun run(args: Array<String>) {
        val lines = args[0].readAll().split("\n\n")
        var board = Board(lines[0].split("\n").toTypedArray())
        for (step in lines[1].replace("\n", "")) {
            board = move(board, step, ::box)
        }
        var p1 = 0
        for (y in 0 until board.length) {
            for (x in 0 until board.width) {
                if (board.board[y][x] == BOX) {
                    p1 += 100 * y + x
                }
            }
        }
        println("p1 : $p1")
    }
    fun run2(args: Array<String>) {
        val lines = args[0].readAll().split("\n\n")
        val line = lines[0]
            .replace("#","##")
            .replace(".", "..")
            .replace("@", "@.")
            .replace("O", "[]")
        var board = Board(line.split("\n").toTypedArray())
        board.print()
        var i = 0
        val steps = lines[1].replace("\n", "")
        println("steps: ${steps.length}")
        for (step in steps) {
//            println("step: $step step $i")
            board = move(board, step, ::box2)
            i++
        }
        board.print()
        var p2 = 0
        for (y in 0 until board.length) {
            for (x in 0 until board.width) {
                if (board.board[y][x] == BOXL) {
                    p2 += 100 * y + x
                }
            }
        }
        println("p2 : $p2")
    }
}
