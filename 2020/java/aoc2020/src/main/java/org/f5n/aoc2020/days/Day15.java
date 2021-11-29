package org.f5n.aoc2020.days;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.f5n.aoc2020.utils.Day;
import org.f5n.aoc2020.utils.Input;
import org.f5n.aoc2020.utils.IntResult;
import org.f5n.aoc2020.utils.Result;
import org.f5n.aoc2020.utils.Utils;

public class Day15 extends Day {
	protected List<Integer> input;

	public Day15(List<Integer> input) {
		this.input = input;
		this.input.add(0, 0);
	}

	private int run (int limit) {
		int i = 1;
		int cur = 0;
		int last = 0;
		Map<Integer, ArrayList<Integer>> r = new HashMap<Integer, ArrayList<Integer>>();
		while (i <= limit) {
			if (i < input.size()) {
				last = input.get(i);
				ArrayList<Integer> li = new ArrayList<Integer>();
				li.add(i);
				r.put(last, li);
				++i;
				continue;
			}
			if (r.containsKey(last)) {
				if (r.get(last).size() == 1) {
					cur = 0;
					r.get(cur).add(i);
				} else {
					int len = r.get(last).size();
					cur = r.get(last).get(len-1) - r.get(last).get(len-2);
					if (!r.containsKey(cur)) {
						r.put(cur, new ArrayList<Integer>());
					}
					r.get(cur).add(i);
					while (r.get(cur).size() > 2) {
						r.get(cur).remove(0);
					}
				}
			}
			last = cur;
			++i;
		}

		return cur;
	}

	protected Result part1(Input limit) {
		int cur = run(limit.getIntValue());
		return new IntResult(cur);
	}

	protected Result part2(Input limit) {
		int cur = run(limit.getIntValue());
		return new IntResult(cur);
	}
}