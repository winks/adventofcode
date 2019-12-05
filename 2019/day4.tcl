#!/usr/bin/tclsh

proc check1 {num} {
  if { $num < 100000 } {
    return 0
  }
  if { $num > 999999 } {
    return 0
  }
  set s [format "%d" $num]
  #puts $s
  set ok 0
  set len [string length $s]
  for { set i 0 } { $i < [string length $s] } { incr i } {
    #puts [format "# ok %d i %d len %d" $ok $i $len]
    if { $i < 1 } {
      continue
    }
    set i2 [expr $i - 1]
    #puts [format "# idx i:%d = %d idx i-1:%d = %d" $i [string index $s $i] $i2 [string index $s $i2] ]
    if { [string index $s $i] < [string index $s $i2] } {
      return 0
    }
    if { [string index $s $i] == [string index $s $i2] } {
      set ok [expr $ok + 1]
    }
  }
  #puts [format "## ok %d i %d len %d" $ok $i $len]
  if { $ok > 0 } {
    return 1
  }
  return 0
}

proc run1 {name} {
  set fp [open $name r]
  set i 0
  
  while { [gets $fp data] >= 0 } {
    #puts $i
    #puts $data
    set numbers($i) $data
    set i [expr $i + 1]
    #puts $i
  }
  close $fp
  
  set len [array size numbers]
  puts [format "Read %d" $len]
  
  set first $numbers(0)
  set last $numbers(1)
  
  set good 0
  
  for { set i $first }  { $i <= $last } { incr i } {
    if { [check1 $i] > 0 } {
      #puts [format "%d" $i]
      set good [expr $good + 1]
    } else {
      #puts [format "## NO %d" $i]
    }
  }
  
  puts [format "Good %d" $good]
}

run1 "4input"

