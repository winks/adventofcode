# Nim 1.0.4 // nim c -r day3.nim
import parseUtils
import strutils

type
  Point* = tuple[x:int, y:int]
  PointList* = seq[Point]
  Line* = tuple[a: Point, b: Point]

proc splitdir(s : string) : tuple[dir: string, len: int] =
  var dir : string = "" & s[0]
  var len1 = s[1 .. s.high]
  var len2 : int
  let x = parseInt(len1, len2, 0)
  return (dir, len2)

proc splitit(s: string) : seq[string]  =
  return s.split(',')

proc paths(zero: tuple[x: int, y: int], s: string) : tuple[h: seq[Line], v: seq[Line]] =
  var rv : tuple[ h: seq[Line], v: seq[Line] ]
  var sp = splitit(s)
  var lastStop = zero
  for sx in sp:
    var d = splitdir(sx)
    #echo d
    var stop : Point
    var line: Line
    if d[0] == "R":
      stop = (lastStop.x + d[1], lastStop.y)
      line = (a: lastStop, b:stop)
      rv.h.add(line)
    if d[0] == "L":
      stop = (lastStop.x - d[1], lastStop.y)
      line = (a: lastStop, b:stop)
      rv.h.add(line)
    if d[0] == "U":
      stop = (lastStop.x , lastStop.y + d[1])
      line = (a: lastStop, b:stop)
      rv.v.add(line)
    if d[0] == "D":
      stop = (lastStop.x , lastStop.y - d[1])
      line = (a: lastStop, b:stop)
      rv.v.add(line)
    lastStop = stop
    #echo stop
  echo "h ", rv.h
  echo "v ", rv.v
  return rv

#proc crossed

proc manhattan(a: Point, b: Point) : int =
  var q = a.x - b.x
  var w = a.y - b.y
  if q < 0:
    q = -1 * q
  if w < 0:
    w = -1 * w

  return q + w

proc runit =
  let f = open("3input")
  defer: f.close()

  let line1 = f.readLine()
  echo line1
  let line2 = f.readLine()
  echo line2

  let zero = (0,0)
  echo zero
  let p1 = paths(zero, line1)
  let p2 = paths(zero, line2)

  var manh = 0
  var tmpMan = 0
  var x : int
  var y : int
  var newp : Point
  for h in p1.h:
   for v in p2.v:
     if h.a.x <= v.a.x and h.b.x >= v.a.x and h.a.y >= v.a.y and h.a.y <= v.b.y:
       echo "match1 ", h, v
       x = v.a.x
       y = h.a.y
     if h.b.x <= v.a.x and h.a.x >= v.a.x and h.b.y >= v.a.y and h.b.y <= v.b.y:
       echo "match2 ", h, v
       x = v.a.x
       y = h.a.y
     if h.a.x >= v.a.x and h.b.x <= v.a.x and h.a.y <= v.a.y and h.a.y >= v.b.y:
       echo "match3 ", h, v
       x = v.a.x
       y = h.a.y
     if h.b.x >= v.a.x and h.a.x <= v.a.x and h.b.y <= v.a.y and h.b.y >= v.b.y:
       echo "match4 ", h, v
       x = v.a.x
       y = h.a.y
     echo x," ",y
     if x != 0 and y != 0:
       newP = (x, y)
       tmpMan = manhattan(zero, newP)
       echo tmpMan
       if tmpMan > 0 and (tmpMan < manh or manh == 0):
         manh = tmpMan
         tmpMan = 0
  echo "manh: ", manh

runit()
