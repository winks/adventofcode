#include <cmath>
#include <iostream>
#include <string>

/*
At the first Go / No Go poll, every Elf is Go until the Fuel Counter-Upper. They haven't determined the amount of fuel required yet.

Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

For example:

For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
For a mass of 1969, the fuel required is 654.
For a mass of 100756, the fuel required is 33583.
The Fuel Counter-Upper needs to know the total fuel requirement. To find it, individually calculate the fuel needed for the mass of each module (your puzzle input), then add together all the fuel values.

What is the sum of the fuel requirements for all of the modules on your spacecraft?

*/
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
