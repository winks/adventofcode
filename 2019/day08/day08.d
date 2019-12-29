import std.algorithm;
import std.conv;
import std.file;
import std.math;
import std.range;
import std.stdio;
import std.string;

auto part2(string line, int iw, int ih)
{
	ulong dim = iw*ih;
	ulong layer = 0;
	ulong pos = 0;
	ulong posr = 0;

	int[] rv = new int[dim];
	for (int j=to!int(line.length)-1; j>=0; --j) {
		pos = j % dim;
		posr = dim - pos - 1;
		//writeln("j ",j," p ",posr," ~ ", line[j]);
		if (layer == 0 || line[j] == '0' || line[j] == '1') {
			rv[posr] = line[j];
		}
		layer += 1;

	}
	writeln("Part 2: ");
	for (int j=0; j<ih;++j){
		for (int i=0; i<iw; ++i) {
			int pos2 = i + (j*iw);
			if  (rv[pos2] == '1') write("░");
			if  (rv[pos2] == '2') write(".");
			if  (rv[pos2] == '0') write(" ");
		}
		writeln();
	}
}

auto part1(string line, int iw, int ih)
{
	ulong dim = iw*ih;
	ulong h = 0;
	int[3] min = new int[3];
	int[3] cur = new int[3];
	min[0] = to!int(dim)+1;
	cur[0] = 0;
	cur[1] = 0;
	cur[2] = 0;

	for (int j=0; j<line.length; ++j) {
		//writeln("j ",j," h ",h," ~ ", line[j]);
		if (line[j] == '0') cur[0] += 1;
		if (line[j] == '1') cur[1] += 1;
		if (line[j] == '2') cur[2] += 1;
		if (j > 0 && (j % dim == dim-1)) {
			//writeln("Layer ",h," z: ",cur[0]," o ",cur[1]," t ",cur[2]," =",(cur[1]*cur[2]));
			if (cur[0] < min[0]) {
				min[0] = cur[0];
				min[1] = cur[1];
				min[2] = cur[2];
			}
			cur[0] = 0;
			cur[1] = 0;
			cur[2] = 0;
			h += 1;
		}
	}

	writeln("Part 1: ",(min[1]*min[2]));
}

void main(string[] args)
{
	if (args.length < 3) return;
	string filename = args[1];
	string content = chomp(readText(filename));
	int iw = to!int(args[2]);
	int ih = to!int(args[3]);
	if (args.length > 4) {
		if (to!int(args[4]) == 2) {
			part2(content, iw, ih);
			return;
		}
		if (to!int(args[4]) == 1) {
			part1(content, iw, ih);
			return;
		}
	}
	part1(content, iw, ih);
	part2(content, iw, ih);
}
