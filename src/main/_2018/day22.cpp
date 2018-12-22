#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/22

// numeric_limits<int>::max();

class rock {
public:
	int x, y;
	int gi, el; // geologic index, erosion level

	char type; // rocks = '.', wet = '=', narrow = '|'

	rock() : rock(0, 0) {
		;
	}

	rock(int x, int y) : x(x), y(y) {
		gi = el = 0;
		type = '?';
	}
};

int MOD = 20183;

void calc_rock_attr(vector<vector<rock>> &grid, int x, int y, int depth, const pii &target) {
	// gi
	if ((x == 0 && y == 0) || (x == target.first && y == target.second)) {
		grid[y][x].gi = 0;
	}
	else if (y == 0) {
		grid[y][x].gi = x * 16807;
	}
	else if (x == 0) {
		grid[y][x].gi = y * 48271;
	}
	else {
		grid[y][x].gi = grid[y-1][x].el * grid[y][x-1].el;
	}

	// el
	grid[y][x].el = (grid[y][x].gi + depth) % MOD;

	// type
	switch (grid[y][x].el % 3) {
		case 0:
			grid[y][x].type = '.';
			break;
		case 1:
			grid[y][x].type = '=';
			break;
		case 2:
			grid[y][x].type = '|';
			break;
	}
}

int solve(vs &input, bool part_two) {

	int depth = extract_nums_from(input[0])[0];
	vi temp_target = extract_nums_from(input[1]);
	pii target = make_pair(temp_target[0], temp_target[1]);

	// mouth = 'M', target = 'T'
	vector<vector<rock>> grid;
	for (size_t i = 0; i <= target.second; i++) {
		vector<rock> temp;
		for (size_t j = 0; j <= target.first; j++) {
			temp.push_back(rock(j, i));
		}
		grid.push_back(temp);
	}

	for (size_t i = 0; i < grid.size(); i++) {
		for (size_t j = 0; j < grid[0].size(); j++) {
			calc_rock_attr(grid, j, i, depth, target);
		}
	}

	for (auto row : grid) {
		for (auto r : row) {
			cout << r.type;
		}
		cout << endl;
	}


	int out = 0;
	if (part_two) {

	}
	else {

		for (size_t i = 0; i <= target.second; i++) {
			for (size_t j = 0; j <= target.first; j++) {
				out += grid[i][j].el % 3;
			}
		}
	}

	return out;
}

int main() {
	vs input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	// cout << "Part 2: " << solve(input, true) << endl;
}
