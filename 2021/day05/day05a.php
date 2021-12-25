<?php
function pp(array $floor) {
    foreach ($floor as $y => $lx) {
        foreach ($lx as $x => $xx) {
            printf("%s ", $floor[$y][$x] > 0 ? $floor[$y][$x] : '.');
        }
        printf("\n");
    }
    printf("\n");
}

function run($filename) : array {
    $time = [];
    $time[] = [microtime(true), 0, 'start'];
    $data = trim(file_get_contents($filename));
    $parts = explode("\n", $data);
    $sizex = 10;
    $sizey = 10;
    $time[] = [$tt = microtime(true), $tt - end($time)[0], 'read'];

    $p2x = [];
    $p2y = [];
    $p2d = [];
    foreach ($parts as $part) {
        [$ls, $rs] = explode(' -> ', $part,2);
        $ls = explode(',', $ls, 2);
        $ls = array_map('intval', $ls);
        $rs = explode(',', $rs, 2);
        $rs = array_map('intval', $rs);
        if ($ls[0] > $sizex) {
            $sizex = $ls[0];
        }
        if ($rs[0] > $sizex) {
            $sizex = $rs[0];
        }
        if ($ls[1] > $sizey) {
            $sizey = $ls[1];
        }
        if ($rs[1] > $sizey) {
            $sizey = $rs[1];
        }
        if ($ls[0] == $rs[0]) {
            $p2x[] = [$ls, $rs];
        } elseif ($ls[1] == $rs[1]) {
            $p2y[] = [$ls, $rs];
        } else {
            $p2d[] = [$ls, $rs];
        }
    }
    $sizex++;
    $sizey++;
    $time[] = [$tt = microtime(true), $tt - end($time)[0], 'points'];

    $linex = [];
    $liney = [];
    foreach ($p2x as $p) {
        #printf("(%s %s) (%s %s)\n", $p[0][0], $p[0][1], $p[1][0], $p[1][1]);
        [$s, $e] = $p[0][1] < $p[1][1] ? [0,1] : [1,0];
        $line = [];
        for ($i=$p[$s][1];$i<=$p[$e][1];$i++) {
            $line[] = [$p[0][0], $i];
        }
        $linex[] = $line;
    }
    foreach ($p2y as $p) {
        #printf("(%s %s) (%s %s)\n", $p[0][0], $p[0][1], $p[1][0], $p[1][1]);
        [$s, $e] = $p[0][0] < $p[1][0] ? [0,1] : [1,0];
        $line = [];
        for ($i=$p[$s][0];$i<=$p[$e][0];$i++) {
            $line[] = [$i, $p[0][1]];
        }
        $liney[] = $line;
    }
    $time[] = [$tt = microtime(true), $tt - end($time)[0], 'lines'];

    $floor = [];
    for ($y=0;$y<$sizey;$y++) {
        $row = [];
        for ($x=0;$x<$sizex;$x++) {
            $row[] = 0;
        }
        $floor[] = $row;
    }
    $time[] = [$tt = microtime(true), $tt - end($time)[0], 'board'];

    $cross1 = 0;
    foreach ($linex as $lx) {
        foreach ($lx as $x) {
            $floor[$x[1]][$x[0]]++;
            if ($floor[$x[1]][$x[0]] == 2) {
                $cross1++;
            }
        }
    }
    foreach ($liney as $lx) {
        foreach ($lx as $x) {
            $floor[$x[1]][$x[0]]++;
            if ($floor[$x[1]][$x[0]] == 2) {
                $cross1++;
            }
        }
    }

    #pp($floor);
    $time[] = [$tt = microtime(true), $tt - end($time)[0], 'cross1'];
    $cross2 = 0;
    $floor2 = [];
    for ($y=0;$y<$sizey;$y++) {
        $row = [];
        for ($x=0;$x<$sizex;$x++) {
            $row[] = 0;
        }
        $floor2[] = $row;
    }
    $lined = [];

    foreach ($p2d as $p) {
        $p1 = $p[0];
        $p2 = $p[1];
        #printf("(%s %s) (%s %s)\n", $p1[0], $p1[1], $p2[0], $p2[1]);
        $stops = [$p1];
        while ($p1[0] != $p2[0] && $p1[1] != $p2[1]) {
            if ($p2[0] > $p1[0]) {
                $p1[0]++;
            } else {
                $p1[0]--;
            }
            if ($p2[1] > $p1[1]) {
                $p1[1]++;
            } else {
                $p1[1]--;
            }
            $stops[] = $p1;
        }
        $lined[] = $stops;
    }

    foreach ($linex as $lx) {
        foreach ($lx as $x) {
            $floor2[$x[1]][$x[0]]++;
            if ($floor2[$x[1]][$x[0]] == 2) {
                $cross2++;
            }
        }
    }
    foreach ($liney as $lx) {
        foreach ($lx as $x) {
            $floor2[$x[1]][$x[0]]++;
            if ($floor2[$x[1]][$x[0]] == 2) {
                $cross2++;
            }
        }
    }
    foreach ($lined as $lx) {
        foreach ($lx as $x) {
            $floor2[$x[1]][$x[0]]++;
            if ($floor2[$x[1]][$x[0]] == 2) {
                $cross2++;
            }
        }
    }
    #pp($floor2);
    $time[] = [$tt = microtime(true), $tt - end($time)[0], 'cross2'];

    return [$cross1, $cross2, $time];
}

$d = function($x) {
    printf("  %s %s\n", str_pad($x[2], 7), $x[1]);
};
$r = run("/aoc/in.txt");
printf("%d - %d\n", $r[0], $r[1]);
array_map($d, $r[2]);
$r = run("/aoc/input.txt");
printf("%d - %d\n", $r[0], $r[1]);
array_map($d, $r[2]);
//printf("       %s\n", ($r[2]['cross1'][0] - $r[2]['start'][0]));
var_dump(opcache_get_status()['jit']);