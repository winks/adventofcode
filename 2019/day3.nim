import parseUtils
import strutils

type
  Point* = tuple[x:int, y:int]
  PointList* = seq[Point]
  Line* = tuple[a: Point, b: Point, cost: int]

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
  var cost = 0
  for sx in sp:
    var d = splitdir(sx)
    #echo d
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

proc runit =
  let f = open("3input")
  defer: f.close()
  
  let line1 = f.readLine()
  echo line1
  let line2 = f.readLine()
  echo line2

  let zero = (0,0)
  #echo zero
  let p1 = paths(zero, line1)
  let p2 = paths(zero, line2)
  
  var manh = 0
  var tmpMan = 0
  var x : int
  var y : int
  var cost = 0
  var tmpCost = 0
  var newp : Point
  for h in p1.h:
   for v in p2.v:
     if min(h.a.x, h.b.x) <= v.a.x and max(h.a.x, h.b.x) >= v.a.x and min(v.a.y, v.b.y) <= h.a.y and max(v.a.y, v.b.y) >= h.a.y:
       x = v.a.x
       y = h.a.y
       echo "match1 ", h, v, " ", x, " ", y
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

       echo "#t1 ", t1
       echo "#t2 ", t2
       tmpCost = h.cost + v.cost - t1 - t2
       echo "#tC ", tmpCost
     #echo x," ",y
     if x != 0 and y != 0:
       newP = (x, y)
       tmpMan = manhattan(zero, newP)
       #echo tmpMan
       if tmpMan > 0 and (tmpMan < manh or manh == 0):
         manh = tmpMan
         tmpMan = 0
       if tmpCost > 0 and (tmpCost < cost or cost == 0):
         cost = tmpCost
  for h in p2.h:
   for v in p1.v:
     if min(h.a.x, h.b.x) <= v.a.x and max(h.a.x, h.b.x) >= v.a.x and min(v.a.y, v.b.y) <= h.a.y and max(v.a.y, v.b.y) >= h.a.y:
       x = v.a.x
       y = h.a.y
       echo "match2 ", h, v, " ", x, " ", y
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
       echo "#t1 ", t1
       echo "#t2 ", t2
       tmpCost = h.cost + v.cost - t1 - t2
       echo "#tC ", tmpCost
     #echo x," ",y
     if x != 0 and y != 0:
       newP = (x, y)
       tmpMan = manhattan(zero, newP)
       #echo tmpMan
       if tmpMan > 0 and (tmpMan < manh or manh == 0):
         manh = tmpMan
         tmpMan = 0
       if tmpCost > 0 and (tmpCost < cost or cost == 0):
         cost = tmpCost
  echo "manh: ", manh
  echo "cost: ", cost

runit()
