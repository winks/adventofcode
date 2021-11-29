package org.f5n.aoc2020;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.HashMap;
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
public class PerfController {
	protected final Logger logger = LoggerFactory.getLogger(getClass());
	private static DayController dc = new DayController();

	@RequestMapping("/perf/{day}/{num}")
	public Map<String, Long> perf(@PathVariable int day, @PathVariable int num, 
			@RequestParam(name = "part", defaultValue = "0") int part) {
		long start = System.currentTimeMillis();
		Map<String, Long> rv = new HashMap<>();
		if (day < 1 || day > 25 ) {
			rv.put("error", 1L);
			return rv;
		}
		if (part < 1 || part > 2) {
			part = 0;
		}
		String sDay = "" + (day > 10 ? day : "0" + day);
		Method dayMethod;
		try {
			dayMethod = DayController.class.getMethod("day" + sDay, int.class);
			logger.info("Calling DC.day" + sDay + "(" + part + ")");

			for (int i = 0; i < num; ++i) {
				dayMethod.invoke(dc, part);
			}
		} catch (NoSuchMethodException ex) {
			logger.warn(ex.toString());
			rv.put("error", 2L);
			return rv;
		} catch (IllegalAccessException ex) {
			logger.warn(ex.toString());
			rv.put("error", 2L);
			return rv;
		} catch (InvocationTargetException ex) {
			logger.warn(ex.toString());
			rv.put("error", 2L);
			return rv;
		}
		Long end = System.currentTimeMillis() - start;

		rv.put("day", (long) day);
		rv.put("num", (long) num);
		rv.put("timeMs", end);
		rv.put("avgNs", (end * 1000 / num));
		return rv;
	}
}