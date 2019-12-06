#include <cmath>
#include <iostream>
#include <string>

int cf(int mass)
{
	float n1 = mass / 3.0;
	int n2 = std::floor(n1);
	return n2 - 2;
}

int main(int argc, char * argv[])
{
	std::string input;
	std::string::size_type sz;
	int total = 0;
	int total2 = 0;
	while (std::cin) {
		getline(std::cin, input);
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

		std::cout << " = " << num << " => " << num2 << " :: " << total2 << " :: " << (total + total2)<< std::endl;
	}
}
