import std.algorithm;
import std.conv;
import std.file;
import std.range;
import std.stdio;
import std.string;

auto part2(int nruns, string line, int off0, int multi)
{
	writeln("Phases: ", nruns);
	string offs = line[0..off0];
	writeln("len   : ",line.length);
	int offset = to!int(offs);
	writeln("offset: ", offset);
	auto nums = line.repeat(multi).joiner("").drop(offset).map!(a => to!int(a) - 48).array;
	ulong len = nums.length;
	writeln("len   : ",len);
	int[] rv0 = new int[len+1];
	for (int i=0; i<len+1; ++i) {
		rv0[i] = 0;
	}

	auto input = nums;
	int[] rv = new int[len+1];
	for (int n=0; n<nruns; ++n) {
		rv = rv0.dup();
		ulong a = 13;
		for (ulong i=len-1; i>0; --i) {
			rv[i] = (input[i] + rv[i+1]) % 10;
		}
		rv[0] = (input[0] + rv[1]) % 10;
		input = rv;
	}

	writeln("Part 2: ");
	writeln(rv.take(8).map!(a => to!string(a)).join(""));
}

void main(string[] args)
{
	if (args.length < 3) return;
	string filename = args[1];
	string content = chomp(readText(filename));
	int nruns = to!int(args[2]);
	part2(nruns, content, 7, 10000);
}
