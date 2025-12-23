import gleam/int
//import gleam/io
import gleam/list
//import gleam/regexp
import gleam/string

fn h1(s, acc, idx) {
  let le = string.length(s)
  case idx {
    n if n >= le -> acc
    _ -> {
      let t = string.slice(s, idx, 1)
      case t {
        "+" -> h1(s, [#(idx, t), ..acc], idx+1)
        "*" -> h1(s, [#(idx, t), ..acc], idx+1)
        _   -> h1(s, acc, idx+1)
      }
    }
  }
}

fn get_slice(lst, acc, idx) {
  case lst {
    [] -> list.reverse(acc)
    _ -> {
      let assert Ok(hd) = list.first(lst)
      let assert Ok(tl) = list.rest(lst)

      let assert Ok(#(from, _f)) = list.first(idx)
      let assert Ok(to0) = list.rest(idx)
      let assert Ok(#(to, _t)) = list.first(to0)

      let t = string.slice(hd, from, to)
      get_slice(tl, [t, ..acc], idx)
    }
  }
}

fn h2(cols, idx, acc) {
  let le = list.length(idx)
  case le {
    i if i < 2 -> acc
    _ -> {
      let assert Ok(a) = list.first(idx)
      let assert Ok(ar) = list.rest(idx)
      let assert Ok(b) = list.first(ar)
      //echo [a, b]
      let #(a1, _) = a
      let #(c1, _) = b
      let c2 = case c1 {
        n if n == a1 -> 99
        _ -> c1-a1
      }
      let x = get_slice(cols, [], [a, #(c2, "")])
      //echo x
      h2(cols, ar, [x, ..acc])
    }
  }
}

fn h3(rx, ops, acc) {
 case rx {
   [] -> acc
   _ -> {
     let assert Ok(rs) = list.first(rx)
     let assert Ok(rr) = list.rest(rx)
     let assert Ok(op) = list.first(ops)
     let assert Ok(or) = list.rest(ops)

     let #(_, o) = op
     let rs2 = list.map(rs, fn(x) {
       let assert Ok(x2) = int.parse(string.trim(x))
       x2
     })

     let rv = case o {
       "+" -> list.fold(rs2, 0, fn(acc, a) { acc + a })
       "*" -> list.fold(rs2, 1, fn(acc, a) { acc * a })
        _ -> 0
     }
     h3(rr, or, [rv, ..acc])
   }
 }
}

pub fn day06a(lines: List(String)) {
  let rev = list.reverse(lines)
  let assert Ok(ops_s) = list.first(rev)
  let foo = h1(ops_s, [], 0)
  let assert Ok(foo2) = list.first(foo)
  let ops = list.reverse([foo2, ..foo])
  let cols = case list.rest(rev) {
    Ok(x) -> list.reverse(x)
    _ -> []
  }
  let hx = list.reverse(h2(cols, ops, []))
  let hy = h3(hx, ops, [])

  int.to_string(list.fold(hy, 0, fn(acc, a) { acc + a }))
}

fn gb(lst, acc, idx) {
  case idx {
    0 -> acc
    _ -> {
      let t = list.map(lst, fn(x) { string.slice(x, idx-1, 1) } )
      let t2 = list.fold(t, "", fn(acc, a) { acc <> a })
      gb(lst, [string.trim(t2), ..acc], idx-1)
    }
  }
}

fn get_slice_b(lst, acc) {
  case lst {
    [] -> acc
    _ -> {
      let assert Ok(hd) = list.first(lst)
      let assert Ok(tl) = list.rest(lst)
      let assert Ok(x) = list.first(hd)
      let idx = string.length(x)
      let t = list.filter(gb(hd, [], idx), fn(x) { string.length(x) > 0 })
      get_slice_b(tl, [t, ..acc])
    }
  }
}

pub fn day06b(lines: List(String)) {
  let rev = list.reverse(lines)
  let assert Ok(ops_s) = list.first(rev)
  let foo = h1(ops_s, [], 0)
  let assert Ok(foo2) = list.first(foo)
  let ops = list.reverse([foo2, ..foo])
  let cols = case list.rest(rev) {
    Ok(x) -> list.reverse(x)
    _ -> []
  }
  let hx = list.reverse(h2(cols, ops, []))

  let hz = list.reverse(get_slice_b(hx, []))
  let hy = h3(hz, ops, [])

  int.to_string(list.fold(hy, 0, fn(acc, a) { acc + a }))
}
