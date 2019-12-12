#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <map>
#include <sstream>
#include <vector>

const uint64_t RESIZE = 2;
const uint64_t STEP_DEFAULT = 4;

const int64_t OP_NUL = 0;
const int64_t OP_ADD = 1;
const int64_t OP_MUL = 2;
const int64_t OP_IN  = 3;
const int64_t OP_OUT = 4;
const int64_t OP_JMT = 5;
const int64_t OP_JMF = 6;
const int64_t OP_LT  = 7;
const int64_t OP_EQ  = 8;
const int64_t OP_REL = 9;
const int64_t OP_FIN = 99;

typedef std::vector<int64_t> OpList;

struct data {
	OpList op;
	uint64_t position = 0;
	int64_t status = 0;
	OpList inputs;
	OpList outputs;
	int64_t output = 0;
	int64_t relbase = 0;
};

struct instruction {
	int64_t opcode = 0;
	OpList params;
};

void ppl(OpList params, std::string prefix, std::string sep = " ")
{
	std::cout << prefix;
	if (params.size() < 1) {
		std::cout << std::endl;
		return;
	}
	if (params.size() < 2) {
		std::cout << params.front() << std::endl;
		return;
	}
	for (auto it = params.begin(); it != params.end()-1; ++it) {
		std::cout << *it << sep;
	}
	std::cout << params.back() << std::endl;
}

void print(data x, std::string prefix = "# ")
{
	std::cout << prefix << "position: " << x.position << " val: " << x.op[x.position] << std::endl;
	std::cout << prefix << "relbase : " << x.relbase << std::endl;
	std::cout << prefix << "status  : " << x.status << std::endl;
	std::string tmp(prefix); tmp.append("inputs  : ");
	ppl(x.inputs, tmp);
	tmp = prefix; tmp.append("outputs : ");
	ppl(x.inputs, tmp);
	if (x.op.size() < 33) {
		ppl(x.op, "", ",");
	}
}

void write(int64_t x)
{
	std::cout << "OUTPUT: " << x << std::endl;
}

uint64_t ain(int64_t op)
{
	switch (op) {
		case OP_NUL: return 0;
		case OP_ADD: return 2;
		case OP_MUL: return 2;
		case OP_IN : return 0;
		case OP_OUT: return 1;
		case OP_JMT: return 2;
		case OP_JMF: return 2;
		case OP_LT : return 2;
		case OP_EQ : return 2;
		case OP_REL: return 1;
		case OP_FIN: return 0;
		default: return 0;
	}
}

uint64_t aout(int64_t op)
{
	switch (op) {
		case OP_NUL: return 0;
		case OP_ADD: return 1;
		case OP_MUL: return 1;
		case OP_IN : return 1;
		case OP_OUT: return 0;
		case OP_JMT: return 0;
		case OP_JMF: return 0;
		case OP_LT : return 1;
		case OP_EQ : return 1;
		case OP_REL: return 0;
		case OP_FIN: return 0;
		default: return 0;
	}
}

uint64_t stp(int64_t op)
{
	return ain(op) + aout(op) + 1;
}

instruction parseop(int64_t op)
{
	instruction rv;
	if (op < 100) {
		rv.opcode = op;
	} else {
		rv.opcode = op % 100;
		int64_t tmp = (op - rv.opcode) / 100;
		do {
			int64_t p = tmp % 10;
			rv.params.push_back(p);
			//rv.params.insert(rv.params.begin(), p);
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
	ppl(ins.params, "### params: ");
}

static bool isimmediate(const instruction & ix, uint64_t pos)
{
	if (ix.params.size() <= pos) return false;
	return ix.params[pos] == 1 ? true : false;
}

static bool isrelative(const instruction & ix, uint64_t pos)
{
	if (ix.params.size() <= pos) return false;
	return ix.params[pos] == 2 ? true : false;
}

int64_t getbymode2(data & v, instruction ix)
{
	uint64_t num = aout(ix.opcode);
	if (num < 1) return 0;
	uint64_t asdf = v.position + ain(ix.opcode) + num;
	int64_t rv = 0;
	if (isrelative(ix, ain(ix.opcode)+num-1)) {
		asdf = v.position + ain(ix.opcode) + 1;
		if (asdf > v.op.size()) v.op.resize(asdf+RESIZE);
		rv = v.relbase + v.op[asdf];
	} else if (!isimmediate(ix, ain(ix.opcode)+num-1)) {
		asdf = v.position + ain(ix.opcode) + 1;
		if (asdf > v.op.size()) v.op.resize(asdf+RESIZE);
		rv = v.op[asdf];
	}
	std::cout << "# gbm2 " << asdf << " " << rv << "[] " << v.op.size() << std::endl;
	return rv;
}

OpList getbymode(data & v, instruction ix)
{
	OpList params;
	for (uint64_t i=0; i<ain(ix.opcode); ++i) {
		// immediate by default
		uint64_t asdf = v.position + i + 1;
		int64_t cur = v.op[asdf];

		std::cout << "##gba *" << asdf << "="<< cur << " isr: " << isrelative(ix, i) << " isi: " << isimmediate(ix, i) << std::endl;
		if (isrelative(ix, i)) {
			uint64_t nx = (uint64_t)(cur + v.relbase);
			if (v.op.size() < nx) v.op.resize(nx+RESIZE);
			cur = v.op[nx];
			std::cout << "##gbr " << cur << " " << nx << " " << v.relbase << std::endl;
		} else if (isimmediate(ix, i)) {
			std::cout << "##gbi " << cur << std::endl;
		} else {
			uint64_t nx = (uint64_t)cur;
			if (v.op.size() < nx) v.op.resize(nx+RESIZE);
			cur = v.op[nx];
			std::cout << "##gbn " << cur << std::endl;
		}
		params.push_back(cur);
	}
	return params;
}

data check(int64_t opcode, data v)
{
	uint64_t steps = stp(opcode);
	if (v.position + steps - 1 > v.op.size()) {
		v.status = 100 + opcode;
	}
	return v;
}

data calc(data v)
{
	int64_t op = v.op[v.position];
	instruction ix = parseop(op);
	pins(ix);

	std::cout << "@#pos " << v.position << " rel " << v.relbase << " op " << ix.opcode << std::endl;
	if (ix.opcode == OP_FIN) {
		v.status = 10;
	} else if (ix.opcode == OP_ADD) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		uint64_t pos = (uint64_t)getbymode2(v, ix);
		ppl(params, "# ADD ");

		int64_t z = params[0] + params[1];
		if ((uint64_t) pos > v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
		v.op[pos] = z;
		std::cout << "# ADD " << pos << " = " << v.op[pos] << " []" << v.op.size() << std::endl;
		std::cout << "@#op1 " << pos << " " << v.op[pos] << std::endl;
		v.position += STEP_DEFAULT;
	} else if (ix.opcode == OP_MUL) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		uint64_t pos = (uint64_t)getbymode2(v, ix);
		ppl(params, "# MUL ");

		int64_t z = params[0] * params[1];
		if ((uint64_t) pos > v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
		v.op[pos] = z;
		std::cout << "# MUL " << pos << " = " << v.op[pos] << " []" << v.op.size() << std::endl;
		std::cout << "@#op2 " << pos << " " << v.op[pos] << std::endl;
		v.position += STEP_DEFAULT;
	} else if (ix.opcode == OP_IN) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		uint64_t pos = (uint64_t) getbymode2(v, ix);
		int64_t n;
		std::cout << "@#op3 " << v.inputs.size() << std::endl;
		if (v.inputs.size() > 0) {
			n = v.inputs.back();
			v.inputs.pop_back();
		} else {
			v.status = 10;
			return v;
		}

		if ((uint64_t) pos > v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
		v.op[pos] = n;
		std::cout << "# IN val:" << n << " pos " << pos << " = " << v.op[pos] << std::endl;
		std::cout << "@#op3 " << pos << " " << v.op[pos] << std::endl;
		v.position += stp(ix.opcode);
	} else if (ix.opcode == OP_OUT) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		int64_t z = params[0];
		std::cout << "# OUT " << z <<  std::endl;
		std::cout << "@OUT " << z << std::endl;

		v.outputs.push_back(z);
		write(z);
		v.position += stp(ix.opcode);
	} else if (ix.opcode == OP_JMT) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		std::cout << "# JMT a " << params[0] << " b " << params[1] << " :: " << (bool)(params[0] != 0) << std::endl;
		std::cout << "@#op5 " << params[0] << " " << params[1] << std::endl;

		if (params[0] != 0) {
			v.position = (uint64_t) params[1];
		} else {
			v.position += stp(ix.opcode);
		}
	} else if (ix.opcode == OP_JMF) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		std::cout << "# JMF a " << params[0] << " b " << params[1] << " :: " << (bool)(params[0] == 0) << std::endl;
		std::cout << "@#op6 " << params[0] << " " << params[1] << std::endl;

		if (params[0] == 0) {
			v.position = (uint64_t) params[1];
		} else {
			v.position += stp(ix.opcode);
		}
	} else if (ix.opcode == OP_LT) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		uint64_t pos = (uint64_t) getbymode2(v, ix);
		std::cout << "# LT a " << params[0] << " b " << params[1] << " from pos " << pos << "|" << (params[0]<params[1]) << std::endl;

		v.op[pos] = (params[0] < params[1]) ? 1 : 0;
		std::cout << "# LT " << pos << " = " << v.op[pos] << std::endl;
		std::cout << "@#op7 " << pos << " " << v.op[pos] << std::endl;
		v.position += stp(ix.opcode);
	} else if (ix.opcode == OP_EQ) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		uint64_t pos = (uint64_t) getbymode2(v, ix);
		std::cout << "# EQ a " << params[0] << " b " << params[1] << " from pos " << pos << "|" << (params[0]==params[1]) << std::endl;

		v.op[pos] = (params[0] == params[1]) ? 1 : 0;
		std::cout << "# EQ " << pos << " = " << v.op[pos] << std::endl;
		std::cout << "@#op8 " << pos << " " << v.op[pos] << std::endl;
		v.position += stp(ix.opcode);
	} else if (ix.opcode == OP_REL) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		std::cout <<"# REL " << params[0] << std::endl;

		v.relbase += params[0];
		std::cout << "@#op9 " << v.relbase-params[0] << " " << v.relbase << std::endl;
		v.position += stp(ix.opcode);
	} else {
		v.status = 1;
	}

	std::cout << "@#sz " << v.op.size() << std::endl;
	std::cout << std::endl;

	return v;
}

OpList getops(std::string allops)
{
	OpList ops;

	std::stringstream ss(allops);
	std::string token;
	std::string::size_type sz;

	while (std::getline(ss, token, ',')) {
		int64_t num = std::stoll(token, &sz);
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

OpList convert(int64_t i)
{
	OpList rv;
	auto it = rv.begin();
	int64_t v = i % 10;
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

data runEngine(data x, OpList inputs, int num)
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

std::vector<OpList> get_perms(bool part1 = true)
{
	int myints[5];
	if (part1) {
		for (int i=0; i<5; ++i) myints[i] = i;
	} else {
		for (int i=0; i<5; ++i) myints[i] = i+5;
	}

	std::vector<OpList> rv;
	do {
		OpList r;
		for (int i=0; i<5; ++i) r.push_back(myints[i]);
		rv.push_back(r);
	} while (std::next_permutation(myints, myints+5));
	return rv;
}

void paint(uint64_t code, uint64_t start)
{

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

	//std::cout << allops << std::endl << "###" << std::endl;

	OpList ops = getops(allops);
	if (ops.size() < 1) return 1;

	// part 1
	data mx;
	mx.inputs.clear();
	mx.outputs.clear();
	mx.output = 0;

	mx.op = ops;
	mx.position = 0;
	mx.status = 0;
	mx = runEngine(mx, {0}, 0);
	print(mx);
}
