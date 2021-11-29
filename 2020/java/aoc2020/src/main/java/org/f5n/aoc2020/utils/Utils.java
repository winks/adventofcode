package org.f5n.aoc2020.utils;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.stream.Stream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


public class Utils {
	public static final String userdir = System.getProperty("user.dir");
	public static final String path1 = "/../../input/day";
	public static final String path2 = "/input.txt";
	protected static HashMap<String, ArrayList<Integer>> cacheInt = new HashMap<String, ArrayList<Integer>>();
	protected static HashMap<String, ArrayList<String>> cacheString = new HashMap<String, ArrayList<String>>();

	public static ArrayList<Integer> getLinesAsInt(String day) {
		if (cacheInt.containsKey(day)) {
			return cacheInt.get(day);
		}
		String full = userdir + path1 + day + path2;

		ArrayList<Integer> lines = new ArrayList<Integer>();
		File file = new File(full);

		try (Stream<String> linesStream = Files.lines(file.toPath())) {
			linesStream.forEach(line -> {
				Integer i = Integer.parseInt(line);
				lines.add(i);
			});
		} catch (Exception ex) {
			System.err.println("Exception: " + ex);
		}
		cacheInt.put(day, lines);
		return lines;
	}

	public static ArrayList<String> getLinesAsString(String day) {
		if (cacheString.containsKey(day)) {
			return cacheString.get(day);
		}
		String full = userdir + path1 + day + path2;

		ArrayList<String> lines = new ArrayList<String>();
		File file = new File(full);

		try (Stream<String> linesStream = Files.lines(file.toPath())) {
			linesStream.forEach(line -> {
				lines.add(line);
			});
		} catch (Exception ex) {
			System.err.println("Exception: " + ex);
		}
		cacheString.put(day, lines);
		return lines;
	}

	public static List<Integer> getLineAsInts(List<String> lines) {
		List<String> strings = Arrays.asList(lines.get(0).split(","));
		List<Integer> ints = strings.stream().map(n -> Integer.parseInt(n)).collect(Collectors.toList());
		return ints;
	}
}
