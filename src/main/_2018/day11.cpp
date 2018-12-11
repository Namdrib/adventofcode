#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/11

int get_power(int x, int y, int grid_serial_number) {
	int rack = x + 10;
	int power = rack * y;
	power += grid_serial_number;
	power *= rack;
	int hundreds = (power / 100) % 10;
	return hundreds - 5;
}

// No output value
// Manually determine the correct output
string solve(int input, bool part_two) {

	// build 2d partial sums
	// row and column 0 are blank
	// remember to offset when doing calculations
	vector<vector<long>> grid(301, vector<long>(301, 0));

	for (size_t i = 1; i < grid.size(); i++) {
		for (size_t j = 1; j < grid.size(); j++) {
			int power = get_power(j-1, i-1, input);
			grid[i][j] = power + grid[i][j-1] + grid[i-1][j] - grid[i-1][j-1];
		}
	}

	long max_power = numeric_limits<long>::min();
	size_t max_power_size = 1;
	pair<size_t, size_t> coords;

	size_t start = (part_two ? 1 : 3);
	size_t end = (part_two ? grid.size()-1 : 3);
	for (size_t size = start; size <=end; size++) {
		for (size_t i = 0; i < grid.size() - size; i++) {
			for (size_t j = 0; j < grid[i].size() - size; j++) {

				long sum = grid[i][j] - grid[i][j+size] - grid[i+size][j] + grid[i+size][j+size];

				if (sum > max_power) {
					max_power = sum;
					max_power_size = size;
					coords = make_pair(j , i);
				}
			}
		}
	}

	stringstream ss;
	ss << coords.first << "," << coords.second;
	if (part_two) {
		ss << "," << max_power_size;
	}
	return ss.str();
}

int main() {
	int input;
	cin >> input;

	assert(get_power(3, 5, 8) == 4);
	assert(get_power(122, 79, 57) == -5);
	assert(get_power(217, 196, 39) == 0);
	assert(get_power(101, 153, 71) == 4);

	// part 1
	assert(solve(18, false) == "33,45");
	assert(solve(42, false) == "21,61");

	// part 2
	assert(solve(18, true) == "90,269,16");
	assert(solve(42, true) == "232,251,12");

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
