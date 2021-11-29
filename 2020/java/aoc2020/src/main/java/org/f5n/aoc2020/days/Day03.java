package org.f5n.aoc2020.days;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.f5n.aoc2020.utils.*;


public class Day03 extends Day {
	protected List<String> input;
	protected char[][] mmap = new char[1][1];
	protected int sx = 0;
	protected int sy = 0;

	public Day03(List<String> input) {
		this.input = input;
	}

	protected Result part1(Input limit) {
		prep();
		long rv = slope(3, 1);
		return new IntResult(rv);
	}

	protected Result part2(Input limit) {
		prep();
		long rv = slope(1, 1) * slope(3, 1) * slope(5, 1) * slope(7, 1) * slope(1, 2);
		return new IntResult(rv);
	}

	private void prep() {
		sy = input.size();
		sx = input.get(0).length();
		mmap = new char[sy+1][sx+1];
		int i = 0;
		for (String line : input) {
			line = line.strip();
			for (int j = 0; j < sx; ++j) {
				mmap[i][j] = line.charAt(j);
			}
			++i;
		}
	}

	private long slope(int stepx, int stepy) {
		int x = 0;
		int y = 0;
		int num = 0;
		while (y < sy - 1) {
			x += stepx;
			y += stepy;
			if (x >= sx) {
				x -= sx;
			}
			if (mmap[y][x] == '#') {
				++num;
			}
		}
		return num;
	}
}