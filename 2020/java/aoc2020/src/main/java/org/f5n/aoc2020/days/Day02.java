package org.f5n.aoc2020.days;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.f5n.aoc2020.utils.*;


public class Day02 extends Day {
	protected List<String> input;
	protected int valid = 0;

	public Day02(List<String> input) {
		this.input = input;
	}

	protected Result part1(Input limit) {
		valid = 0;
		run(1);
		return new IntResult(valid);
	}

	protected Result part2(Input limit) {
		valid = 0;
		run(2);
		return new IntResult(valid);
	}

	private void run(int part) {
		for (String s : input) {
			String[] parts = s.split(":");
			String passw = parts[1].strip();
			parts = parts[0].split(" ");
			char match = parts[1].charAt(0);
			parts = parts[0].split("-");
			int n1 = Integer.parseInt(parts[0]);
			int n2 = Integer.parseInt(parts[1]);

			if (part == 1) {
				calc1(passw, match, n1, n2);
			} else {
				calc2(passw, match, n1, n2);
			}
		}
	}

	private void calc1(String passw, char match, int n1, int n2) {
		int vc = 0;
		for (int i = 0; i<passw.length(); ++i) {
			if (passw.charAt(i) == match) {
				++vc;
			}
		}
		if (vc >= n1 && vc <= n2) {
			++valid;
		}
	}

	private void calc2(String passw, char match, int n1, int n2) {
		if ((passw.charAt(n1-1) == match && !(passw.charAt(n2-1) == match)) ||
				(!(passw.charAt(n1-1) == match) && passw.charAt(n2-1) == match)) {
			++valid;
		}
	}
}