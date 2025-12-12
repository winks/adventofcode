import gleam/int
import gleam/list
import gleam/regexp
import gleam/string

pub fn day02a(lines: List(String)) {
  //echo lines
  let assert Ok(line) = list.first(lines)
  let parts = string.split(line, on: ",")
  //echo parts
  echo a1(parts, 0)
  Nil
}

pub fn day02b(_lines: List(String)) {
  Nil
}

fn a1(lst: List(String), rv: Int) {
  case lst {
    [] -> rv
    _ -> {
      let assert Ok(hd) = list.first(lst)
      let assert Ok(tl) = list.rest(lst)

      let p = string.split(hd, on: "-")
      let assert Ok(i) = list.first(p)
      let assert Ok(jj) = list.rest(p)
      let assert Ok(j) = list.first(jj)
      let assert Ok(i2) = int.parse(i)
      let assert Ok(j2) = int.parse(j)
      let r = a2(i2, j2, 0)

      a1(tl, rv+r)
    }
  }
}

fn a2(from: Int, to: Int, rv: Int) {
  //echo [from, to]
  case from, to {
    x, y if x > y -> rv
    _, _ -> {
        let assert Ok(re) = regexp.from_string("^(\\d+)\\1$")
        let c = regexp.check(re, int.to_string(from))
        case c {
          True -> a2(from+1, to, rv+from)
          False -> a2(from+1, to, rv)
        }
    }
  }
}
