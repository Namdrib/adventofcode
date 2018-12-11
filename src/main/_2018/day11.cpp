#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/11

long get_power(int x, int y, int grid_serial_number) {
	long rack = x + 10;
	long power = rack * y;
	power += grid_serial_number;
	power *= rack;
	long hundreds = (power / 100) % 10;
	return hundreds-5;
}

// No output value
// Manually determine the correct output
string solve(int input, bool part_two) {

	vector<vector<int>> grid(300, vector<int>(300, -1));

	long max_power = numeric_limits<long>::min();
	size_t max_power_size = 1;
	pair<size_t, size_t> coords;

	for (size_t size = 1; size <= grid.size(); size++) {

		// for each starting position
		for (size_t i=0; i<grid.size()-size; i++) {
			for (size_t j=0; j<grid[i].size()-size; j++) {

				// calculate the sum of the square starting at [i][j]
				long sum = 0;
				for (size_t y = 0; y < size; y++) {
					for (size_t x = 0; x < size; x++) {
						size_t destx = j + x;
						size_t desty = i + y;
						int *dest = &(grid[desty][destx]);
						if (*dest == -1) {
							*dest = get_power(j+x, i+y, input);
						}
						sum += *dest;
					}
				}
				if (sum > max_power) {
					max_power = sum;
					coords = make_pair(j, i);
					max_power_size = size;
				}
			}
		}
	}

	stringstream ss;
	ss << coords.first << "," << coords.second;
	if (part_two) {
		ss << "," << max_power_size;
	}
	cout << "returning " << ss.str() << endl;
	return ss.str();
}

int main() {
	int input;
	cin >> input;

	// assert(get_power(3, 5, 8) == 4);
	// assert(get_power(122, 79, 57) == -5);
	// assert(get_power(217, 196, 39) == 0);
	// assert(get_power(101, 153, 71) == 4);

	// part 1 (note x and y are reversed)
	// assert(solve(18, false) == "33,45");
	// assert(solve(42, false) == "21,61");

	assert(solve(18, true) == "90,269,16");
	assert(solve(42, true) == "232,251,12");

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
