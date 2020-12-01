#!/usr/bin/env bash

INPUT=../input/day01/input.txt

cat $INPUT | while read a; do cat $INPUT | while read b; do x=$((a+b)); if [[ "$x" == "2020" ]]; then echo "$a $b $x $((a*b))"; fi; done; done

cat $INPUT | while read a; do cat $INPUT | while read b; do cat $INPUT | while read c; do x=$((a+b+c)); if [[ "$x" == "2020" ]]; then echo "$a $b $c $x $((a*b*c))"; fi; done; done; done
