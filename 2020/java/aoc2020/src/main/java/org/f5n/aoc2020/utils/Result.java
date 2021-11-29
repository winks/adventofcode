package org.f5n.aoc2020.utils;


abstract public class Result {
	public long runtime = 0;
	abstract public String getValue();
	abstract public long getIntValue();

	public String toString() {
		return "Result<time="+runtime+",value="+getValue()+">";
	}
}
