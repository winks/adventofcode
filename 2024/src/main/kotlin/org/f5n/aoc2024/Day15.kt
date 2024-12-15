package org.f5n.aoc2024

class Day15 {
    val BOX = 'O'
    val WALL = '#'
    val UP = '^'
    val LEFT = '<'
    val RIGHT = '>'

    fun move(board: Board, step: Char) : Board {
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
        return box(board, step, line, nxt)
    }

    fun box(board: Board, step: Char, line: List<Pos>, nxt: Pos) : Board {
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
//        println(line)
//        println("$robot $nxt")
//        println(rest)
        val free = if (step == LEFT || step == UP) rest.lastOrNull { board.peek(it) == '.' } else rest.firstOrNull { board.peek(it) == '.' }
        if (free == null) {
            // do nothing
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

    fun run(args: Array<String>) {
        val lines = args[0].readAll().split("\n\n")
        var board = Board(lines[0].split("\n").toTypedArray())
//        board.print()
        for (step in lines[1].replace("\n", "")) {
//            println("step: $step")
            board = move(board, step)
//            board.print()
//            println()
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
}
