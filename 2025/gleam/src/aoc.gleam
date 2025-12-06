import argv
import file_streams/file_stream
import file_streams/text_encoding
import gleam/io
import gleam/list
import gleam/string
import day01
import day02
import day05
import day06

pub fn main() {
  case argv.load().arguments {
    ["day01a", file_name] -> day01.day01a(read_lines_strip(file_name))
    ["day01b", file_name] -> day01.day01b(read_lines_strip(file_name))
    ["day02a", file_name] -> day02.day02a(read_lines_strip(file_name))
    ["day02b", file_name] -> day02.day02b(read_lines_strip(file_name))
    ["day05a", file_name] -> day05.day05a(read_lines_strip(file_name))
    ["day05b", file_name] -> day05.day05b(read_lines_strip(file_name))
    ["day06a", file_name] -> day06.day06a(read_lines_nocrlf(file_name))
    ["day06b", file_name] -> day06.day06b(read_lines_nocrlf(file_name))
    _ -> io.println("Usage: aoc dayXX FILE")
  }
}

fn read_acc(fs, acc, strip) {
  case file_stream.read_line(fs) {
    Ok(s) -> case strip {
        2 -> read_acc(fs, [string.replace(s,"\n",""), ..acc], strip)
        1 -> read_acc(fs, [string.trim(s), ..acc], strip)
        _ -> read_acc(fs, [s, ..acc], strip)
      }
    //Error(file_stream_error.Eof) -> acc
    _ -> acc
  }
}

fn read_lines_x(filename: String, strip: Int) -> List(String) {
  let encoding = text_encoding.Unicode
  let assert Ok(fs) = file_stream.open_read_text(filename, encoding)
  let acc : List(String) = []

  list.reverse(read_acc(fs, acc, strip))
}

fn read_lines_nocrlf(filename:String) -> List(String) {
  read_lines_x(filename, 2)
}

fn read_lines_strip(filename:String) -> List(String) {
  read_lines_x(filename, 1)
}

//fn read_lines(filename:String) -> List(String) {
//  read_lines_x(filename, 0)
//}
