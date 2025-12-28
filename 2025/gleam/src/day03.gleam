import gleam/int
//import gleam/io
import gleam/list
import gleam/string

fn b2(bank: List(Int), idx: Int, pos: Int, acc: List(Int)) -> List(Int) {
  case idx {
    0 -> acc
    _ -> {
      let end = list.length(bank) - idx + 1
      let slice = list.take(list.drop(bank, pos),end-pos)
      let assert Ok(top) = list.max(slice, int.compare)
      let pos = list.length(list.take_while(slice, fn(x) { x != top })) + 1
      //echo slice
      //echo top
      //echo pos
      //echo end
      b2(bank, idx-1, pos, list.append(acc, [top]))
    }
  }
}

fn b(banks: List(List(Int)), k: Int, acc: List(Int)) -> List(Int) {
  case banks {
    [] -> acc
    _ -> {
      let assert Ok(hd) = list.first(banks)
      let assert Ok(tl) = list.rest(banks)
      let assert Ok(x) = int.parse(string.join(list.map(b2(hd, k, 0, []), int.to_string), ""))
      b(tl, k, list.append(acc, [x]))
    }
  }
}

pub fn day03a(lines: List(String)) {
  let lines = list.map(lines, fn(x) {
    list.map(string.split(x, ""), fn(y) {
      let assert Ok(z) = int.parse(y)
      z
    })
  })
  let r11 = b(lines, 2, [])
  let assert Ok(r1) = list.reduce(r11, fn(acc, x) { acc + x })
  int.to_string(r1)
}

pub fn day03b(lines: List(String)) {
  let lines = list.map(lines, fn(x) {
    list.map(string.split(x, ""), fn(y) {
      let assert Ok(z) = int.parse(y)
      z
    })
  })
  let r11 = b(lines, 12, [])
  let assert Ok(r1) = list.reduce(r11, fn(acc, x) { acc + x })
  int.to_string(r1)
}
