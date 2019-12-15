#!/usr/bin/env bash

function dline {
	local line=$1
	local comm=$2
	local laststop=${line[0]}
	local stop=${line[1]}
	local cost=${line[2]}
	echo " DD line $comm"
	echo " DD len  : ${#line[@]}"
	echo " DD lstop: ${laststop[*]}"
	echo " DD stop : ${stop[*]}"
	echo " DD cost : ${cost}"
}

function dp {
	local x1=$1
	local y1=$2
	local x2=$3
	local y2=$4
	local c1=$5
	echo "Line ($x1/$y1) - ($x2/$y2)[$c1]"
}

function paths2 () {
	local x=$1
	local y=$2
	local sx=$3
	local dir=${sx:0:1}
	local len=${sx:1}
	let "len = $len + 0"

	if [ "$dir" == "R" ];then
		let "x = $x + $len"
	elif [ "$dir" == "L" ];then
		let "x = $x - $len"
	elif [ "$dir" == "U" ];then
		let "y = $y + $len"
	elif [ "$dir" == "D" ];then
		#echo l
		let "y = $y - $len"
	else
	  echo "ERROR $x $y $dir $len"
	fi
	rv_dir=$dir
	rv_len=$len
	rv_x=$x
	rv_y=$y
}

function manhattan () {
	local r=("$@")
	local a=(${r[0]} ${r[1]})
	local b=(${r[2]} ${r[3]})
	local q=0
	local w=0
	let "q = ${a[0]} - ${b[0]}"
	let "w = ${a[1]} - ${b[1]}"
	if [ "$q" -lt 0 ]; then
		let "q = -1 * $q"
	fi
	if [ "$w" -lt 0 ]; then
		let "w = -1 * $w"
	fi
	let "rv = $q + $w"

	rv_manhattan=$rv
}

function cnt2 () {
	local zerox=$1
	local zeroy=$2
	shift 3
	local arr=("$@")
	local singlesize=0
	let "singlesize = ${#arr[@]} / 2"
	local singlesizefoo=0
	let "singlesizefoo = $singlesize + 1"
	local linesize=0
	echo "Z $zerox $zeroy ${#arr[@]} => ${singlesize}"
	local i=0
	local nha=()
	local nva=()
	for ob in "${arr[@]}"; do
		let "i = $i + 1"
		#echo "le ${ob[@]} @ ${i}"
		if [ $i -lt $singlesizefoo ]; then
			nha+=($ob)
		else
			nva+=($ob)
		fi
	done
	#echo "added ${#nha[@]} < to nha"
	#echo "added ${#nva[@]} < to nva"
	echo '----------------------------------'

	local x=0
	local y=0
	local cost=0
	local manh=0
	local t1=0
	local t2=0

	local hax=${nha[0]}
	local hay=${nha[1]}
	local hbx=${nha[2]}
	local hby=${nha[3]}
	echo "hax.."
	echo ${hax}
	echo ${hay}
	echo ${hbx}
	echo ${hby}
	local vax=${nva[0]}
	local vay=${nva[1]}
	local vbx=${nva[2]}
	local vby=${nva[3]}
	echo "vax.."
	echo ${vax}
	echo ${vay}
	echo ${vbx}
	echo ${vby}
	local min1=$((hax < hbx ? hax : hbx))
	echo "DD min1 $min1 ~ $hax $hbx // $vax"
	if [ $min1 -gt $vax ]; then
		return 1
	fi
	local max1=$((hax > hbx ? hax : hbx))
	local min12=$((vax < vbx ? vax : vbx))
	echo "DD max1 $max1 $min12 ~ $hax $hay $hbx $hby // $vax $vbx"
	if [ $max1 -lt $min12 ]; then
		return 1
	fi
	local min2=$((vay < vby ? vay : vby))
	echo "DD min2 $min2 ~ $vay $vby // $hay"
	if [ $min2 -gt $hay ]; then
		return 1
	fi
	local max2=$((vay > vby ? vay : vby))
	local min22=$((hay < hby ? hay : hby))
	echo "DD max2 $max2 $min22 ~ $vay $vby // $hay $hby"
	if [ $max2 -lt $min22 ]; then
		return 1
	fi
	x=$vax
	y=$hay
	echo "match ($hax/$hay - $hbx/$hby) // ($vax/$vay - $vbx/$vby)  - $x $y"
	if [ $hax -lt $hbx ]; then
		let "t1 = $max1 - $x"
	else
		let "t1 = $x - $min1"
	fi
	t1=${t1#-}
	if [ $vay -lt $vby ]; then
		let "t2 = $max2 - $y"
	else
		let "t2 = $y - $min2"
	fi
	t2=${t2#-}
	echo "t1 = $t1"
	echo "t2 = $t2"
	let "cost = ${nha[4]} + ${nva[4]} - $t1 - $t2"
	local mhargs=($zerox $zeroy $x $y)
	rv_mahattan=0
	manhattan ${mhargs[@]}
	local manh=$?

	rv_manh=$rv_manhattan
	rv_cost=$cost

	return 0
}

function main () {
	local FN=""
	local L1=""
	local L2=""
	local total_manh=0
	local total_cost=0
	local ZEROX=0
	local ZEROY=0
	local mc=()
	if [ ! -z "$1" ]; then
		FN="$1"
	fi
	#echo $FN
	L1=$(cat $FN | head -n1)
	L2=$(cat $FN | head -n2 | tail -n1)
	echo $L1
	#echo $L2

	# paths L1
	local sp1=$(echo $L1 | sed 's/,/\n/g')
	# paths L1
	local sp2=$(echo $L2 | sed 's/,/\n/g')
	# init p1
	local lastx1=0
	local lasty1=0
	local cost1=0
	# init p2h
	local lastx2h=0
	local lasty2h=0
	local cost2h=0
	# init p2v
	local lastx2v=0
	local lasty2v=0
	local cost2v=0

	local sx1=''
	local sx2=''
	for sx1 in $sp1; do
		rv_dir=''
		rv_len=0
		rv_x=0
		rv_y=0
		paths2 $lastx1 $lasty1 $sx1
		local tmp1=($rv_dir $rv_len $rv_x $rv_y)
		echo "    TMP1 $rv_dir , $rv_len , $rv_x , $rv_y :: ${#tmp1[@]} :: ${tmp1[@]}"
		let "cost1 = $cost1 + ${tmp1[1]}"
		local line1=($lastx1 $lasty1 ${tmp1[2]} ${tmp1[3]} $cost1)

		lastx2h=0
		lasty2h=0
		cost2h=0
		lastx2v=0
		lasty2v=0
		cost2v=0
		if [ "${tmp1[0]}" == "R" -o ${tmp1[0]} == "L" ]; then
			for sx2 in $sp2; do
				rv_dir=''
				rv_len=0
				rv_x=0
				rv_y=0
				paths2 $lastx2h $lasty2h $sx2
				local tmp2=($rv_dir $rv_len $rv_x $rv_y)
				echo "    TMP2 $rv_dir , $rv_len , $rv_x , $rv_y :: ${#tmp2[@]} :: ${tmp2[@]}"
				let "cost2h = $cost2h + ${tmp2[1]}"
				local line2=($lastx2h $lasty2h ${tmp2[2]} ${tmp2[3]} $cost2h)
				# ignore horizontal in inner loop
				if [ "${tmp2[0]}" == "U" -o ${tmp2[0]} == "D" ]; then
			        echo "P1 - horizontal"
					echo "P2 - vertical"
					dp ${line1[@]}
					dp ${line2[@]}
					local carg=("$ZEROX" "$ZEROY" "#" "${line1[@]}" "${line2[@]}")
					echo "LEN CARG ${#carg[@]} ${#line1[@]} ${#line2[@]}"
					echo "CARG ${carg[@]}"

					rv_manh=0
					rv_cost=0
					cnt2 ${carg[@]}
					echo "xman  $rv_manh"
					echo "xcost $rv_cost"
					if [ $rv_manh -gt 0 ]; then
						if [ $rv_manh -lt $total_manh -o $total_manh -eq 0 ]; then
							total_manh=$rv_manh
						fi
					fi
					if [ $rv_cost -gt 0 ]; then
						if [ $rv_cost -lt $total_cost -o $total_cost -eq 0 ]; then
							total_cost=$rv_cost
						fi
					fi
				fi

				lastx2h=${tmp2[2]}
				lasty2h=${tmp2[3]}
			done
		else
			for sx2 in $sp2; do
				rv_dir=''
				rv_len=0
				rv_x=0
				rv_y=0
				paths2 $lastx2v $lasty2v $sx2
				local tmp2=($rv_dir $rv_len $rv_x $rv_y)
				echo "    TMP2 $rv_dir , $rv_len , $rv_x , $rv_y :: ${#tmp2[@]} :: ${tmp2[@]}"
				let "cost2v = $cost2v + ${tmp2[1]}"
				local line2=($lastx2v $lasty2v ${tmp2[2]} ${tmp2[3]} $cost2v)
				# ignore horizontal in inner loop
				if [ "${tmp2[0]}" == "R" -o ${tmp2[0]} == "L" ]; then
			        echo "P1 - vertical"
					echo "P2 - horizontal"
				    dp ${line1[@]}
				    dp ${line2[@]}
					local carg=("$ZEROX" "$ZEROY" "#" "${line2[@]}" "${line1[@]}")
					echo "LEN CARG ${#carg[@]} ${#line2[@]} ${#line1[@]}"
					echo "CARG ${carg[@]}"

					rv_manh=0
					rv_cost=0
					cnt2 ${carg[@]}
					echo "xman  $rv_manh"
					echo "xcost $rv_cost"
					if [ $rv_manh -gt 0 ]; then
						if [ $rv_manh -lt $total_manh -o $total_manh -eq 0 ]; then
							total_manh=$rv_manh
						fi
					fi
					if [ $rv_cost -gt 0 ]; then
						if [ $rv_cost -lt $total_cost -o $total_cost -eq 0 ]; then
							total_cost=$rv_cost
						fi
					fi
				fi

				lastx2v=${tmp2[2]}
				lasty2v=${tmp2[3]}
			done
		fi
		lastx1=${tmp1[2]}
		lasty1=${tmp1[3]}
	done

	echo "TOTAL M $total_manh"
	echo "TOTAL C $total_cost"

	return

	for h in ${hv[@]}; do
		for v in ${vv2[@]}; do
			cnt $ZERO $h $v
			mc=$?
			if [ ${mc[0]} -gt 0 ]; then
				if [ ${mc[0]} -lt $manh -o $manh -eq 0 ]; then
					manh=${mc[0]}
					echo $mc
				fi
			fi
			if [ ${mc[1]} -gt 0 ]; then
				if [ ${mc[1]} -lt $cost -o $cost -eq 0 ]; then
					cost=${mc[1]}
					echo $cost
				fi
			fi
		done
	done
	for h in ${hv2[@]}; do
		for v in ${vv[@]}; do
			cnt $ZERO $h $v
			mc=$?
			if [ ${mc[0]} -gt 0 ]; then
				if [ ${mc[0]} -lt $manh -o $manh -eq 0 ]; then
					manh=${mc[0]}
					echo $mc
				fi
			fi
			if [ ${mc[1]} -gt 0 ]; then
				if [ ${mc[1]} -lt $cost -o $cost -eq 0 ]; then
					cost=${mc[1]}
					echo $cost
				fi
			fi
		done
	done

	echo "manh: $manh"
	echo "cost: $cost"
}


	### test manhattan
	# a=(5 11)
	# b=(3 7)
	# #echo ${a[@]}
	# #echo ${b[@]}
	# ab=("${a[@]}" "${b[@]}")
	# echo ${ab[@]}
	# echo ${#ab[@]}
	# manhattan ${ab[@]}
	# echo "m: $?"
	# ab=("${b[@]}" "${a[@]}")
	# manhattan ${ab[@]}
	# echo "m: $?"

main $1
