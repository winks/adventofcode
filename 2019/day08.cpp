#include <algorithm>
#include <iostream>
#include <iterator>
#include <fstream>
#include <vector>

int main(int argc, char *argv[])
{
	std::string data;
	size_t iw = 0;
	size_t ih = 0;
	size_t nlayers = 0;
	if (argc > 1) {
		std::ifstream infile(argv[1]);
		infile >> data;
	}
	if (argc < 4) {
		return 1;
	}
	iw = (size_t) std::stoi(argv[2]);
	ih = (size_t) std::stoi(argv[3]);
	nlayers = data.size() / (iw*ih);

	//std::cout << data << std::endl << std::endl;
	std::cout << "# w: " << iw << " h: " << ih << " = " << iw*ih << std::endl;
	std::cout << "# got: " << data.size() << " = " << nlayers << " layers" << std::endl;

	std::vector<std::string> slayers;

	for (size_t i=0; i<data.size(); i+=(iw*ih)) {
		std::string layer = data.substr(i, (iw*ih));
		//std::cout << "# step " << i << " = " << layer << std::endl;
		slayers.insert(slayers.end(), layer);
	}

	size_t min_layer = 0;
	int num_zero = 0;
	int num_one = 0;
	int num_two = 0;
	for (size_t i=0; i<slayers.size(); ++i) {
		int tmp0 = 0; int tmp1 = 0; int tmp2 = 0;
		for (size_t n=0; n<slayers.at(i).size(); ++n) {
			switch (slayers.at(i).at(n)) {
				case '0': ++tmp0; break;
				case '1': ++tmp1; break;
				case '2': ++tmp2; break;
				default: continue;
			}
		}
		if (tmp0 <= num_zero || num_zero == 0) {
			num_zero = tmp0;
			num_one = tmp1;
			num_two = tmp2;
			min_layer = i;
		}
	}
	std::cout << "minlayer: " << min_layer << ": " << slayers.at(min_layer) << std::endl;
	std::cout << "result 1: " << (num_one * num_two) << std::endl;

	std::string final = slayers.back();

	int i =0;
	for (auto it = slayers.rbegin(); it!= slayers.rend(); ++it) {
		for (size_t n=0; n<(*it).size(); ++n) {
			switch ((*it).at(n)) {
				case '0': final[n] = '0'; break;
				case '1': final[n] = '1'; break;
			}
		}
		++i;
	}
	std::cout << "result 2:  " << final << std::endl;
	std::cout << ""  << std::endl;

	for (size_t n=0; n<final.size(); ++n) {
		switch (final.at(n)) {
			case '0': std::cout << "█"; break;
			case '1': std::cout << "░"; break;
		}
		if (n == 24 || (n > 30 && n % 25 == 24) ) std::cout << "." << std::endl;
	}
}
