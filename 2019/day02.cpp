#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>

/*
An Intcode program is a list of integers separated by commas (like 1,0,0,3,99).
To run one, start by looking at the first integer (called position 0).
Here, you will find an opcode - either 1, 2, or 99. The opcode indicates what to do;
for example, 99 means that the program is finished and should immediately halt.
Encountering an unknown opcode means something went wrong.

Opcode 1 adds together numbers read from two positions and stores the result in a third position.
The three integers immediately after the opcode tell you these three positions -
the first two indicate the positions from which you should read the input values,
and the third indicates the position at which the output should be stored.

For example, if your Intcode computer encounters 1,10,20,30, it should read the values at positions 10 and 20, add those values, and then overwrite the value at position 30 with their sum.

Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them. Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
*/

const int STEP_DEFAULT = 4;
const int OP_ADD = 1;
const int OP_MUL = 2;
const int OP_FIN = 99;

struct data {
	std::vector<int> op;
	uint position = 0;
	int status = 0;
};

void print(data x)
{
	std::cout << "# status  : " << x.status << std::endl;
	std::cout << "# position: " << x.position << std::endl;
	std::cout << "# length  : " << (int) x.op.size() << std::endl;
	for (uint i = 0; i < x.op.size()-1; ++i) {
		std::cout << x.op[i] << ',';
	}
	std::cout << x.op[x.op.size()-1] << std::endl << std::endl;
}

data calc(data v)
{
	if (v.op[v.position] == OP_FIN) {
		v.status = 10;
	} else if (v.op[v.position] == OP_ADD) {
		if (v.position + 3 > v.op.size()) {
			v.status = 20;
			return v;
		}
		int a = v.op[v.position+1];
		int b = v.op[v.position+2];
		int z = v.op[v.position+3];
		//if (z > v.op.size()+1) {
		//	v.status = 21;
		//} else {
			v.op[z] = v.op[a] + v.op[b];
			v.position += STEP_DEFAULT;
		//}
	} else if (v.op[v.position] == OP_MUL) {
		if (v.position + 3 > v.op.size()) {
			v.status = 30;
			return v;
		}
		int a = v.op[v.position+1];
		int b = v.op[v.position+2];
		int z = v.op[v.position+3];
		//if (z > v.op.size()+1) {
		//	v.status = 31;
		//} else {
			v.op[z] = v.op[a] * v.op[b];
			v.position += STEP_DEFAULT;
		//}
	} else {
		v.status = 1;
	}

	return v;
}

int main(int argc, char *argv[])
{
	std::string allops;

	std::string input;
	while (std::cin) {
		getline(std::cin, input);
		if (input.size() > 2) allops = input;
	}

	std::cout << allops << std::endl;

	uint pos = 0;

	std::vector<std::string> sops;
	std::vector<int> ops;

	std::stringstream ss(allops);
	std::string token;
	std::string::size_type sz;

	while (std::getline(ss, token, ',')) {
		sops.push_back(token);
		int num = std::stoi(token, &sz);
		ops.push_back(num);
	}
	if (ops.size() < 1) return 1;

	if (argc > 1) ops[1] = std::stoi(argv[1], &sz);
	if (argc > 2) ops[2] = std::stoi(argv[2], &sz);

	data x;
	x.op = ops;
	x.position = pos;

	print(x);

	do {
		x = calc(x);
		print(x);
	} while (x.position < x.op.size()-1 && x.status != 10);

}
