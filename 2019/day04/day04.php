<?php
function equalize($num) {
	$str = sprintf("%d", $num);
	for ($i=0;$i<strlen($str);++$i) {
		if ($i == 0) continue;
		$cur  = intval(substr($str, $i, 1));
		$last = intval(substr($str, $i-1, 1));
		if ($cur < $last) {
			$str = sprintf("%s%s", substr($str, 0, $i), str_repeat($last, strlen($str)-$i));
			return intval($str);
		}
	}
	return intval($str);
}

function check1($num) {
	if ($num < 100000 || $num > 999999) {
		return false;
	}

	$s = sprintf("%d", $num);
	$ok = 0;

	for ($i=0;$i<strlen($s);++$i) {
		if ($i<1) {
			continue;
		}
		if (intval($s[$i]) <  intval($s[$i-1])) return false;
		if (intval($s[$i]) == intval($s[$i-1])) ++$ok;
	}
	if ($ok > 0) return true;
	return false;
}

function check2($num) {
	if ($num < 100000 || $num > 999999) {
		return false;
	}

	$s = sprintf("%d", $num);
	$ok = 0;
	$last = " ";
	$cnt = 1;

	for ($i=0;$i<strlen($s);++$i) {
		$cur = $s[$i];
		if ($cur == $last) {
			++$cnt;
		} else {
			$cnt = 1;
		}

		if ($i<1) {
			$last = $cur;
			continue;
		}

		if ($cnt == 2) {
			if ($i < strlen($s)-1 && $s[$i+1] !== $cur) {
				$ok++;
			} else if ($i == strlen($s)-1) {
				$ok++;
			}
			$last = $cur;
			continue;
		} else {
			$last = $cur;
			continue;
		}

		if ($i == strlen($s)-1) return (($ok > 0) && $cnt <= 2);
	}
	if ($ok > 0) return true;
	return false;
}

function f1($a, $b) {
	$ax     = $a;
	$bx     = $b;
	$i      = 0;
	$cnt    = 0;
	$lastok = 0;

	while ($a <= $b) {
		$rv = check1($a);
		if ($rv && $a > $lastok) {
            ++$cnt;
			$lastok = $a;
			++$a;
		} else {
			$a2 = equalize($a);
			if ($a2 > $b) break;
			$rv = check1($a2);
			if ($rv && $a2 > $lastok) {
				$cnt++;
				$lastok = $a2;
			}
			$a = $a2 + 1;
		}
		++$i;
	}
	printf("max   : %d\n", ($bx-$ax));
	printf("i     : %s\n", $i);
	printf("result: %s\n", $cnt);
}

function f2($a, $b) {
	$ax     = $a;
	$bx     = $b;
	$i      = 0;
	$cnt    = 0;
	$lastok = 0;

	while ($a <= $b) {
		$a2 = equalize($a);
		if ($a2 > $b) break;
		$rv = check2($a2);
		if ($rv && $a2 > $lastok) {
			$cnt++;
			$lastok = $a2;
		}
		$a = $a2 + 1;
		++$i;
	}
	printf("max   : %d\n", ($bx-$ax));
	printf("i     : %s\n", $i);
	printf("result: %s\n", $cnt);
}

if (count($argv) < 2) {
	echo sprintf("Usage: %s /path/to/file", $argv[0]) . PHP_EOL;
	exit();
} else {
	$fname = $argv[1];
}

$fh = fopen($fname, "r");
while (!feof($fh)) {
	$result = fgets($fh);
	if (strpos($result, '-') !== false) break;
}
$parts = array_map('intval', explode('-', $result));

f1($parts[0], $parts[1]);
f2($parts[0], $parts[1]);
