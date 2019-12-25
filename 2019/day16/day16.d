import std.algorithm;
import std.conv;
import std.file;
import std.math;
import std.range;
import std.stdio;
import std.string;

auto part2(int nruns, string line, int off0, int multi)
{
	string offs = line[0..off0];
	int offset = to!int(offs);
	auto nums = line.repeat(multi).joiner("").drop(offset).map!(a => to!int(a) - 48).array;
	ulong len = nums.length;
	int ilen = to!int(len);
	int[] rv0 = new int[len+1];
	for (int i=0; i<len+1; ++i) {
		rv0[i] = 0;
	}

	auto input = nums;
	int[] rv = new int[len+1];
	for (int n=0; n<nruns; ++n) {
		rv = rv0.dup();
		ulong a = 13;
		for (int i=ilen-1; i>=0; --i) {
			rv[i] = (input[i] + rv[i+1]) % 10;
		}
		input = rv;
	}

	writeln("Part 2: ");
	writeln(rv.take(8).map!(a => to!string(a)).join(""));
}

auto part1(int nruns, string line)
{
	int[4] pattern;
	pattern[0] = 0;
	pattern[1] = 1;
	pattern[2] = 0;
	pattern[3] = -1;

	auto nums = line.map!(a => to!int(a) - 48).array;
	ulong len = nums.length;
	int ilen = to!int(len);

	int[] rv0 = new int[len+1];
	for (int i=0; i<len+1; ++i) {
		rv0[i] = 0;
	}

	int[] rv = new int[len+1];
	for (int n=0; n<nruns; ++n) {
		rv = rv0.dup();
		for (int i=ilen; i>=1; i--) {
			int sum = 0;
			int to=i-1;
			for (int j=ilen-1; j>= to; j--) {
				int delta = int((j+1) / i) % 4;
				sum += (nums[j] * pattern[delta]);
			}
			rv[i] = abs(sum) % 10;
		}
		nums = rv.tail(len);

	}
	writeln("Part 1: ");
	writeln(nums.take(8).map!(a => to!string(a)).join(""));
}

void main(string[] args)
{
	if (args.length < 3) return;
	string filename = args[1];
	string content = chomp(readText(filename));
	int nruns = to!int(args[2]);
	part1(100, content);
	part2(nruns, content, 7, 10000);
	//part1(100, "80871224585914546619083218645595");
}
