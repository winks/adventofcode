#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <sstream>
#include <vector>
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */

const bool DEBUG = false;
const uint64_t RESIZE = 30;
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
	ppl(x.outputs, tmp);
	if (x.op.size() < 33) {
		ppl(x.op, "", ",");
	}
}

void write(int64_t x)
{
	if (!DEBUG) return;
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

data calc(const data & v2)
{
	data v = v2;
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
			n = 1;
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
			v.position = (uint64_t) params[1];
		} else {
			v.position += stp(ix.opcode);
		}
		if (v.position > 1000) v.position = 0;
	} else if (ix.opcode == OP_JMF) {
		v = check(ix.opcode, v);
		if (v.status >= 100 && v.status < 200) return v;

		OpList params = getbymode(v, ix);
		if (DEBUG) std::cout << "# JMF a " << params[0] << " b " << params[1] << " :: " << (bool)(params[0] == 0) << std::endl;
		if (DEBUG) std::cout << "@#op6 " << params[0] << " " << params[1] << std::endl;

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

int single(data v, OpList code, int x, int y)
{
	v.status = 0;
	v.position = 0;
	v.relbase = 0;
	v.inputs.clear();
	v.output = 0;
	v.outputs.clear();
	v.op = code;
	v.inputs.push_back(y);
	v.inputs.push_back(x);

	if (DEBUG) std::cout << "  CHK " << x << "/" << y << std::endl;

	do {
		v = calc(v);
		print(v);
		if (v.outputs.size() > 0) {
			return v.outputs.front();
		}
	} while (v.position < v.op.size()-1 && v.status != 10 && v.status != 1);

	return 666;
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
	return (type == 1) ? "#" : ".";
}

void show(int64_t image[100][100], uint maxw, uint maxh, uint size)
{
	uint minw = 0;
	uint minh = 0;

	std::vector<uint> offsets;
	std::vector<uint> offsets2;
	std::vector<uint> cand;

	for (auto j = minh; j < maxh; ++j) {
		uint countRow = 0;
		uint offs = 0;
		uint offs2 = 0;
		for (auto i = minw; i < maxw; ++i) {
			if (image[i][j] == 1) {
				++countRow;
				if (offs == 0) offs = i;
				offs2 = i;
			}
			std::cout << getTile(image[i][j]);
		}
		if (countRow >= size) {
			cand.push_back(j);
			//std::cout << "cand " << j << std::endl;
			offsets.push_back(offs);
			offsets2.push_back(offs2);
		}
		offs = 0;
		std::cout << std::endl;
	}
	std::cout << std::endl;

	uint idx = 0;
	for (auto it = cand.begin(); it != cand.end(); ++it) {
		uint j = *it;
		// longer than the image
		if (j + size > maxh) continue;
		//std::cout << "  ROW " << j << std::endl;

		for (uint col = offsets.at(idx); col <= offsets2.at(idx)-size+1; ++col) {
			uint lenRow = 0;
			uint lastCol;
			for (uint row = j; row<j+size; ++row) {
				uint curCol = col;
				//std::cout <<  "    CHK: " << row << "/" << curCol << std::endl;
				if (image[col][row] == 1) ++lenRow;
				lastCol = curCol;
			}
			if (lenRow >= size) std::cout << "OK     ROW: " << j << "/" << lastCol << ":: " << (lastCol * 10000) + j << std::endl;
			//else std::cout << "  FAIL ROW: " << j << "/" << lastCol << ":: " << lenRow << std::endl;
		}
		++idx;
	}
}

int paint2(OpList code, OpList inputs)
{
	int cnt = 0;
	int affectedRow = 0;
	int minx = 0;
	int64_t lout = 0;

	int minw = 400;
	int maxw = 1000;
	int minh = 850;
	int maxh = 1200;
	uint searchSize = 100;
	OpList lastIn;

	//minh = 35;
	//maxh = 45;
	//minw = 20;
	//maxw = 30;
	//searchSize = 4;

	// map 100x100 => size 8 = > found 81/50 =>  on line 80: x =50, start on row 75 = 10 first len 8 on row 57
	// 10 in 100x100 => 75
	// size 100 => 1000x1000 => 750

	std::cout << "### PART 2 ###################################" << std::endl;
	for (int y = minh; y < maxh; ++y) {
		affectedRow = 0;
		int firstx = 0;
		for (int x = minw; x < maxw; ++x) {
			data mx;
			mx.status = 0;
			mx.position = 0;
			mx.relbase = 0;
			mx.inputs.clear();
			mx.output = 0;
			mx.outputs.clear();
			mx.op = code;

			mx.inputs.push_back(y);
			mx.inputs.push_back(x);

			do {
				mx = calc(mx);
				print(mx);

				if (mx.outputs.size() > 0) {
					lout = mx.outputs.front();
					mx.outputs.clear();
					//std::cout << "FT " << x << "/" << y << " = " << lout << std::endl;
					if (lout == 1) {
						++affectedRow;
						// save some processing time
						//if (minx == 0) {
						//	minx = x;
						//	firstx = x;
						//}
						firstx = x;
					}
				}

				if (firstx == x) {
					data mx2;
					int x2 = x;
					int y2 = y+searchSize-1;
					int r = single(mx2, code, x2, y2);
					if (r == 1) {
						if (DEBUG) std::cout << "  FOUND y " << x << "/" << y << " last row size: " << affectedRow  << std::endl;
						data mx3;
						x2 = x+searchSize-1;
						y2 = y;
						r = single(mx3, code, x2, y2);
						if (r == 1) {
							std::cout << "  FOUND x " << x << "/" << y << std::endl;
							return 10000 * x + y;
						}
					}
				}

				++cnt;
				firstx = 0;
			} while(mx.position < mx.op.size()-1 && mx.status != 10 && mx.status != 1);
		}
		if (DEBUG) std::cout << "ROW " << y << " " << affectedRow << std::endl;
	}
	//show(image, maxw, maxh, searchSize);

	//std::cout << "SIZE " << (maxw * maxh) << std::endl;
	//std::cout << "AFF  " << affectedRow << std::endl;

	return 0;
}

int paint(OpList code, OpList inputs)
{
	int64_t image[100][100] = {};
	int cnt = 0;
	int affected = 0;
	int64_t lout = 0;

	int maxw = 50;
	int maxh = 50;
	uint searchSize = 8;
	OpList lastIn;

	for (int y = maxh-1; y >= 0; --y) {
		for (int x = maxw-1; x >= 0; --x) {
			data mx;
			mx.status = 0;
			mx.position = 0;
			mx.relbase = 0;
			mx.inputs.clear();
			mx.output = 0;
			mx.outputs.clear();
			mx.op = code;

			mx.inputs.push_back(y);
			mx.inputs.push_back(x);

			do {
				mx = calc(mx);
				print(mx);

				if (mx.outputs.size() > 0) {
					lout = mx.outputs.front();
					mx.outputs.clear();
					image[x][y] = lout;
					if (lout == 1) ++affected;
				}
				++cnt;
			} while(mx.position < mx.op.size()-1 && mx.status != 10 && mx.status != 1);
		}
	}
	if (DEBUG) show(image, maxw, maxh, searchSize);

	std::cout << "SIZE " << (maxw * maxh) << std::endl;
	std::cout << "AFF  " << affected << std::endl;

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

	// part 2
	if (argc > 2) {
		int p2 = paint2(ops, inputs);
		std::cout << "Part 2: " << p2 << std::endl;
		return 0;
	}

	paint(ops, inputs);
}
