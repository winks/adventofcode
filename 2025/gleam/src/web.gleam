import gleam/bytes_tree
import gleam/erlang/process
import gleam/http.{Post}
import gleam/http/request.{type Request}
import gleam/http/response.{type Response}
import gleam/list
import gleam/string
import mist.{type Connection, type ResponseData}
import multipart_form
import multipart_form/field
import day01
import day02
import day04
import day05
import day06

const days = ["01a", "02a", "04a", "05a", "05b", "06a", "06b"]

const index = "<html>
<head>
<title>AoC 2025</title>
</head>
<body>
<h1><a href='/'>AoC 2025</a></h1>
<hr>
%result%
<hr>
<form action='/' method='POST' enctype='multipart/form-data'>
<textarea id='txt' name='txt'></textarea>
<br>
<select id='day' name='day'>
%days%
</select>
<p>
<input type='submit'>
</p>
</form>
</body>
</html>"

fn html_days(d: List(String), acc: String) {
  case d {
    [] -> acc
    _ -> {
      let assert Ok(a) = list.first(d)
      let assert Ok(b) = list.rest(d)
      let acc = acc <> "<option value='day" <> a <> "'>Day " <> a <>"</option>\n"
      html_days(b, acc)
    }
  }
}

fn lines(s) {
  s
  |> string.replace("\r\n", "\n")
  |> string.replace("\r", "\n")
  |> string.split("\n")
}

pub fn run() {
  let not_found =
    response.new(404)
    |> response.set_body(mist.Bytes(bytes_tree.new()))

  let assert Ok(_) =
    fn(req: Request(Connection)) -> Response(ResponseData) {
      echo "Got a request from: " <> string.inspect(mist.get_client_info(req.body))
      case request.path_segments(req) {
        [] -> handle_form(req)
        _ -> not_found
      }
    }
    |> mist.new
    |> mist.bind("localhost")
    |> mist.with_ipv6
    |> mist.port(8000)
    |> mist.start

  process.sleep_forever()
}

fn handle_form(req: Request(Connection)) -> Response(ResponseData) {
  let main = case req.method {
    Post -> {
      let assert Ok(req) = mist.read_body(req, 1024 * 1024 * 30)
      let assert Ok(x) = multipart_form.from_request(req)
      let txt1 = list.filter_map(x, fn(x) { case x {
        #("txt", field.String(a)) -> Ok(a)
        #(_, _) -> Error(1)
      } })
      let assert Ok(txt) = list.first(txt1)
      let day1 = list.filter_map(x, fn(x) { case x {
        #("day", field.String(a)) -> Ok(a)
        #(_, _) -> Error(1)
      } })
      let assert Ok(day) = list.first(day1)

      case day {
        "day01a" -> day01.day01a(list.map(lines(txt), string.trim))
        "day01b" -> day01.day01b(list.map(lines(txt), string.trim))
        "day02a" -> day02.day02a(list.map(lines(txt), string.trim))
        "day02b" -> day02.day02b(list.map(lines(txt), string.trim))
        "day04a" -> day04.day04a(list.map(lines(txt), string.trim))
        "day04b" -> day04.day04b(list.map(lines(txt), string.trim))
        "day05a" -> day05.day05a(list.map(lines(txt), string.trim))
        "day05b" -> day05.day05b(list.map(lines(txt), string.trim))
        "day06a" -> day06.day06a(lines(txt))
        "day06b" -> day06.day06b(lines(txt))
        _ -> ""
      }
    }
    _ -> ""
  }

  let body = index
    |> string.replace("%result%", main)
    |> string.replace("%days%", html_days(days, ""))

  response.new(200)
  |> response.set_body(mist.Bytes(bytes_tree.from_string(body)))
}

