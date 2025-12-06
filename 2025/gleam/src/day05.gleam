import gleam/int
import gleam/list
import gleam/string

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

pub fn day05a(lines: List(String)) {
  let ranges = list.filter(lines, fn(x) { string.contains(x, "-") })
  //echo ranges
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
  //echo nums
  let nums2 = list.map(nums, fn(x) {
    let assert Ok(a) = int.parse(x)
    a
  })
  //echo nums2

  let r = h1(nums2, r2, [])
  echo list.length(list.unique(r))

  Nil
}

pub fn day05b(_lines: List(String)) {
  Nil
}
