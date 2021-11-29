package org.f5n.aoc2020;

import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import org.f5n.aoc2020.utils.*;
import org.f5n.aoc2020.days.*;


@RestController
public class DayController {
	protected final static Logger logger = LoggerFactory.getLogger(DayController.class);

	@RequestMapping("/day/1")
	public List<IntResult> day11(@RequestParam(name = "part", defaultValue = "0") int part) {
		String sDay = "01";
		IntInput in = new IntInput(2020);
		List<Integer> inputs = Utils.getLinesAsInt(sDay);
		List<IntResult> rv = factoryInt(sDay, inputs, in, in, part);
		return rv;
	}

	@RequestMapping("/day/2")
	public List<IntResult> day02(@RequestParam(name = "part", defaultValue = "0") int part) {
		String sDay = "02";
		Input in = new NoInput();
		List<String> inputs = Utils.getLinesAsString(sDay);
		List<IntResult> rv = factoryString(sDay, inputs, in, in, part);
		return rv;
	}

	@RequestMapping("/day/3")
	public List<IntResult> day03(@RequestParam(name = "part", defaultValue = "0") int part) {
		String sDay = "03";
		Input in = new NoInput();
		List<String> inputs = Utils.getLinesAsString(sDay);
		List<IntResult> rv = factoryString(sDay, inputs, in, in, part);
		return rv;
	}

	@RequestMapping("/day/15")
	public List<IntResult> day15(@RequestParam(name = "part", defaultValue = "0") int part) {
		String sDay = "15";
		List<String> inputs1 = Utils.getLinesAsString(sDay);
		List<Integer> inputs = Utils.getLineAsInts(inputs1);
		List<IntResult> rv = factoryInt(sDay, inputs, new IntInput(2020), new IntInput(30000000), part);
		return rv;
	}

	private static List<IntResult> factoryInt(String sDay, List<Integer> inputs, Input i1, Input i2, int part) {
		List<IntResult> rv = new ArrayList<>();
		Day day;

		try {
			Class cls = Class.forName("org.f5n.aoc2020.days.Day" + sDay);
			day = (Day) cls.getDeclaredConstructor(List.class).newInstance(inputs);
		} catch (NoSuchMethodException ex) {
			logger.warn(ex.toString());
			return rv;
		} catch (IllegalAccessException ex) {
			logger.warn(ex.toString());
			return rv;
		} catch (InvocationTargetException ex) {
			logger.warn(ex.toString());
			return rv;
		} catch (ClassNotFoundException ex) {
			logger.warn(ex.toString());
			return rv;
		} catch (InstantiationException ex) {
			logger.warn(ex.toString());
			return rv;
		}

		if (day == null) {
			return rv;
		}
		IntResult ir1;
		IntResult ir2;
		if (part != 2) {
			ir1 = (IntResult) day.runPart1(i1);
			rv.add(ir1);
		}
		if (part != 1) {
			ir2 = (IntResult) day.runPart2(i2);
			rv.add(ir2);
		}

		return rv;
	}

	private static List<IntResult> factoryString(String sDay, List<String> inputs, Input i1, Input i2, int part) {
		List<IntResult> rv = new ArrayList<>();
		Day day;

		try {
			Class cls = Class.forName("org.f5n.aoc2020.days.Day" + sDay);
			day = (Day) cls.getDeclaredConstructor(List.class).newInstance(inputs);
		} catch (NoSuchMethodException ex) {
			logger.warn(ex.toString());
			return rv;
		} catch (IllegalAccessException ex) {
			logger.warn(ex.toString());
			return rv;
		} catch (InvocationTargetException ex) {
			logger.warn(ex.toString());
			return rv;
		} catch (ClassNotFoundException ex) {
			logger.warn(ex.toString());
			return rv;
		} catch (InstantiationException ex) {
			logger.warn(ex.toString());
			return rv;
		}

		if (day == null) {
			return rv;
		}
		IntResult ir1;
		IntResult ir2;
		if (part != 2) {
			ir1 = (IntResult) day.runPart1(i1);
			rv.add(ir1);
		}
		if (part != 1) {
			ir2 = (IntResult) day.runPart2(i2);
			rv.add(ir2);
		}

		return rv;
	}
}
