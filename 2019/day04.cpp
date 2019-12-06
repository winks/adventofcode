#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <tuple>
#include <vector>

void pprint(std::vector<std::tuple<int,int>> v, std::string prefix = "")
{
	return;
	if (prefix.size() > 0) std::cout << prefix << " :: ";
	for (auto it = v.begin(); it != v.end(); ++it) {
		std::tuple<int,int> x = *it;
		std::cout << "(" << std::get<0>(x) << "/" << std::get<1>(x) << ")";
	}
	std::cout << std::endl;
}

std::vector<std::tuple<int,int>> go(std::tuple<std::string,int> s, std::tuple<int,int> origin)
{
	std::vector<std::tuple<int,int>> coords;
	std::string d = std::get<0>(s);
	int len = std::get<1>(s);
	int x = std::get<0>(origin);
	int y = std::get<1>(origin);

	std::cout << "going " << d << " " << len << " from " << x << "/" << y << std::endl;

	if (d == "R") {
		for (int i=1; i<=len; ++i) {
			x++;
			std::tuple<int,int> p = std::make_tuple(x, y);
			coords.push_back(p);
		}
	} else if (d == "U") {
		for (int i=1; i<=len; ++i) {
			y++;
			std::tuple<int,int> p = std::make_tuple(x, y);
			coords.push_back(p);
		}
	} else if (d == "L") {
		for (int i=1; i<=len; ++i) {
			x--;
			std::tuple<int,int> p = std::make_tuple(x, y);
			coords.push_back(p);
		}
	} else if (d == "D") {
		for (int i=1; i<=len; ++i) {
			y--;
			std::tuple<int,int> p = std::make_tuple(x, y);
			coords.push_back(p);
		}
	} else {
		return coords;
	}

	pprint(coords, "go");

	return coords;
}

std::vector<std::tuple<int,int>> path(std::vector<std::tuple<std::string,int>> ops, std::tuple<int,int> zero)
{
	std::vector<std::tuple<int,int>> coords;
	std::tuple<int,int> start = zero;

	for (uint i=0; i<ops.size(); ++i) {
		std::cout
			<< ".  i: " << i
			<< " start: (" << std::get<0>(start) << "/" << std::get<1>(start)
			<< ") len:" << coords.size()
			<< std::endl;
		std::vector<std::tuple<int,int>> c2 = go(ops[i], start);
		for (auto it = c2.begin(); it != c2.end(); ++it) {
			coords.push_back(*it);
		}
		start = coords.back();
		std::cout
			<< ".. i: " << i
			<< " start: (" << std::get<0>(start) << "/" << std::get<1>(start)
			<< ") len:" << coords.size()
			<< std::endl;
		pprint(coords, "path");
	}

	return coords;
}

std::vector<std::tuple<std::string,int>> parse(const std::string & arg)
{
	std::stringstream ss(arg);
	std::string token;
	std::string::size_type sz;

	std::vector<std::tuple<std::string, int>> rv;
	std::tuple<std::string, int> rvx;

	while (std::getline(ss, token, ',')) {
		if (token.size() < 2) continue;
		int num = std::stoi(token.substr(1, std::string::npos), &sz);
		rvx = std::make_tuple(token.substr(0, 1), num);
		rv.push_back(rvx);
	}

	return rv;
}

int manhattan(std::tuple<int,int> p1, std::tuple<int,int> p2)
{
	int a = std::abs(std::get<0>(p1) - std::get<0>(p2));
	int b = std::abs(std::get<1>(p1) - std::get<1>(p2));
	return a + b;
}

std::vector<std::tuple<int,int>> crossed(std::vector<std::tuple<int,int>> p1, std::vector<std::tuple<int,int>> p2)
{
	std::vector<std::tuple<int,int>> tmp;

	int64_t counter = 0;

	for (auto it1 = p1.begin(); it1 != p1.end(); ++it1) {
		int x1 = std::get<0>(*it1);
		int y1 = std::get<1>(*it1);

		for (auto it2 = p2.begin(); it2 != p2.end(); ++it2) {
			int x2 = std::get<0>(*it2);
			int y2 = std::get<1>(*it2);

			if (x1 == x2 && y1 == y2) {
				tmp.push_back(*it1);
			}
			++counter;
			if (counter % 1000000 == 0) std::cout << counter << " | " << tmp.size() << std::endl;
			if (counter % 1000000000 == 0) {
				for (auto it3 = tmp.begin(); it3 != tmp.end(); ++it3) {
					std::cout << " A " << std::get<0>(*it3) << "/" << std::get<1>(*it3);
				}
				std::cout << std::endl;
			}
		}
	}
	pprint(tmp, "crossed");

	return tmp;
}

std::tuple<int,int> find(std::vector<std::tuple<int,int>> v, std::tuple<int, int> origin)
{
	std::tuple<int,int> rv = origin;

	int lowest = 0;

	for (auto it = v.begin(); it != v.end(); ++it) {
		int man = manhattan(origin, *it);
		if (lowest == 0) {
			lowest = man;
			rv = *it;
		} else if (man < lowest) {
			lowest = man;
			rv = *it;
		}
		std::cout << lowest << std::endl;
	}

	return rv;
}

int main(int argc, char *argv[])
{
	std::vector<std::string> allops;

	if (argc < 2) {
		std::string input;
		while (std::cin) {
			getline(std::cin, input);
			if (input.size() > 2) allops.push_back(input);
		}
	} else {
		allops.push_back("R8,U5,L5,D3");
		allops.push_back("U7,R6,D4,L4");
	}

	std::cout << "lines: " << allops.size() << std::endl;

	if (allops.size() != 2) return 3;

	std::tuple<int,int> zero(0, 0);

	std::vector<std::tuple<std::string,int>> ops1 = parse(allops[0]);
	std::vector<std::tuple<int,int>> p1 = path(ops1, zero);

	std::cout << "line 1: " << p1.size() << std::endl;
	pprint(p1, "LINE1");

	std::vector<std::tuple<std::string,int>> ops2 = parse(allops[1]);
	std::vector<std::tuple<int,int>> p2 = path(ops2, zero);

	std::cout << "line 2: " << p2.size() << std::endl;
	pprint(p2, "LINE2");

	std::vector<std::tuple<int,int>> crx = crossed(p1, p2);

	std::tuple<int,int> rv = find(crx, zero);
	if (rv == zero) {
		std::cout << "NOPE" << std::endl;
	} else {
		std::cout << "YES " << std::get<0>(rv) << "/" << std::get<1>(rv) << " ~ " << manhattan(rv, zero)  << std::endl;
	}
}
