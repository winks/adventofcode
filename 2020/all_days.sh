#!/usr/bin/env bash

function xx {
  for i in $(seq $1 $2); do
    [ ! -f day0$i/day0$i.py ] && continue;
    cd day0$i
    echo "# day0$i"
    CMD1="python3 day0$i.py 1"
    CMD2="python3 day0$i.py 2"
    if [ "$3" == "1" ]; then
      hyperfine "$CMD1"
      hyperfine "$CMD2"
    else
      $CMD1
      $CMD2
    fi
    cd ..
  done
}

if [ "$1" == "perf" ]; then
  xx 1 9 1
  xx 10 25 1
elif [ "$1" == "run" ]; then
  xx 1 9
  xx 10 25
else
  echo "$0 perf|run"
fi
