import gleam/float
import gleam/int
import gleam/list
import gleam/result
import gleam/string

pub fn day12a(lines: List(String)) {
  let x = parse(lines, [], [], [])
  let reg = get_regions(x.1, [])
  let pcs = list.map(x.0, get_piece(_, []))

  let rv = list.map(reg, fn(r) {
    let assert Ok(left) = list.first(r)
    let assert Ok(right) = list.last(r)
    let assert Ok(x) = list.first(left)
    let assert Ok(y) = list.last(left)
    let z1 = list.zip(right, pcs)
    let z2 = list.map(z1, fn(z) {
      let sz = z.0 * size(z.1)
      sz
    })
      |> list.reduce(fn(x, acc) { acc + x})
      |> result.unwrap(0)
    case z2 {
      a if a > x*y -> 0
      _ -> {
        let xx = float.floor(int.to_float(x) /. 3.0) //|> result.unwrap(0.0)
        let yy = float.floor(int.to_float(y) /. 3.0) //|> result.unwrap(0.0)
        let s = int.to_float(size([right]))
        case xx *. yy {
          b if b >=. s -> 1
          _ -> 0
        }
      }
    }
  })
  int.to_string(size([rv]))
}

pub fn day12b(_lines: List(String)) {
  ""
}

fn parse(lines: List(String), buf: List(String), acc_p: List(List(String)), acc_r: List(String)) {
  case lines {
    [] -> #(acc_p, acc_r)
    [tl] -> #(acc_p, list.append(acc_r, [tl]))
    ["", ..tl] -> parse(tl, [], list.append(acc_p, [buf]), acc_r)
    [hd, ..tl] -> {
      case string.contains(hd, "x") {
        True -> parse(tl, buf, acc_p, list.append(acc_r, [hd]))
        False -> parse(tl, list.append(buf, [hd]), acc_p, acc_r)
      }
    }
  }
}

fn get_regions(lines: List(String), acc: List(List(List(Int)))) {
  case lines {
    [] -> acc
    [hd, ..tl] -> {
      let p = string.split(hd, ": ")
      let left = list.first(p)
        |> result.map(string.split(_, "x"))
        |> result.unwrap([])
        |> list.map(int.parse)
        |> list.map(result.unwrap(_, 0))
      let right = list.rest(p)
        |> result.unwrap([])
        |> list.first()
        |> result.unwrap("")
        |> string.split(" ")
        |> list.map(int.parse)
        |> list.map(result.unwrap(_, 0))
      get_regions(tl, list.append(acc, [[left, right]]))
    }
  }
}

fn get_piece(lines: List(String), acc: List(List(Int))) {
  case lines {
    [] -> acc
    [hd, ..tl] -> {
      case string.contains(hd, ":") {
        True -> get_piece(tl, acc)
        False -> {
          let hd = hd
            |> string.replace("#", "1")
            |> string.replace(".", "0")
          let h3 = string.split(hd, "")
            |> list.map(int.parse)
            |> list.map(result.unwrap(_, 0))
          get_piece(tl, list.append(acc, [h3]))
        }
      }
    }
  }
}

fn size(p: List(List(Int)) ) {
  result.unwrap(list.reduce(list.flatten(p), fn(x, acc) { acc + x } ), 0)
}

