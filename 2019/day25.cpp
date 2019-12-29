#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */

const bool DEBUG = false;
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

struct Point {
	int64_t x = 0;
	int64_t y = 0;
};

bool operator<(const Point & l, const Point & r) {
	return (l.x<r.x || (l.x==r.x && l.y<r.y));
}

void ppl(OpList params, std::string prefix, std::string sep = " ", bool force = false)
{
	if (!DEBUG && !force) return;
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
	if (!DEBUG) return;
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
	return;
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
	if (!DEBUG) return;
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
		if (asdf >= v.op.size()) v.op.resize(asdf+RESIZE);
		rv = v.relbase + v.op[asdf];
	} else if (!isimmediate(ix, ain(ix.opcode)+num-1)) {
		asdf = v.position + ain(ix.opcode) + 1;
		if (asdf >= v.op.size()) v.op.resize(asdf+RESIZE);
		rv = v.op[asdf];
	}
	if (DEBUG) std::cout << "# gbm2 " << asdf << " " << rv << "[] " << v.op.size() << std::endl;
	return rv;
}

OpList getbymode(data & v, instruction ix)
{
	OpList params;
	for (uint64_t i=0; i<ain(ix.opcode); ++i) {
		// immediate by default
		uint64_t asdf = v.position + i + 1;
		if (asdf >= v.op.size()) v.op.resize(asdf+RESIZE);
		int64_t cur = v.op[asdf];

		if (DEBUG) std::cout << "##gba *" << asdf << "="<< cur << " isr: " << isrelative(ix, i) << " isi: " << isimmediate(ix, i) << std::endl;
		if (isrelative(ix, i)) {
			uint64_t nx = (uint64_t)(cur + v.relbase);
			if (v.op.size() <= nx) v.op.resize(nx+RESIZE);
			cur = v.op[nx];
			if (DEBUG) std::cout << "##gbr " << cur << " " << nx << " " << v.relbase << std::endl;
		} else if (isimmediate(ix, i)) {
			if (DEBUG) std::cout << "##gbi " << cur << std::endl;
		} else {
			uint64_t nx = (uint64_t)cur;
			if (v.op.size() <= nx) v.op.resize(nx+RESIZE);
			cur = v.op[nx];
			if (DEBUG) std::cout << "##gbn " << cur << std::endl;
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
	if ((uint64_t) v.position >= v.op.size()) v.op.resize((uint64_t)v.position+RESIZE);
	int64_t op = v.op[v.position];
	instruction ix = parseop(op);
	pins(ix);

	if (DEBUG) std::cout << "@#pos " << v.position << " rel " << v.relbase << " op " << ix.opcode << std::endl;
	if (ix.opcode == OP_FIN) {
		v.status = 10;
	} else if (ix.opcode == OP_ADD) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		uint64_t pos = (uint64_t)getbymode2(v, ix);
		ppl(params, "# ADD ");

		int64_t z = params[0] + params[1];
		if ((uint64_t) pos >= v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
		v.op[pos] = z;
		if (DEBUG) std::cout << "# ADD " << pos << " = " << v.op[pos] << " []" << v.op.size() << std::endl;
		if (DEBUG) std::cout << "@#op1 " << pos << " " << v.op[pos] << std::endl;
		v.position += STEP_DEFAULT;
	} else if (ix.opcode == OP_MUL) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		uint64_t pos = (uint64_t)getbymode2(v, ix);
		ppl(params, "# MUL ");

		int64_t z = params[0] * params[1];
		if ((uint64_t) pos >= v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
		v.op[pos] = z;
		if (DEBUG) std::cout << "# MUL " << pos << " = " << v.op[pos] << " []" << v.op.size() << std::endl;
		if (DEBUG) std::cout << "@#op2 " << pos << " " << v.op[pos] << std::endl;
		v.position += STEP_DEFAULT;
	} else if (ix.opcode == OP_IN) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		uint64_t pos = (uint64_t) getbymode2(v, ix);
		int64_t n;
		if (DEBUG) std::cout << "@#op3 " << v.inputs.size() << std::endl;
		if (v.inputs.size() > 0) {
			n = v.inputs.back();
			v.inputs.pop_back();
		} else {
			v.status = 10;
			return v;
		}

		if ((uint64_t) pos >= v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
		v.op[pos] = n;
		if (DEBUG) std::cout << "# IN val:" << n << " pos " << pos << " = " << v.op[pos] << std::endl;
		if (DEBUG) std::cout << "@#op3 " << pos << " " << v.op[pos] << std::endl;
		v.position += stp(ix.opcode);
	} else if (ix.opcode == OP_OUT) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		int64_t z = params[0];
		if (DEBUG) std::cout << "# OUT " << z <<  std::endl;
		if (DEBUG) std::cout << "@OUT " << z << std::endl;

		v.outputs.push_back(z);
		write(z);
		v.position += stp(ix.opcode);
	} else if (ix.opcode == OP_JMT) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		if (DEBUG) std::cout << "# JMT a " << params[0] << " b " << params[1] << " :: " << (bool)(params[0] != 0) << std::endl;
		if (DEBUG) std::cout << "@#op5 " << params[0] << " " << params[1] << std::endl;

		if (params[0] != 0) {
			if ((uint64_t) params[1] >= v.op.size()) v.op.resize((uint64_t)params[1]+RESIZE);
			v.position = (uint64_t) params[1];
		} else {
			v.position += stp(ix.opcode);
		}
	} else if (ix.opcode == OP_JMF) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		if (DEBUG) std::cout << "# JMF a " << params[0] << " b " << params[1] << " :: " << (bool)(params[0] == 0) << std::endl;
		if (DEBUG) std::cout << "@#op6 " << params[0] << " " << params[1] << std::endl;

		if (params[0] == 0) {
			if ((uint64_t) params[1] >= v.op.size()) v.op.resize((uint64_t)params[1]+RESIZE);
			v.position = (uint64_t) params[1];
		} else {
			v.position += stp(ix.opcode);
		}
	} else if (ix.opcode == OP_LT) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		uint64_t pos = (uint64_t) getbymode2(v, ix);
		if (DEBUG) std::cout << "# LT a " << params[0] << " b " << params[1] << " from pos " << pos << "|" << (params[0]<params[1]) << std::endl;

		v.op[pos] = (params[0] < params[1]) ? 1 : 0;
		if (DEBUG) std::cout << "# LT " << pos << " = " << v.op[pos] << std::endl;
		if (DEBUG) std::cout << "@#op7 " << pos << " " << v.op[pos] << std::endl;
		v.position += stp(ix.opcode);
	} else if (ix.opcode == OP_EQ) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		uint64_t pos = (uint64_t) getbymode2(v, ix);
		if (DEBUG) std::cout << "# EQ a " << params[0] << " b " << params[1] << " from pos " << pos << "|" << (params[0]==params[1]) << std::endl;

		v.op[pos] = (params[0] == params[1]) ? 1 : 0;
		if (DEBUG) std::cout << "# EQ " << pos << " = " << v.op[pos] << std::endl;
		if (DEBUG) std::cout << "@#op8 " << pos << " " << v.op[pos] << std::endl;
		v.position += stp(ix.opcode);
	} else if (ix.opcode == OP_REL) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		if (DEBUG) std::cout <<"# REL " << params[0] << std::endl;

		v.relbase += params[0];
		if (DEBUG) std::cout << "@#op9 " << v.relbase-params[0] << " " << v.relbase << std::endl;
		v.position += stp(ix.opcode);
	} else {
		v.status = 1;
	}

	if (DEBUG) std::cout << "@#sz " << v.op.size() << std::endl;
	if (DEBUG) std::cout << std::endl;

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

std::string getTile(int64_t type)
{
	switch(type) {
	case 4 : return "#";
	case 6 : return ".";
	case 8 : return "o";
	case 9 : return "D";
	default:  return " ";
	}
}

void show(int64_t image[100][100])
{
	// 4 = wall
	// 9 = droid
	// 6 = visited
	// 8 = droid + oxygen

	int minw = 0;
	int maxw = 100;
	int minh = 0;
	int maxh = 100;

	for (auto j = 0; j < 100; ++j) {
		for (auto i = 0; i < 100; ++i) {
			if (image[i][j] != 0) {
				minw = std::max(minw, i);
				maxw = std::min(maxw, i);
				minh = std::max(minh, j);
				maxh = std::min(maxh, j);
			}
		}
	}

	std::cout << std::endl;
	for (auto j = maxh; j < minh; ++j) {
		std::cout << "|" << ((j<10) ?" ":"") << j << "| ";
		for (auto i = maxw; i < minw; ++i) {
			std::cout << getTile(image[i][j]);
		}
		std::cout << std::endl;
	}
	std::cout << "|    ";
	for (auto i = minw; i < maxw; ++i) {
		if (i % 2 ==  0) {
			if (i < 10) std::cout << i;
			else std::cout << (i % 10);
		} else std::cout << " ";
	}
	std::cout << std::endl;
	std::cout << std::endl;
}

/*
    Accept a movement command via an input instruction.
    Send the movement command to the repair droid.
    Wait for the repair droid to finish the movement operation.
    Report on the status of the repair droid via an output instruction.

Only four movement commands are understood:
north (1),
south (2),
west (3), and
east (4).
Any other command is invalid. The movements differ in direction,
but not in distance: in a long enough east-west hallway, a series of commands
like 4,4,4,4,3,3,3,3 would leave the repair droid back where it started.

The repair droid can reply with any of the following status codes:

    0: The repair droid hit a wall. Its position has not changed.
    1: The repair droid has moved one step in the requested direction.
    2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.
*/

Point where(const Point & cur, int64_t direc)
{
	Point rv = cur;
	if (direc == 1) {
		rv.y -= 1;
	} else if (direc == 2) {
		rv.y += 1;
	} else if (direc == 3) {
		rv.x -= 1;
	} else if (direc == 4) {
		rv.x += 1;
	}
	return rv;
}

int64_t turnl(int64_t direc)
{
	switch (direc) {
		case 1: return 3;
		case 2: return 4;
		case 3: return 2;
		case 4: return 1;
	default: return 1;
	}
}

int64_t turnr(int64_t direc)
{
	switch (direc) {
		case 1: return 4;
		case 2: return 3;
		case 3: return 1;
		case 4: return 2;
	default: return 1;
	}
}

void showpos(const Point & cur, const Point & last, int64_t direc)
{
	std::string dir("0NSWE");
	std::cout	<< "|Pos: (" << cur.x << "/" << cur.y << ") going " << dir[(uint)direc]
				<< " Last(" << last.x << "/" << last.y << ")" << std::endl;
}

std::vector<Point> getne(const Point & cur, int64_t image[100][100])
{
	std::vector<Point> neighbors;
	Point w2;
	w2 = where(cur, 1);
	if (image[w2.x][w2.y] == 0) {
		neighbors.push_back(w2);
	}
	w2 = where(cur, 2);
	if (image[w2.x][w2.y] == 0) {
		neighbors.push_back(w2);
	}
	w2 = where(cur, 3);
	if (image[w2.x][w2.y] == 0) {
		neighbors.push_back(w2);
	}
	w2 = where(cur, 4);
	if (image[w2.x][w2.y] == 0) {
		neighbors.push_back(w2);
	}
	std::cout << "|i Pos(" << cur.x << "/" << cur.y << ") n:" << neighbors.size() << std::endl;
	for (auto i = 0; i < neighbors.size(); ++i) {
		std::cout << "|iN " << neighbors[i].x  << "/" << neighbors[i].y << "=" << image[neighbors[i].x][neighbors[i].y] << std::endl;
	}
	return neighbors;
}

int64_t manual0(int64_t image[100][100], const Point & cur, const Point &last, int64_t direc, data & mx)
{
	show(image);
	showpos(cur, last, direc);
	if (mx.inputs.size() < 1) {
		std::cin >> direc;
		int64_t fixme = direc;
		if (direc < 1 || direc > 4) direc = 1;
		if ((direc == 1 || direc == 2) && fixme < 10) {
			mx.inputs.push_back(3);
			mx.inputs.push_back(4);
			mx.inputs.push_back(4);
			mx.inputs.push_back(3);
		}
		if ((direc == 3 || direc == 4) && fixme < 10) {
			mx.inputs.push_back(1);
			mx.inputs.push_back(2);
			mx.inputs.push_back(2);
			mx.inputs.push_back(1);
		}
		std::cout << "|iX " << direc << " f" << fixme << std::endl;
		if (fixme > 10) {
			direc = fixme / 11;
			mx.inputs.clear();
		}
	} else {
		direc = mx.inputs.back();
		mx.inputs.pop_back();
	}
	return direc;
}

int64_t manual1(int64_t image[100][100], const Point & cur, const Point &last, int64_t direc, data & mx)
{
	showpos(cur, last, direc);
	show(image);
	if (mx.inputs.size() < 1) {
		std::cin >> direc;
		if (direc < 1 || direc > 4) direc = 1;
		if (direc == 1 || direc == 2) {
			mx.inputs.push_back(3);
			mx.inputs.push_back(4);
			mx.inputs.push_back(4);
			mx.inputs.push_back(3);
		}
		if (direc == 3 || direc == 4) {
			mx.inputs.push_back(1);
			mx.inputs.push_back(2);
			mx.inputs.push_back(2);
			mx.inputs.push_back(1);
		}
	} else {
		direc = mx.inputs.back();
		mx.inputs.pop_back();
	}
	return direc;
}

int paint(OpList code, OpList inputs)
{
	data mx;
	mx.inputs.clear();
	mx.outputs.clear();
	mx.output = 0;

	mx.op = code;
	mx.position = 0;
	mx.status = 0;
	mx.inputs = inputs;

	int j = 0;

	std::string input;
input ="east\nnorth\nnorth\nnorth\nsouth\neast\nnorth\nnorth\nwest\nsouth\nnorth\ntake asterisk\neast\nsouth\neast\nsouth\nwest\ntake prime number\n";
input.append("east\nnorth\ntake sand\neast\nsouth\ntake tambourine\nwest\nnorth\nwest\n");
	for (int i = input.size()-1; i>=0; --i) {
		mx.inputs.push_back(input[i]);
	}

while (true) {

j = 0;
	do {
		mx = calc(mx);

		if (DEBUG) std::cout << "AT POS " << mx.position << std::endl;
++j;
	} while(j < 500000 && mx.position < mx.op.size()-1 && mx.status != 10 && mx.status != 1 && mx.op[mx.position] != 99);

	std::cout << std::endl;
	std::cout << mx.status << " " << mx.position << std::endl;
	mx.status = 0;

if (mx.outputs.size() > 0) {
	std::cout << "==================================================================== " << std::endl;

print(mx);
for (auto it = mx.outputs.begin(); it != mx.outputs.end(); ++it) {
	char c = (char) *it;
	std::cout << c;
}
	std::cout << std::endl;

	input = "";
	getline(std::cin, input);
	std::cout << ">" << input << "<" << std::endl;

	mx.inputs.push_back(10);
	for (int i = input.size()-1; i>=0; --i) {
		char c = input[i];
		mx.inputs.push_back((long) c);
	}
for (auto it = mx.inputs.begin(); it != mx.inputs.end(); ++it) {
	std::cout << *it << " ";
}
std::cout << std::endl;

mx.outputs.clear();
}



}

	return 0;
}

int main(int argc, char *argv[])
{
	std::string allops;
	std::ifstream infile;
	if (argc > 1) {
		infile = std::ifstream(argv[1]);
		infile >> allops;
	} else {
		return 1;
	}

	OpList ops = getops(allops);
	if (ops.size() < 1) return 1;

	OpList inputs = {};
	if (argc > 2) {
		infile = std::ifstream(argv[2]);
		infile >> allops;
		inputs = getops(allops);
	}

	// part 1
	paint(ops, inputs);
}
