#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
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

const int64_t DIR_UP    =  94;
const int64_t DIR_RIGHT =  62;
const int64_t DIR_DOWN  = 118;
const int64_t DIR_LEFT  =  60;

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
	int64_t dir = 0;
	bool operator==(const Point & rhs) { return this->x == rhs.x && this->y == rhs.y; }
	bool operator!=(const Point & rhs) { return !operator==(rhs); }
	std::string pp(std::string prefix = "") {
		std::string rv(prefix);
		rv.append(std::to_string(this->x));
		rv.append("/");
		rv.append(std::to_string(this->y));
		return rv;
	}
	void ppp(std::string prefix) { std::cout << pp(prefix) << std::endl;}
};

bool operator<(const Point & l, const Point & r) {
	return (l.x<r.x || (l.x==r.x && l.y<r.y));
}

void ppl(const OpList & params, const std::string & prefix, const std::string & sep = " ")
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

void ppl(std::vector<Point> params, std::string prefix = "", std::string sep = " ", bool force = false)
{
	std::cout << prefix;
	if (params.size() < 1) {
		std::cout << std::endl;
		return;
	}
	if (params.size() < 2) {
		std::cout << "(" << params.front().x << "/" << params.front().y << ")[" << "]" << std::endl;
		return;
	}
	for (auto it = params.begin(); it != params.end()-1; ++it) {
		std::cout << "("<< it->x << "/" << it->y << ")[" << "]" << sep;
	}
	std::cout << "("<< params.back().x << "/" << params.back().y << ")[" << "]" << std::endl;
}

void print(data x, std::string prefix = "# ")
{
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
		if ((uint64_t) pos >= v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
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
		if ((uint64_t) pos >= v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
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
			//v.status = 10;
			//return v;
			n = 0;
		}

		if ((uint64_t) pos >= v.op.size()) v.op.resize((uint64_t)pos+RESIZE);
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

std::string getTile(int64_t type)
{
	char aChar = type;
	std::string rv(" ");
	rv[0] = aChar;
	if (type == 0) rv[0] = '|';
	return rv;
}

bool isCrossing(int64_t i, int64_t j, int64_t image[100][100], int minw = 0, int maxw = 41, int minh = 0, int maxh = 43)
{
	if (i > minw + 1
		&& i < maxw -1
		&& j>minh+1
		&& j < maxh
		&& image[i][j-1] == 35
		&& image[i-1][j] == 35
		&& image[i+1][j] == 35
		&& image[i][j+1] == 35
	) {
	return true;
	}
	return false;
}

void show(int64_t image[100][100])
{
	int minw = 0;
	int maxw = 41;
	int minh = 0;
	int maxh = 43;

	std::cout << std::endl;
	int countblocks = 0;
	int param = 0;
	int total = 0;
	int64_t type = 0;
	std::vector<std::string> dbg;
	std::vector<int64_t> p;
	std::vector<int64_t> p2;
	std::string line("");
	std::string tile;
	for (auto j = minh; j < maxh; ++j) {
		for (auto i = minw; i < maxw; ++i) {
			type = image[i][j];
			p2.push_back(type);
			tile = getTile(image[i][j]);
			if (image[i][j] != 10) {
				if (image[i][j] == 35) {
					++countblocks;
					if (isCrossing(i, j, image, minw, maxw, minh, maxh)
					) {
							tile = "O";
							param =  i * j;
							p.push_back(i);
							p.push_back(j);
							p.push_back(0);
							total += param;
					}
				}
				std::cout << tile;
			} else {
				std::cout << std::endl;
			}
		}
	}
	std::cout << std::endl;
	std::cout << "Blocks: " << countblocks << std::endl;
	std::cout << "LP    : " << param << std::endl;
	std::cout << "Total : " << total << std::endl;
	ppl(p, "");
	int i = 0;
	int f = 0;
	for (auto it = p2.begin(); it != p2.end(); ++it) {
		++i;
		if (*it == DIR_UP) f = i;
		if (*it != 35 && *it != 46 && *it != 10) {
			std::cout << *it << " ";
		}
	}
	std::cout << std::endl << f << std::endl;;
}

bool isOut(Point a, int minw, int maxw, int minh, int maxh)
{
	return (a.x < minw || a.x > maxw-1 || a.y < minh || a.y > maxh-1);
}

Point nextStep(Point cur, int64_t dir)
{
	Point next;
	next.x = cur.x;
	next.y = cur.y;
	next.dir = dir;
	if (dir == DIR_UP) {
		next.x += 1;
	} else if (dir == DIR_RIGHT) {
		next.y += 1;
	} else if (dir == DIR_DOWN) {
		next.x -= 1;
	} else {
		next.y -= 1;
	}

	return next;
}

char pd(int64_t dir)
{
	if (dir == DIR_UP) {
		return 'N';
	} else if (dir == DIR_RIGHT) {
		return 'E';
	} else if (dir == DIR_DOWN) {
		return 'S';
	} else {
		return 'W';
	}
}

int64_t pdiff(Point from, Point to)
{
	if (from.x > to.x) {
		return DIR_LEFT;
	} else if (from.x < to.x) {
		return DIR_RIGHT;
	} else {
		if (from.y > to.y ) {
			return DIR_UP;
		} else {
			return DIR_DOWN;
		}
	}
}

bool isValid(Point a, int64_t image[100][100])
{
	return image[a.x][a.y] == 35;
}

std::vector<Point> getallne(const Point & cur, int64_t image[100][100], int64_t pref)
{
	std::vector<Point> neighbors;
	Point w1 = nextStep(cur, DIR_UP);
	Point w2 = nextStep(cur, DIR_RIGHT);
	Point w3 = nextStep(cur, DIR_DOWN);
	Point w4 = nextStep(cur, DIR_LEFT);
	Point w5 = nextStep(cur, pref);
	neighbors.push_back(w1);
	neighbors.push_back(w2);
	neighbors.push_back(w3);
	neighbors.push_back(w4);
	neighbors.push_back(w5);
	return neighbors;
}

Point fdir(Point cur, Point last, int64_t dir, int64_t image[100][100], int minw = 0, int maxw = 41, int minh = 0, int maxh = 43)
{
	std::string rv;
	std::vector<int64_t> dirs;
	//  94 = ^ UP
	//  62 = > RIGHT
	// 118 - v DOWN
	//  60 = < LEFT
	Point next = nextStep(cur, dir);
	cur .ppp("Currently     : ");
	last.ppp("Coming from   : ");
	std::vector<Point> done;
	std::vector<Point> neighbors = getallne(cur, image, cur.dir);
	bool valid = false;
	while (neighbors.size() > 0) {
		Point next = neighbors.back();
		ppl(neighbors);
		neighbors.pop_back();
		done.push_back(next);
		next.ppp("Found ini next: ");
		std::cout << (image[next.x][next.y] == 35 ? "y" : std::to_string(image[next.x][next.y])) << std::endl;
		std::cout <<
		(int) !isOut(next, minw, maxw, minh, maxh) <<
		(int) isValid(next, image) <<
		(int) (next != last) << std::endl;
		if (isOut(next, minw, maxw, minh, maxh) || !isValid(next, image) || next == last) continue;
		for (auto it = done.begin(); it != done.end(); ++ it) {
			if (next == *it) continue;
		}
		valid = true;
		dirs.push_back(next.dir);
		next.ppp("Found next ");
		return next;
	}
	return cur;
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

	int64_t image[100][100] = {};
	int i = 0;
	int64_t lastOut = 0;
	int64_t startDir = 0;
	Point lastPos;
	Point curPos;
	Point startPos;

	do {
		mx = calc(mx);
		print(mx);
		if (mx.outputs.size() > 0) {
			std::cout << "XX " << mx.outputs.size() << std::endl;
		}
		if (mx.outputs.size() > 0) {
			lastOut = mx.outputs.back();
			mx.outputs.pop_back();
			if (lastOut != 10) {
				image[curPos.x][curPos.y] = lastOut;
				if(lastOut == 60 || lastOut == 62 || lastOut == 118 || lastOut == 94) {
					startPos.x = curPos.x;
					startPos.y = curPos.y;
					startDir = lastOut;
					startPos.dir = startDir;
				std::cout << "XXX" << curPos.x << startPos.x << std::endl;
				}
				curPos.x += 1;
			} else {
				image[curPos.x+1][curPos.y] = lastOut;
				curPos.x = 0;
				curPos.y += 1;
			}
			image[curPos.x][curPos.y] = lastOut;
		}

		++i;
	} while(mx.position < mx.op.size()-1 && mx.status != 10 && mx.status != 1);

	show(image);

	OpList code2 = code;
	code2[0] = 2;
	data mx2;
	mx2.inputs.clear();
	mx2.outputs.clear();
	mx2.output = 0;
	mx2.op = code2;
	mx2.position = 0;
	mx2.status = 0;


	// part 2
	lastPos.x = startPos.x -1;
	lastPos.y = startPos.y;

	startPos.ppp("Found start: ");
	lastPos.ppp("Found last: ");
	Point next;
	Point bak;
	bak.x = startPos.x;
	bak.y = startPos.y;
	bak.dir = startPos.dir;

	std::vector<std::pair<Point, int64_t>> path;
	std::pair<Point, int64_t> sp;
	sp.first = startPos;
	sp.second = DIR_UP;
	path.push_back(sp);
	do {
		next  = fdir(startPos, lastPos, startDir, image);
		int64_t adjust = pdiff(startPos, next);
		startDir = next.dir;
		sp.first = next;
		sp.second = adjust;
		path.push_back(sp);
		lastPos = startPos;
		startPos = next;
	} while (next.x != 39);

/*
	next.y = 27;
	sp.first = next;
	sp.second = DIR_DOWN;
	path.push_back(sp);

	next.y = 28;
	sp.first = next;
	sp.second = DIR_DOWN;
	path.push_back(sp);

	next.y = 29;
	sp.first = next;
	sp.second = DIR_DOWN;
	path.push_back(sp);

	next.y = 30;
	sp.first = next;
	sp.second = DIR_DOWN;
	path.push_back(sp);

	next.x = 40;
	sp.first = next;
	sp.second = DIR_RIGHT;
	path.push_back(sp);

	next.y = 29;
	sp.first = next;
	sp.second = DIR_UP;
	path.push_back(sp);

	next.y = 28;
	sp.first = next;
	sp.second = DIR_UP;
	path.push_back(sp);

	next.y = 27;
	sp.first = next;
	sp.second = DIR_UP;
	path.push_back(sp);

	next.y = 26;
	sp.first = next;
	sp.second = DIR_UP;
	path.push_back(sp);
*/

	for (auto it = path.begin(); it != path.end(); ++it) {
		Point p = it->first;
		std::cout << "Path: " << p.pp() << " " << pd(it->second) << std::endl;
	}

	std::string rinput;
	std::vector<std::string> rinputs;
	std::pair<Point, int64_t> a = path.front();
	std::pair<Point, int64_t> b;
	int forward = 0;

	uint linelen = 14;

	int pos = -1;
	for (auto it = path.begin()+1; ;) {
		++pos;
		if (rinput.length() > linelen) {
			rinputs.push_back(rinput);
			rinput = "";
		}
		if (it == path.end()-1) {
			++forward;
			rinput.append(std::to_string(forward));
			rinputs.push_back(rinput);
			// @TODO a
			std::cout << "early" << std::endl;
			break;
		}
		b = *it;
		a.first.ppp("a is: ");
		b.first.ppp("b is: ");
		std::cout << std::to_string(a.second) << " " << std::to_string(b.second) <<  " " << pdiff(a.first, b.first) << std::endl;
		std::string tmp;
		if (a.second != pdiff(a.first, b.first)) {
			std::cout << " dirchange" << std::endl;
			if (forward > 0) {
				rinput.append(std::to_string(forward));
				rinput.append(",");
				std::cout << " fwd ended:"<< rinput << std::endl;
				forward = 0;
			}
			if (pdiff(a.first, b.first) == DIR_RIGHT) {
				tmp = (a.second == DIR_UP) ? "R,": "L,";
			} else if (pdiff(a.first, b.first) == DIR_LEFT) {
				tmp = (a.second == DIR_UP) ? "L,": "R,";
			} else if (pdiff(a.first, b.first) == DIR_UP) {
				tmp = (a.second == DIR_RIGHT) ? "L,": "R,";
			} else if (pdiff(a.first, b.first) == DIR_DOWN) {
				tmp = (a.second == DIR_RIGHT) ? "R,": "L,";
			} else {
				std::cout << "ERROR" << std::endl;
			}
			++forward;
			if (rinput.size() <= linelen) {
				rinput.append(tmp);
				std::cout << " dc: cmd not done:"<< rinput << std::endl;
				tmp = "";
				a = b;
				++it;
				continue;
			} else {
				std::cout << "dc: cmd done:"<< rinput << std::endl;
				rinputs.push_back(rinput);
				rinput = tmp;
				a = b;
				++it;
				continue;
			}
		} else {
			// go forward
			++forward;
			std::cout << "fwd is now :"<< std::to_string(forward) << std::endl;
			a = b;
			++it;
			continue;
		}
	}

	uint ASCII_y = 121;
	uint ASCII_n = 110;

/*
	std::string::size_type sz;
	for (auto it = rinputs.begin(); it != rinputs.end(); ++it) {
		std::cout << *it << std::endl;
		for (uint i = 0; i < (*it).size(); ++i) {
			char c = (*it).at(i);
			//std::cout << c << std::endl;
			mx2.inputs.push_back(c);
		}
		mx2.inputs.push_back(10);
	}
	mx2.inputs.push_back(ASCII_y);
	mx2.inputs.push_back(10);
	std::reverse(mx2.inputs.begin(), mx2.inputs.end());
	ppl(mx2.inputs, "");
	//return 2;

*/

	mx2.inputs.clear();

	rinputs.clear();

	rinput = "A,B,A,B,A,C,B,C,A,C";
	rinputs.push_back(rinput);
	rinput = "R,4,L,10,L,10";
	rinputs.push_back(rinput);
	rinput = "L,8,R,12,R,10,R,4";
	rinputs.push_back(rinput);
	rinput = "L,8,L,8,R,10,R,4";
	rinputs.push_back(rinput);

	for (auto it = rinputs.begin(); it != rinputs.end(); ++it) {
		std::cout << *it << std::endl;
		for (uint i = 0; i < (*it).size(); ++i) {
			char c = (*it).at(i);
			//std::cout << c << std::endl;
			mx2.inputs.push_back(c);
		}
		mx2.inputs.push_back(10);
	}
	mx2.inputs.push_back(ASCII_n);
	mx2.inputs.push_back(10);
	std::reverse(mx2.inputs.begin(), mx2.inputs.end());
	ppl(mx2.inputs, "FOO");

	do {
		mx2 = calc(mx2);
		print(mx2);
		if (mx2.outputs.size() > 0) {
			std::cout << "XX " << mx2.outputs.size() << std::endl;
		}
		if (mx2.outputs.size() > 0) {
			lastOut = mx2.outputs.back();
			mx2.outputs.pop_back();
			if (lastOut != 10) {
				image[curPos.x][curPos.y] = lastOut;
				if(lastOut == 60 || lastOut == 62 || lastOut == 118 || lastOut == 94) {
					startPos.x = curPos.x;
					startPos.y = curPos.y;
					startDir = lastOut;
					startPos.dir = startDir;
				std::cout << "XXX" << curPos.x << startPos.x << std::endl;
				}
				curPos.x += 1;
			} else {
				image[curPos.x+1][curPos.y] = lastOut;
				curPos.x = 0;
				curPos.y += 1;
			}
			image[curPos.x][curPos.y] = lastOut;
		}

		++i;
	} while(mx2.position < mx2.op.size()-1 && mx2.status != 10 && mx2.status != 1);

	show(image);

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

	// part2
	if (argc > 2) {
		ops[0] = 2;
	}

	OpList inputs = {0};
	if (argc > 3) {
		infile = std::ifstream(argv[3]);
		infile >> allops;
		inputs = getops(allops);
	}

	// part 1
	return paint(ops, inputs);
}
