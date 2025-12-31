import argv
import file_streams/file_stream
import file_streams/text_encoding
import gleam/float
import gleam/io
import gleam/list
import gleam/string
import gleam/time/duration
import gleam/time/timestamp
import day01
import day02
import day03
import day04
import day05
import day06
import day12
import web

pub fn main() {
  let rstart = start()
  let rv = case argv.load().arguments {
    ["day01a", file_name] -> day01.day01a(read_lines_strip(file_name))
    ["day01b", file_name] -> day01.day01b(read_lines_strip(file_name))
    ["day02a", file_name] -> day02.day02a(read_lines_strip(file_name))
    ["day02b", file_name] -> day02.day02b(read_lines_strip(file_name))
    ["day03a", file_name] -> day03.day03a(read_lines_strip(file_name))
    ["day03b", file_name] -> day03.day03b(read_lines_strip(file_name))
    ["day04a", file_name] -> day04.day04a(read_lines_strip(file_name))
    ["day04b", file_name] -> day04.day04b(read_lines_strip(file_name))
    ["day05a", file_name] -> day05.day05a(read_lines_strip(file_name))
    ["day05b", file_name] -> day05.day05b(read_lines_strip(file_name))
    ["day06a", file_name] -> day06.day06a(read_lines_nocrlf(file_name))
    ["day06b", file_name] -> day06.day06b(read_lines_nocrlf(file_name))
    ["day12a", file_name] -> day12.day12a(read_lines_strip(file_name))
    ["web"] -> {
      web.run()
      ""
    }
    _ -> {
      io.println("Usage: aoc dayXX FILE\n       aoc web")
      ""
    }
  }
  let rstop = stop(rstart)
  io.println(float.to_string(rstop) <> " s")
  io.println(rv)
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

fn start() -> timestamp.Timestamp {
  let now = timestamp.system_time()
  now
}

fn stop(ts: timestamp.Timestamp) {
  let now = timestamp.system_time()
  //echo duration.to_iso8601_string(timestamp.difference(ts, now))
  duration.to_seconds(timestamp.difference(ts, now))
}
