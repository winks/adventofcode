package org.f5n.aoc2020.utils;

abstract public class Day {
    protected long start = 0;
    
    abstract protected Result part1(Input in);
    abstract protected Result part2(Input in);

    public Result runPart1(Input in) {
        start = System.currentTimeMillis();
        Result rv = part1(in);
        rv.runtime = (System.currentTimeMillis() - start);
        return rv;
    }

    public Result runPart2(Input in) {
        start = System.currentTimeMillis();
        Result rv = part2(in);
        rv.runtime = (System.currentTimeMillis() - start);
        return rv;
    }
}