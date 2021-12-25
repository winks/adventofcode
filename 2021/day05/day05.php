<?php

    $time = [];
    $time[] = hrtime(true);
$data = trim(file_get_contents("/aoc/in.txt"));
$parts = explode("\n", $data);
    $time[] = hrtime(true);

/*
// $cb1 = function(string $k) : array {
//    $r = => explode(',', $k);
//};
$cb_f = fn(array $a) : array => (($a[0] == $a[1]));
$cb_f2 = function(array $a) : array {
    var_dump($a);
    return true;
};
$cb_xy = fn(string $k) : array => explode(',', $k, 2);
$cb_line = function(string $k) use ($cb_f, $cb_xy, $cb_f2) : array {
    $r = explode(' -> ', $k, 2);
    var_dump($r);
    //$r = array_map('intval', array_map($cb_xy, $r));
    $r = array_map($cb_xy, $r);
    var_dump($r);
    //$r = array_filter($r, $cb_f2, ARRAY_FILTER_USE_BOTH);
    $r2 = [];
    foreach ($r as $a) {
        var_dump($a)
        if ($a[0][0] == $a[1][0] || $a[0][1] == $a[1][1]) {
            $r[] = $a;
        }
    }
    var_dump($r2);
    return $r2;
};
$parts = array_map($cb_line, [$parts[0]]);
*/
$p2x = [];
$p2y = [];
foreach ($parts as $part) {
    [$ls, $rs] = explode(' -> ', $part,2);
    $ls = explode(',', $ls, 2);
    $rs = explode(',', $rs, 2);
    if ($ls[0] == $rs[0]) {
        $p2x[] = [$ls, $rs];
    } elseif ($ls[1] == $rs[1]) {
        $p2y[] = [$ls, $rs];
    }
    //var_dump($ls, $rs);
}
    $time[] = hrtime(true);

#print_r($p2x);
#print_r($p2y);

$linex = [];
$liney = [];
foreach ($p2x as $p) {
    [$s, $e] = $p[0][1] < $p[1][1] ? [0,1] : [1,0];
    #print_r($p);
    #var_dump($s, $e);
    $line = [];
    for ($i=$p[$s][1];$i<=$p[$e][1];$i++) {
        $line[] = [intval($p[0][0]), intval($i)];
    }
    $linex[] = $line;
}
foreach ($p2y as $p) {
    [$s, $e] = $p[0][0] < $p[1][0] ? [0,1] : [1,0];
    #print_r($p);
    #var_dump($s, $e);
    $line = [];
    for ($i=$p[$s][0];$i<=$p[$e][0];$i++) {
        $line[] = [intval($i), intval($p[0][1])];
    }
    $liney[] = $line;
}
print_r("===========\n");
foreach ($linex as $lx) {
    foreach ($lx as $x) {
        printf("(%d,%d)", $x[0], $x[1]);
    }
    printf("\n");
}
foreach ($liney as $lx) {
    foreach ($lx as $x) {
        printf("(%d,%d)", $x[0], $x[1]);
    }
    printf("\n");
}
print_r("===========\n");

$combo = $linex;
#array_push($combo, ...$liney);
$found = [];
foreach ($linex as $lx) {
    foreach ($lx as $x) {
        foreach ($liney as $ly) {
            foreach ($ly as $y) {
                if ($x[0] == 9) {
                    #printf("(%d,%d) (%d,%d)\n", $x[0], $x[1], $y[0], $y[1]);
                }
                if ($x[0] == $y[0] && $x[1] == $y[1]) {
                    $k = sprintf("%d,%d", $x[0], $x[1]);
                    if (!array_key_exists($k, $found)) {
                        $found[$k] = 0;
                    }
                    $found[$k]++;
                    #printf("(%d,%d) (%d,%d)\n", $x[0], $x[1], $y[0], $y[1]);
                }
            }
        }
    }
}
$cross = 0;
#var_dump($found);
printf("P1: %s\n", array_sum($found) - count($found));