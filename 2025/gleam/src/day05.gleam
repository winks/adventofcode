import gleam/int
import gleam/list
import gleam/result
import gleam/string

pub fn day05a(lines: List(String)) {
  let ranges = list.filter(lines, fn(x) { string.contains(x, "-") })
  let r2 = list.map(ranges, fn(x) {
    let pairs = list.map(string.split(x, "-"), fn(x) {
      let assert Ok(a) = int.parse(x)
      a
    })
    let assert Ok(le) = list.first(pairs)
    let assert Ok(r) = list.rest(pairs)
    let assert Ok(ri) = list.first(r)
    [le, ri]
  })
  let nums = list.filter(lines, fn(x) { !string.contains(x, "-") && string.length(x) > 0 })
  let nums2 = list.map(nums, fn(x) {
    let assert Ok(a) = int.parse(x)
    a
  })

  int.to_string(list.length(list.unique(h1(nums2, r2, []))))
}

pub fn day05b(lines: List(String)) {
  let ranges = list.filter(lines, fn(x) { string.contains(x, "-") })
  let r2 = list.map(ranges, fn(x) {
    let pairs = list.map(string.split(x, "-"), fn(x) {
      let assert Ok(a) = int.parse(x)
      a
    })
    let assert Ok(le) = list.first(pairs)
    let ri = list.rest(pairs)
      |> result.try(list.first(_))
      |> result.unwrap(0)
    #(le, ri)
  })
  let r3 = list.sort(r2, fn(x, y) {
    let #(x1, _) = x
    let #(y1, _) = y
    int.compare(x1, y1)
  })
  let r4 = list.reverse(r3)
  let assert Ok(rx) = list.first(r4)
  let r5 = list.reverse([rx, ..r4])
  let b = list.reverse(bb(r5, []))
  let rv2 = list.map(b, fn(x) {
    let #(a,b) = x
    b - a + 1
  })
  int.to_string(list.fold(rv2, 0, fn(acc, x) { acc + x }))
}

fn h1(a, p, rv) {
  case a {
    [] -> rv
    _ -> {
      let assert Ok(hd) = list.first(a)
      let assert Ok(tl) = list.rest(a)
      let p2 = p
      let rv1 = list.map(p2, fn(x) {
        let assert Ok(x1) = list.first(x)
        let assert Ok(xr) = list.rest(x)
        let assert Ok(x2) = list.first(xr)
        case hd {
          y if y >= x1 && y <= x2 -> hd
          _ -> 0
        }
      })
      let r = list.filter(rv1, fn(x) { x > 0 })
      h1(tl, p, list.flatten([rv,r]))
    }
  }
}


fn bb(lst, acc) {
  case list.first(lst) {
    Error(_) -> acc
    Ok(#(lo1, hi1)) -> {
      let assert Ok(tl) = list.rest(lst)
      case list.first(tl) {
        Error(_) -> {
          [#(lo1, hi1), ..acc]
        }
        Ok(#(lo2, hi2)) -> {
          case lo2, hi2 {
            x, y if x <= hi1 && y <= hi1 -> {
              let assert Ok(tl2) = list.rest(tl)
              bb([#(lo1, hi1), ..tl2], acc)
            }
            x, y if x <= hi1 && y > hi1 -> {
              bb([#(lo1, hi2), ..tl], acc)
            }
            x, _ if x >= hi1 -> {
              bb(tl, [#(lo1, hi1), ..acc])
            }
            _, _ -> bb(tl, acc)
          }
        }
      }
    }
  }
}

