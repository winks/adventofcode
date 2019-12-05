#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>

const int STEP_DEFAULT = 4;
const int STEP_IN      = 2;
const int STEP_OUT     = 2;
const int OP_ADD = 1;
const int OP_MUL = 2;
const int OP_IN  = 3;
const int OP_OUT = 4;
const int OP_FIN = 99;

struct data {
	std::vector<int> op;
	uint position = 0;
	int status = 0;
};

struct instruction {
	int opcode = 0;
	std::vector<int> params;
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

void write(int x)
{
	std::cout << "OUTPUT: " << x << std::endl;
}

instruction parseop(int op)
{
	instruction rv;
	if (op < 100) {
		rv.opcode = op;
	} else {
		rv.opcode = op % 100;
		int tmp = (op - rv.opcode) / 100;
		do {
			int p = tmp % 10;
			rv.params.push_back(p);
			tmp -= p;
			tmp = tmp / 10;
		} while (tmp > 0);
	}
	while (rv.params.size() < STEP_DEFAULT-1) {
		rv.params.push_back(0);
	}
	return rv;
}

void pins(instruction ins)
{
	std::cout << "## opcode: " << ins.opcode << std::endl;
	std::cout << "## params: ";
	for (auto it = ins.params.begin(); it != ins.params.end(); ++it) {
		std:: cout << *it << ",";
	}
	std::cout << std::endl;
}

bool isimmediate(instruction ix, uint pos)
{
	if (ix.params.size() <= pos) return false;
	return ix.params[pos] > 0 ? true : false;
}

data calc(data v)
{
	int op = v.op[v.position];
	instruction ix = parseop(op);
	pins(ix);

	if (ix.opcode == OP_FIN) {
		v.status = 10;
	} else if (ix.opcode == OP_ADD) {
		if (v.position + 3 > v.op.size()) {
			v.status = 20;
			return v;
		}
		std::vector<int> params;
		params.push_back(v.op[v.position+1]);
		params.push_back(v.op[v.position+2]);
		params.push_back(v.op[v.position+3]);

		std::cout << "# ADD ";
		for (auto it = params.begin(); it != params.end(); ++it) {
			std::cout << *it << " ";
		}
		std::cout << std::endl;

		int a = isimmediate(ix, 0) ? params[0] : v.op[(uint)params[0]];
		int b = isimmediate(ix, 1) ? params[1] : v.op[(uint)params[1]];
		int z = a + b;

		v.op[(uint)params[2]] = z;
		v.position += STEP_DEFAULT;
	} else if (ix.opcode == OP_MUL) {
		if (v.position + 3 > v.op.size()) {
			v.status = 30;
			return v;
		}
		std::vector<int> params;
		params.push_back(v.op[v.position+1]);
		params.push_back(v.op[v.position+2]);
		params.push_back(v.op[v.position+3]);

		std::cout << "# MUL ";
		for (auto it = params.begin(); it != params.end(); ++it) {
			std::cout << *it << " ";
		}
		std::cout << std::endl;

		int a = isimmediate(ix, 0) ? params[0] : v.op[(uint)params[0]];
		int b = isimmediate(ix, 1) ? params[1] : v.op[(uint)params[1]];
		int z = a * b;

		v.op[(uint)params[2]] = z;
		v.position += STEP_DEFAULT;
	} else if (ix.opcode == OP_IN) {
		if (v.position + 1 > v.op.size()) {
			v.status = 40;
			return v;
		}
		int z = v.op[v.position+1];
		int n;
		std::cin >> n;
		std::cout << "# IN " << n << " to " << z << " pos " << v.position+1 << std::endl;
		v.op[(uint)z] = n;
		v.position += STEP_IN;
	} else if (ix.opcode == OP_OUT) {
		if (v.position + 1 > v.op.size()) {
			v.status = 50;
			return v;
		}
		int a = v.op[v.position+1];
		int z = v.op[(uint)a];
		std::cout << "# OUT " << a << " from pos " << v.position+1 << std::endl;
		write(z);
		v.position += STEP_OUT;
	} else {
		v.status = 1;
	}

	return v;
}

std::vector<int> getops(std::string allops)
{
	std::vector<int> ops;

	std::stringstream ss(allops);
	std::string token;
	std::string::size_type sz;

	while (std::getline(ss, token, ',')) {
		int num = std::stoi(token, &sz);
		ops.push_back(num);
	}

	return ops;
}

std::string getin()
{
	std::string allops;

	std::string input;
	while (std::cin) {
		getline(std::cin, input);
		if (input.size() > 2) allops = input;
	}

	return allops;
}

int main(int argc, char *argv[])
{
	std::string::size_type sz;
	std::string allops;
	if (argc > 1) {
		std::ifstream infile(argv[1]);
		infile >> allops;
	}

	//std::string allops = getin();
	std::cout << allops << std::endl << "###" << std::endl;

	std::vector<int> ops = getops(allops);
	if (ops.size() < 1) return 1;

	if (argc > 2) ops[1] = std::stoi(argv[2], &sz);
	if (argc > 3) ops[2] = std::stoi(argv[3], &sz);

	data x;
	x.op = ops;
	x.position = 0;

	print(x);

	do {
		x = calc(x);
		print(x);
	} while (x.position < x.op.size()-1 && x.status != 10);

}
