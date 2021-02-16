package org.f5n.aoc2020.utils;

public class IntInput extends Input {
    public int value = 0;

    public IntInput(int value) {
        this.value = value;
    }

    public int getIntValue() {
        return value;
    }
}