package org.f5n.aoc2020;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import org.f5n.aoc2020.utils.*;
import org.f5n.aoc2020.days.*;

@RestController
public class DayController {

	@RequestMapping("/day/1")
	public List<IntResult> day01(@RequestParam(name = "part", defaultValue = "0") int part) {
		ArrayList<Integer> inputs = Utils.getLinesAsInt("01");
		Day01 day = new Day01(inputs);
		IntInput in = new IntInput(2020);

		List<IntResult> rv = new ArrayList<>();
		IntResult ir1;
		IntResult ir2;
		if (part != 2) {
		 	ir1 = (IntResult) day.runPart1(in);
			rv.add(ir1);
		}
		if (part != 1) {
		 	ir2 = (IntResult) day.runPart2(in);
			rv.add(ir2);
		}

		return rv;
	}

	@RequestMapping("/day/2")
	public List<IntResult> day02(@RequestParam(name = "part", defaultValue = "0") int part) {
		ArrayList<String> inputs = Utils.getLinesAsString("02");
		Day02 day = new Day02(inputs);
		IntInput in = new IntInput(0);

		List<IntResult> rv = new ArrayList<>();
		IntResult ir1;
		IntResult ir2;
		if (part != 2) {
		 	ir1 = (IntResult) day.runPart1(in);
			rv.add(ir1);
		}
		if (part != 1) {
		 	ir2 = (IntResult) day.runPart2(in);
			rv.add(ir2);
		}

		return rv;
	}

	@RequestMapping("/day/3")
	public List<IntResult> day03(@RequestParam(name = "part", defaultValue = "0") int part) {
		ArrayList<String> inputs = Utils.getLinesAsString("03");
		Day03 day = new Day03(inputs);
		IntInput in = new IntInput(0);

		List<IntResult> rv = new ArrayList<>();
		IntResult ir1;
		IntResult ir2;
		if (part != 2) {
		 	ir1 = (IntResult) day.runPart1(in);
			rv.add(ir1);
		}
		if (part != 1) {
		 	ir2 = (IntResult) day.runPart2(in);
			rv.add(ir2);
		}

		return rv;
	}

	@RequestMapping("/day/15")
	public List<IntResult> day15(@RequestParam(name = "part", defaultValue = "0") int part) {
		List<String> inputs = Utils.getLinesAsString("15");
		List<Integer> inputs2 = Utils.getLineAsInts(inputs);
		
		Day day = new Day15(inputs2);
		IntInput in;

		List<IntResult> rv = new ArrayList<>();
		IntResult ir1;
		IntResult ir2;
		if (part != 2) {
			in = new IntInput(2020);
		 	ir1 = (IntResult) day.runPart1(in);
			rv.add(ir1);
		}
		if (part != 1) {
			in = new IntInput(30000000);
		 	ir2 = (IntResult) day.runPart2(in);
			rv.add(ir2);
		}

		return rv;
	}
}
