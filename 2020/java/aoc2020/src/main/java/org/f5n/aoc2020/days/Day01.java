package org.f5n.aoc2020.days;

import java.util.List;
import java.util.HashMap;

import org.f5n.aoc2020.utils.*;


public class Day01 extends Day {
	protected List<Integer> input;

	public Day01(List<Integer> input) {
		this.input = input;
	}

	protected Result part1(Input limit) {
		HashMap<Integer, Boolean> m = new HashMap<Integer, Boolean>();
		for (Integer i: input) {
			int other = limit.getIntValue() - i;
			if (m.containsKey(other)) {
				return new IntResult(i * other);
			}
			m.put(i, true);
		}

		return new IntResult();
	}

	public Result part2(Input limit) {
		HashMap<Integer, Boolean> m = new HashMap<Integer, Boolean>();
		HashMap<Integer, Integer> n = new HashMap<Integer, Integer>();
		for (Integer i: input) {
			if (m.size() < 2) {
				m.put(i, true);
				continue;
			}
			for (int ii: m.keySet()) {
				if (i + ii >= limit.getIntValue()) {
					continue;
				}
				
				if (n.containsKey(i)) {
					return new IntResult(i * n.get(i));
				}
				int other = limit.getIntValue() - ii - i;
				n.put(other, i * ii);
			}
			m.put(i, true);
		}

		return new IntResult();
	}
}
