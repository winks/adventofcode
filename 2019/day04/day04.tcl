#!/usr/bin/tclsh
# Tcl 8.6
#
proc readfile {name} {
  set fp [open $name r]
  set i 0

  while { [gets $fp data] >= 0 } {
    set lines($i) $data
  }
  close $fp
  set numbers [split $lines(0) "-"]
  return $numbers
}

proc check1 {num} {
  set s [format "%d" $num]
  set ok 0
  # i will start at 1
  set i2 0
  for { set i 1 } { $i < 6 } { incr i } {
    set s1 [string index $s $i]
    set s2 [string index $s $i2]
    if { $s1 < $s2 } {
      return 0
    }
    if { $s1 == $s2 } {
      set ok [expr $ok + 1]
    }
    incr i2 1
  }
  if { $ok > 0 } {
    return 1
  }
  return 0
}

proc check2 {num} {
  set s [format "%d" $num]

  set ok 0
  set last " "
  set cnt 1
  set last [string index $s 0]
  for { set i 1 } { $i < 6 } { incr i } {
    set cur [string index $s $i]
    if { $cur < $last } {
      return 0
    }

    if { $cur == $last } {
      set cnt [expr $cnt + 1]
    } else {
      set cnt 1
    }

    if { $cnt == 2 } {
      if { $i < 5 && $cur != [string index $s [expr $i + 1] ] } {
        set ok [expr $ok + 1]
      } elseif { $i == 5 } {
        set ok [expr $ok + 1]
      }
      set last $cur
      continue
    } else {
      set last $cur
      continue
    }
  }
  if { $i == 5 } {
    if { $ok > 0 && $cnt <= 2 } {
      return 1
    } else {
      return 0
    }
  }
  if { $ok > 0 } {
    return 1
  }
  return 0
}

proc check1_slow {num} {
  if { $num < 100000 } {
    return 0
  }
  if { $num > 999999 } {
    return 0
  }
  set s [format "%d" $num]
  set ok 0
  set len [string length $s]
  for { set i 0 } { $i < [string length $s] } { incr i } {
    if { $i < 1 } {
      continue
    }
    set i2 [expr $i - 1]
    if { [string index $s $i] < [string index $s $i2] } {
      return 0
    }
    if { [string index $s $i] == [string index $s $i2] } {
      set ok [expr $ok + 1]
    }
  }
  if { $ok > 0 } {
    return 1
  }
  return 0
}

proc check2_slow {num} {
  if { $num < 100000 } {
    return 0
  }
  if { $num > 999999 } {
    return 0
  }
  set s [format "%d" $num]

  set ok 0
  set last " "
  set cnt 1
  set len [string length $s]
  set lenm1 [expr $len -1]
  for { set i 0 } { $i < [string length $s] } { incr i } {
    set cur [string index $s $i]

    if { $cur == $last } {
      set cnt [expr $cnt + 1]
    } else {
      set cnt 1
    }

    if { $i < 1 } {
      set last $cur
      continue
    }

    set il [expr $i - 1]
    if { [string index $s $i] < [string index $s $il] } {
      return 0
    }

    if { $cnt == 2 } {
      set i2 [expr $i + 1]
      if { $i < $lenm1 && $cur != [string index $s $i2] } {
        set ok [expr $ok + 1]
      } elseif { $i == $lenm1 } {
        set ok [expr $ok + 1]
      }
      set last $cur
      continue
    } else {
      set last $cur
      continue
    }
  }
  if { $i == $lenm1 } {
    if { $ok > 0 && $cnt <= 2 } {
      return 1
    } else {
      return 0
    }
  }
  if { $ok > 0 } {
    return 1
  }
  return 0
}

proc run1 {name } {
  set numbers [readfile $name]
  lassign $numbers first last
  set good 0

  for { set i $first }  { $i <= $last } { incr i } {
    if { [check1 $i] > 0 } {
      set good [expr $good + 1]
    }
  }

  puts [format "Part 1: %d" $good]
}

proc run2 {name } {
  set numbers [readfile $name]
  lassign $numbers first last
  set good 0

  for { set i $first }  { $i <= $last } { incr i } {
    if { [check2 $i] > 0 } {
      set good [expr $good + 1]
    }
  }

  puts [format "Part 2: %d" $good]
}

if { $argc != 1 } {
  puts "Usage: day04.tcl /path/to/file"
} else {
  run1 [lindex $argv 0]
  run2 [lindex $argv 0]
}
