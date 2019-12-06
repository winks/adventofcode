#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>

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
		v.op[z] = v.op[a] + v.op[b];
		v.position += STEP_DEFAULT;
	} else if (v.op[v.position] == OP_MUL) {
		if (v.position + 3 > v.op.size()) {
			v.status = 30;
			return v;
		}
		int a = v.op[v.position+1];
		int b = v.op[v.position+2];
		int z = v.op[v.position+3];
		v.op[z] = v.op[a] * v.op[b];
		v.position += STEP_DEFAULT;
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
	} while (x.position < x.op.size()-1 && x.status != 10 && x.status != 1);
}
