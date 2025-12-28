import gleam/int
//import gleam/io
import gleam/list
import gleam/string

//fn pp(m) {
//  case list.first(m) {
//    Error(_) -> Nil
//    Ok(line) -> {
//      io.println(list.fold(line, "", fn(acc, x) { acc <> x}))
//      let assert Ok(r) = list.rest(m)
//      pp(r)
//    }
//  }
//}

fn split(lines, acc) {
  case list.first(lines) {
    Error(_) -> acc
    Ok(line) -> {
      let assert Ok(r) = list.rest(lines)
      let x = string.split(line, "")
      split(r, [x, ..acc])
    }
  }
}

fn get_n(m0, y, x) {
  let m1 = list.map(m0, fn (row) { list.drop(row, x-1) })
  let assert Ok(le) = list.first(m0)
  let len = list.length(le)
  let k = case x {
    0 -> 2
    l if l >= len-1 -> 2
    _ -> 3
  }
  let m2 = list.map(m1, fn (row) { list.take(row, k) })
  let leny = list.length(m0)
  let ky = case y {
    0 -> 2
    l if l >= leny-1 -> 2
    _ -> 3
  }
  let m3 = list.drop(m2, y-1)
  let m4 = list.take(m3, ky)
  m4
}

fn cur(m0, y, x) {
  let m1 = list.map(m0, fn (row) { list.drop(row, x) })
  let m2 = list.map(m1, fn (row) { list.take(row, 1) })
  let m3 = list.drop(m2, y)
  let m4 = list.take(m3, 1)
  let assert Ok(r) = list.first(list.flatten(m4))
  r
}

fn help1(maze, y, x) {
  let cur = cur(maze, y, x)
  let a = case cur {
    "@" -> {
      let n = get_n(maze, y, x)
      let p = list.filter(list.flatten(n), fn(x) { x == "@" })
      //echo n
      //echo p
      let pl = list.length(p)
      case pl {
        n if n < 5 -> 1
        _ -> 0
      }
    }
    _ -> {
     //echo "-"
     0
    }
  }
  //io.println("y: " <> int.to_string(y) <> " x: " <> int.to_string(x) <> " cur: " <> cur <> " a: " <>
  //int.to_string(a))
  a
}

fn run1(maze, y, x, x0, acc) {
  let a = acc + help1(maze, y, x)
  case y, x {
    0, 0 -> a
    _, 0 -> run1(maze, y-1, x0,  x0, a)
    0, _ -> run1(maze, y,   x-1, x0, a)
    _, _ -> run1(maze, y,   x-1, x0, a)
  }
}

pub fn day04a(lines: List(String)) {
  let maze = list.reverse(split(lines, []))
  //pp(maze)
  let assert Ok(fx) = list.first(maze)
  let y = list.length(maze) - 1
  let x = list.length(fx) - 1
  let r = run1(maze, y, x, x, 0)
  int.to_string(r)
}

pub fn day04b(_lines: List(String)) {
  ""
}
