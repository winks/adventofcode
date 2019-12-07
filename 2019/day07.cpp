#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>

const int STEP_DEFAULT = 4;
const int STEP_IN      = 2;
const int STEP_OUT     = 2;
const int STEP_JMT     = 3;
const int STEP_JMF     = 3;
const int STEP_LT      = 4;
const int STEP_EQ      = 4;

const int OP_ADD = 1;
const int OP_MUL = 2;
const int OP_IN  = 3;
const int OP_OUT = 4;
const int OP_JMT = 5;
const int OP_JMF = 6;
const int OP_LT  = 7;
const int OP_EQ  = 8;
const int OP_FIN = 99;

struct data {
	std::vector<int> op;
	uint position = 0;
	int status = 0;
	std::vector<int> inputs;
	std::vector<int> outputs;
	int output = 0;
};

struct instruction {
	int opcode = 0;
	std::vector<int> params;
};

void print(data x, std::string prefix = "# ")
{
	std::cout << prefix << "position: " << x.position << " val: " << x.op[x.position] << std::endl;
	std::cout << prefix << "length  : " << (int) x.op.size() << std::endl;
	std::cout << prefix << "status  : " << x.status << std::endl;
	std::cout << prefix << "inputs  : ";
	for (auto it = x.inputs.begin(); it != x.inputs.end(); ++it) {
		std::cout << *it << ",";
	}
	std::cout << std::endl;
	std::cout << prefix << "outputs : ";
	for (auto it = x.outputs.begin(); it != x.outputs.end(); ++it) {
		std::cout << *it << ",";
	}
	std::cout << std::endl;
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
	std::cout << "### opcode: " << ins.opcode << std::endl;
	std::cout << "### params: ";
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
			v.status = 100 + OP_ADD;
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
			v.status = 100 + OP_MUL;
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
			v.status = 100 + OP_IN;
			return v;
		}
		uint pos = v.position+1;
		int z = v.op[pos];
		int n;
		if (v.inputs.size() > 0) {
            n = v.inputs.back();
			v.inputs.pop_back();
		} else {
			v.status = 10;
			return v;
			//std::cin >> n;
		}
		std::cout << "# IN val: " << n << " address: pos " << pos << " val: " << z << " => " << n << std::endl;

		v.op[(uint)z] = n;
		v.position += STEP_IN;
	} else if (ix.opcode == OP_OUT) {
		if (v.position + 1 > v.op.size()) {
			v.status = 100 + OP_OUT;
			return v;
		}
		uint pos = v.position+1;
		int a = v.op[pos];
		int z = isimmediate(ix, 0) ? v.op[pos] : v.op[(uint)a];
		std::cout << "# OUT " << z << " from pos " << pos << " = " << z << std::endl;

		v.outputs.push_back(z);
		write(z);
		v.position += STEP_OUT;
	} else if (ix.opcode == OP_JMT) {
		if (v.position + 2 > v.op.size()) {
			v.status = 100 + OP_JMT;
			return v;
		}
		std::vector<int> params;
		params.push_back(v.op[v.position+1]);
		params.push_back(v.op[v.position+2]);

		int a = isimmediate(ix, 0) ? params[0] : v.op[(uint)params[0]];
		int b = isimmediate(ix, 1) ? params[1] : v.op[(uint)params[1]];
		std::cout << "# JMT a " << params[0] << "=" << a << " b " << params[1] << "=" << b << " :: " << (bool)(a != 0) << std::endl;

		if (a != 0) {
			v.position = (uint)b;
		} else {
			v.position += STEP_JMT;
		}
	} else if (ix.opcode == OP_JMF) {
		if (v.position + 2 > v.op.size()) {
			v.status = 100 + OP_JMF;
			return v;
		}
		std::vector<int> params;
		params.push_back(v.op[v.position+1]);
		params.push_back(v.op[v.position+2]);

		int a = isimmediate(ix, 0) ? params[0] : v.op[(uint)params[0]];
		int b = isimmediate(ix, 1) ? params[1] : v.op[(uint)params[1]];
		std::cout << "# JMF a *" << params[0] << "=" << a << " b *" << params[1] << "=" << b << " :: " << (bool)(a == 0) << std::endl;

		if (a == 0) {
			std::cout << "# JMF *" << v.position << "=" << v.op[v.position] << " => *" << b << "=" << v.op[(uint)b] << std::endl;
			v.position = (uint)b;
		} else {
			v.position += STEP_JMF;
		}
	} else if (ix.opcode == OP_LT) {
		if (v.position + 3 > v.op.size()) {
			v.status = 100 + OP_LT;
			return v;
		}
		std::vector<int> params;
		params.push_back(v.op[v.position+1]);
		params.push_back(v.op[v.position+2]);
		params.push_back(v.op[v.position+3]);

		int a = isimmediate(ix, 0) ? params[0] : v.op[(uint)params[0]];
		int b = isimmediate(ix, 1) ? params[1] : v.op[(uint)params[1]];
		int pos = params[2];
		std::cout << "# LT a " << a << " b " << b << " from pos " << pos << std::endl;

		v.op[(uint)pos] = (a < b) ? 1 : 0;
		v.position += STEP_LT;
	} else if (ix.opcode == OP_EQ) {
		if (v.position + 3 > v.op.size()) {
			v.status = 100 + OP_EQ;
			return v;
		}
		std::vector<int> params;
		params.push_back(v.op[v.position+1]);
		params.push_back(v.op[v.position+2]);
		params.push_back(v.op[v.position+3]);

		int a = isimmediate(ix, 0) ? params[0] : v.op[(uint)params[0]];
		int b = isimmediate(ix, 1) ? params[1] : v.op[(uint)params[1]];
		int z = params[2];

		v.op[(uint)z] = (a == b) ? 1 : 0;
		v.position += STEP_EQ;
	} else {
		v.status = 1;
	}
	std::cout << std::endl;

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

data step(data v)
{
	print(v, "#GO## ");

	do {
		v = calc(v);
		print(v);
	} while (v.position < v.op.size()-1 && v.status != 10 && v.status != 1);

	v.status = 0;
	print(v, "#END# ");

	return v;
}

std::vector<int> convert(int i)
{
	std::vector<int> rv;
	auto it = rv.begin();
	int v = i % 10;
	it = rv.begin();
	rv.insert(it, v);

	i -= v;
	i /= 10;
	v = i % 10;
	it = rv.begin();
	rv.insert(it, v);

	i -= v;
	i /= 10;
	v = i % 10;
	it = rv.begin();
	rv.insert(it, v);

	i -= v;
	i /= 10;
	v = i % 10;
	it = rv.begin();
	rv.insert(it, v);

	i -= v;
	i /= 10;
	it = rv.begin();
	rv.insert(it, i);

	return rv;
}

data runEngine(data x, std::vector<int> inputs, int num)
{
	std::cout << "# Starting engine " << num << std::endl;
	x.inputs = inputs;
	x = step(x);
	if (x.outputs.size() < 1) {
		std::cout << "NO OUTPUT! " << num << std::endl;
		x.status = 200 + num;
		x.output = 0;
	} else {
		x.output = x.outputs.front();
		x.status = 0;
	}
	x.outputs.clear();

	return x;
}

std::vector<std::vector<int>> get_perms(bool part1 = true)
{
	int myints[5];
	if (part1) {
		for (int i=0; i<5; ++i) myints[i] = i;
	} else {
		for (int i=0; i<5; ++i) myints[i] = i+5;
	}

	std::vector<std::vector<int>> rv;
	do {
		std::vector<int> r;
		for (int i=0; i<5; ++i) r.push_back(myints[i]);
		rv.push_back(r);
	} while (std::next_permutation(myints, myints+5));
	return rv;
}

int main(int argc, char *argv[])
{
	std::string allops;
	if (argc > 1) {
		std::ifstream infile(argv[1]);
		infile >> allops;
	} else {
		return 1;
	}

	std::cout << allops << std::endl << "###" << std::endl;

	std::vector<int> ops = getops(allops);
	if (ops.size() < 1) return 1;

	bool part1 = true;
	if (argc > 2) {
		std::string testMode(argv[2]);
		if (testMode == "2") part1 = false;
	}

	std::vector<std::vector<int>> all_sets;
	std::vector<int> set1;
	int runOnlySet = -1;
	if (argc > 3) {
		runOnlySet = std::stoi(argv[3]);
		if (runOnlySet >= 0 && runOnlySet <= 99999) {
			set1 = convert(runOnlySet);
			all_sets.push_back(set1);
		}
	} else {
		all_sets = get_perms(part1);
	}

	int i = 0;
	for (auto sit = all_sets.begin(); sit != all_sets.end(); ++sit) {
		set1 = *sit;
		std::cout << "SET " << i++ << " = ";
		for (auto it = set1.begin(); it != set1.end(); ++it) {
			std:: cout << *it << ",";
		}
		std::cout << std::endl;

		if (part1) {
			/*
			At its first input instruction, provide it the amplifier's phase setting, [3].
			At its second input instruction, provide it the input signal, [0]
			My inputs are reversed, so this would be 0,3 and not 3,0
			Also the first input signal is always 0.
			*/
			data mx;
			mx.inputs.clear();
			mx.outputs.clear();
			mx.output = 0;

			for (int num = 0; num<5; ++num) {
				mx.op = ops;
				mx.position = 0;
				mx.status = 0;
				mx = runEngine(mx, {mx.output, set1[num]}, num);
				if (mx.status >= 200) {
					break;
				}
			}
			std::cout << "FINAL " << mx.output << std::endl;
		} else {
			data buffer;
			buffer.output = 0;
			data mxs[5];
			for (int im=0; im<5; ++im) {
				data tmpd;
				tmpd.op = ops;
				mxs[im] = tmpd;
			}

			bool running = true;
			int initial = 5;
			while (running) {
				for (int num = 0; num<5; ++num) {
					std::cout << "INITIAL " << initial << std::endl;
					if (initial > 0) {
						mxs[num] = runEngine(mxs[num], {buffer.output, set1[num]}, num);
						--initial;
					} else {
						mxs[num] = runEngine(mxs[num], {buffer.output}, num);
					}
					if (mxs[num].status >= 200) {
						running = false;
						break;
					}
					buffer = mxs[num];
				}
				std::cout << "FINAL? " << buffer.output << std::endl;
			}
			std::cout << "FINAL " << buffer.output << std::endl;
		}
	}
}
