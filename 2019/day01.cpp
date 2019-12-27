#include <cmath>
#include <iostream>
#include <fstream>
#include <string>

int cf(int mass)
{
	float n1 = mass / 3.0;
	int n2 = std::floor(n1);
	return n2 - 2;
}

int main(int argc, char * argv[])
{
	if (argc < 2) {
		std::cout << "Usage: " << argv[0] << " /path/to/file" << std::endl;
		return 0;
	}
	std::ifstream infile = std::ifstream(argv[1]);
	std::string input;
	std::string::size_type sz;
	int total = 0;
	int total2 = 0;
	while (infile >> input) {
		if (input.size() < 2) continue;
		std::cout << "> " << input;
		int num = std::stoi(input, &sz);
		int num2 = cf(num);
		total += num2;

		std::cout << " = " << num << " => " << num2 << " :: " << total << std::endl;

		int fuel = num2;
		do {
			fuel = cf(fuel);
			if (fuel > 0) total2 += fuel;
		} while (fuel > 0);

		std::cout << " = " << num << " => " << num2 << " :: " << total2 << " :: " << (total + total2) << std::endl;
		std::cout << total << " + " << total2 << " = " << (total + total2) << std::endl;
	}
}
