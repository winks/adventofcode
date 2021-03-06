# Nim 1.0.4

import os
import strutils

type
  Point* = tuple[x:int, y:int]
  PointList* = seq[Point]
  Line* = tuple[a: Point, b: Point, cost: int]

proc splitdir(s : string) : tuple[dir: string, len: int] =
  var dir : string = "" & s[0]
  var len1 = s[1 .. s.high]
  var len2 : int = parseInt(len1)
  return (dir, len2)

proc splitit(s: string) : seq[string]  =
  return s.split(',')

proc paths(zero: tuple[x: int, y: int], s: string) : tuple[h: seq[Line], v: seq[Line]] =
  var rv : tuple[ h: seq[Line], v: seq[Line] ]
  var sp = splitit(s)
  var lastStop = zero
  var cost = 0
  for sx in sp:
    var d = splitdir(sx)
    var stop : Point
    var line: Line
    cost += d[1]
    if d[0] == "R":
      stop = (lastStop.x + d[1], lastStop.y)
      line = (a: lastStop, b:stop, cost: cost)
      rv.h.add(line)
    if d[0] == "L":
      stop = (lastStop.x - d[1], lastStop.y)
      line = (a: lastStop, b:stop, cost: cost)
      rv.h.add(line)
    if d[0] == "U":
      stop = (lastStop.x , lastStop.y + d[1])
      line = (a: lastStop, b:stop, cost: cost)
      rv.v.add(line)
    if d[0] == "D":
      stop = (lastStop.x , lastStop.y - d[1])
      line = (a: lastStop, b:stop, cost: cost)
      rv.v.add(line)
    lastStop = stop
    #echo stop
  echo "h ", rv.h
  echo "v ", rv.v
  return rv

proc manhattan(a: Point, b: Point) : int =
  var q = a.x - b.x
  var w = a.y - b.y
  if q < 0:
    q = -1 * q
  if w < 0:
    w = -1 * w
  return q + w

proc cnt(zero: Point, h: Line, v: Line) : tuple[m: int, c: int] =
  var x : int
  var y : int
  var cost = 0
  var manh = 0
  if min(h.a.x, h.b.x) <= v.a.x and max(h.a.x, h.b.x) >= v.a.x and min(v.a.y, v.b.y) <= h.a.y and max(v.a.y, v.b.y) >= h.a.y:
    x = v.a.x
    y = h.a.y
    echo "match ", h, v, " ", x, " ", y
    var t1 : int
    var t2 : int

    if h.a.x < h.b.x:
      t1 = abs( max(h.a.x, h.b.x) - x)
    else:
      t1 = abs( x - min(h.a.x, h.b.x) )
    if v.a.y < v.b.y:
      t2 = abs( max(v.a.y, v.b.y) - y )
    else:
      t2 = abs( y - min(v.a.y, v.b.y) )

    #echo "#t1 ", t1
    #echo "#t2 ", t2
    cost = h.cost + v.cost - t1 - t2
    manh = manhattan(zero, (x, y))
    #echo "#tC ", cost
    #echo "#tm ", manh
  return (manh, cost)

proc runit =
  let args = commandLineParams()
  if len(args) < 1:
    let app = getAppFilename()
    echo "Usage: ", app, " /path/to/file"
    return
  let filename = args[0].string
  let f = open(filename)
  defer: f.close()

  let line1 = f.readLine()
  echo line1
  let line2 = f.readLine()
  echo line2

  let zero = (0,0)
  let p1 = paths(zero, line1)
  let p2 = paths(zero, line2)

  var manh = 0
  var cost = 0

  for h in p1.h:
   for v in p2.v:
     let mc = cnt(zero, h, v)
     if mc.m > 0 and (mc.m < manh or manh == 0):
       manh = mc.m
       echo mc
     if mc.c > 0 and (mc.c < cost or cost == 0):
       cost = mc.c

  for h in p2.h:
   for v in p1.v:
     let mc = cnt(zero, h, v)
     if mc.m > 0 and (mc.m < manh or manh == 0):
       manh = mc.m
       echo mc
     if mc.c > 0 and (mc.c < cost or cost == 0):
       cost = mc.c

  echo "manh: ", manh
  echo "cost: ", cost

runit()
