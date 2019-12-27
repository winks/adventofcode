#!/usr/bin/env bash

echo "| Day    | Language | Part | Time |"
echo "| ------ | -------- | ---- | ---: |"
find . -type f -name Makefile | sort | grep '^\./day' | while read f; do
#echo $f
	day=$(echo $(dirname $f) | sed 's,^\./day,Day ,')
	i=0
	grep "@echo \"#" $f | sed 's/.*@echo "# //' | sed 's,"$,,' | while read m; do
		if [ $i -eq 0 ]; then
			echo -n "| $day |"
		else
			echo -n "|        |"
		fi
		m1=$(echo $m | cut -d, -f1)
		m2=$(echo $m | cut -d, -f2)
		m3=$(echo $m | cut -d, -f3)
		m=$(echo $m | sed 's/[,:]/|/g')
		echo "$m |"
		let "i = i + 1"
	done
done
