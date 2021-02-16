package org.f5n.aoc2020;

import java.util.HashMap;
import java.util.Map;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import org.f5n.aoc2020.utils.*;
import org.f5n.aoc2020.days.*;

@RestController
public class PerfController {
    private static DayController dc = new DayController();

	@RequestMapping("/perf/{day}/{num}")
	public Map<String, Long> perf(@PathVariable int day, @PathVariable int num, 
			@RequestParam(name = "part", defaultValue = "0") int part) {
		long start = System.currentTimeMillis();
		if (part != 1 && part != 2) {
			part = 0;
		}
		for (int i = 0; i < num; ++i) {
			switch(day) {
				case 1:
					dc.day01(part);
					break;
				case 2:
					dc.day02(part);
					break;
                case 3:
					dc.day03(part);
					break;
                case 15:
					dc.day15(part);
					break;
				default:
					break;
			}
		}
		Long end = System.currentTimeMillis() - start;

		Map<String, Long> rv = new HashMap<>();
		rv.put("day", (long) day);
		rv.put("num", (long) num);
		rv.put("timeMs", end);
		rv.put("avgNs", (end * 1000 / num));
		return rv;
	}
}