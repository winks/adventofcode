package org.f5n.aoc2020.utils;

import org.f5n.aoc2020.utils.Result;

public class IntResult extends Result {
	public long value = 0;

	public IntResult() {}

	public IntResult(long value) {
		this.value = value;
	}
	
	public String getValue() {
		return "<" + value + ">";
	}
	public long getIntValue() {
		return value;
	}

	public String toString() {
		return "Int"+super.toString();
	}
}
