import gleam/int
import gleam/list
import gleam/string

pub fn day01a(lines: List(String)) {
  let rv1 = h01(lines, 50, 0)
  echo rv1
  Nil
}

pub fn day01b(lines: List(String)) {
  let rv = h01b(lines, 50, 0)
  echo rv
  Nil
}

fn hh01up(cur: Int, num: Int, r: Int) {
  //echo [cur, num, r]
  case cur, num {
    100, 0 -> [0, r+1]
    0, 0   -> [0, r+1]
    _, 0   -> [cur, r]
    100, _ -> hh01up(0, num, r)
    0, _   -> hh01up(1, num-1, r+1)
    _, _   -> hh01up(cur+1, num-1, r)
  }
}
fn hh01dn(cur: Int, num: Int, r: Int) {
  //echo [cur, num, r]
  case cur, num {
    -100, 0 -> [0, r+1]
    0, 0    -> [0, r+1]
    _, 0    -> [cur, r]
    -100, _ -> hh01dn(0, num, r)
    0, _    -> hh01dn(-1, num+1, r+1)
    _, _    -> hh01dn(cur-1, num+1, r)
  }
}

fn h01b(lst: List(String), cur: Int, rv: Int) {
  case lst {
    [] -> rv
    _ -> {
      let assert Ok(hd) = list.first(lst)
      let assert Ok(tl) = list.rest(lst)
      let len = string.length(hd) - 1
      let assert Ok(ed) = int.parse(string.slice(from: hd, at_index: 1, length: len))
      echo lst
      echo ed
      let change = case string.first(hd) {
        Ok("R") -> hh01up(cur, ed, rv)
        Ok("L") -> hh01dn(cur, 0 - ed, rv)
        _ -> [0, 0]
      }
      echo change
      let assert Ok(c2) = list.first(change)
      let assert Ok(rv22) = list.rest(change)
      let assert Ok(rv2) = list.first(rv22)


      h01b(tl, c2, rv2)
    }
  }
}

fn hh01(n: Int, r: Int) {
  case n {
    x if x > 100 -> hh01(n-100, r)
    y if y < 0 -> hh01(n+100, r)
    z0 if z0 == 0 -> [0, r+1]
    z1 if z1 == 100 -> hh01(0, r)
    z2 if z2 == -100 -> hh01(0, r)
    _ -> [n, r]
  }
}

fn h01(lst: List(String), s: Int, rv: Int) {
  case lst {
    [] -> rv
    _ -> {
      let assert Ok(hd) = list.first(lst)
      let assert Ok(tl) = list.rest(lst)
      let le = string.length(hd) - 1
      let ed = string.slice(from: hd, at_index: 1, length: le)
      let assert Ok(ed2) = int.parse(ed)
      let n = case string.first(hd) {
        Ok("R") -> s + ed2
        Ok("L") -> s - ed2
        _ -> 0
      }
      let h = hh01(n, 0)
      let assert Ok(n2) = list.first(h)
      let assert Ok(rv11) = list.rest(h)
      let assert Ok(rv1) = list.first(rv11)
      echo [n, n2, rv1]
      echo tl

      h01(tl, n, rv+rv1)
    }
  }
}
