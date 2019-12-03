#include <iostream>
#include <sstream>
#include <tuple>
#include <vector>

/*
*/

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
			x++;
			std::tuple<int,int> p = std::make_tuple(x, y);
			coords.push_back(p);
		}
	} else if (d == "D") {
		for (int i=1; i<=len; ++i) {
			y++;
			std::tuple<int,int> p = std::make_tuple(x, y);
			coords.push_back(p);
		}
	} else {
		return coords;
	}

	//std::cout << "> " ;
	//for (auto it = coords.begin(); it != coords.end(); ++it) {
		//std::cout << std::get<0>(*it) << "/" << std::get<1>(*it) << " ";
	//}
	//std::cout << std::endl;

	return coords;
}

std::vector<std::tuple<int,int>> path(std::vector<std::tuple<std::string,int>> ops, std::tuple<int,int> zero)
{
	std::vector<std::tuple<int,int>> coords;

	for (uint i=0; i<ops.size(); ++i) {
		std::tuple<int,int> start;
		start = zero;
		std::cout
			<< ".  i: " << i
			<< " start: (" << std::get<0>(start) << "/" << std::get<1>(start)
			<< ") len:" << coords.size()
			<< std::endl;
		std::vector<std::tuple<int,int>> c2 = go(ops[i], start);
		start = coords.back();
		for (auto it = c2.begin(); it != c2.end(); ++it) {
			coords.push_back(*c2.data());
		}
		std::cout
			<< ".. i: " << i
			<< " start: (" << std::get<0>(start) << "/" << std::get<1>(start)
			<< ") len:" << coords.size()
			<< std::endl;
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

int manhattan()
{
	int rv = 0;
	return rv;
}

std::tuple<int,int> crossed(std::vector<std::tuple<int,int>> p1, std::vector<std::tuple<int,int>> p, std::tuple<int,int> zero)
{
	std::tuple<int,int> result;

	return result;
}

void pprint(std::vector<std::tuple<int,int>> v)
{
	for (auto it = v.begin(); it != v.end(); ++it) {
		std::tuple<int,int> x = *it;
		std::cout << "(" << std::get<0>(x) << "/" << std::get<1>(x) << ")";
	}
	std::cout << std::endl;
}

int main(int argc, char *argv[])
{
	std::vector<std::string> allops;

	std::string input;
	while (std::cin) {
		getline(std::cin, input);
		if (input.size() > 2) allops.push_back(input);
	}

	std::cout << "lines: " << allops.size() << std::endl;

	if (allops.size() != 2) return 3;

	std::tuple<int,int> zero(0, 0);

    std::vector<std::tuple<std::string,int>> ops1 = parse(allops[0]);
	std::vector<std::tuple<int,int>> p1 = path(ops1, zero);

	std::cout << "line 1: " << p1.size() << std::endl;
	pprint(p1);

    std::vector<std::tuple<std::string,int>> ops2 = parse(allops[1]);
	std::vector<std::tuple<int,int>> p2 = path(ops2, zero);

	std::cout << "line 2: " << p2.size() << std::endl;
	pprint(p2);
}
