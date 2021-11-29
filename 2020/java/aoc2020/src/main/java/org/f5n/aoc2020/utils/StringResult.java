package org.f5n.aoc2020.utils;

import org.f5n.aoc2020.utils.Result;


public class StringResult extends Result {
	public String value;

	public StringResult(String value, long start) {
		this.value = value;
		this.runtime = (System.currentTimeMillis() - start);
	}

	public String getValue() {
		return "" + value;
	}
	public long getIntValue() {
		return 0;
	}

	public String toString() {
		return "Int"+super.toString();
	}
}
