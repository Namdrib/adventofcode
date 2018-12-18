#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/18

// count the number of c immediately around in[y][x] in all 8 directions
int count_around(const vs &in, int x, int y, char c) {

	int out = 0;

	for (int i = -1; i <= 1; i++) {
		for (int j = -1; j <= 1; j++) {
			if (i == 0 && j == 0) continue;

			if (y+i < 0 || y+i >= (int) in.size()
					|| x+j < 0 || x+j >= (int) in[y].size()) {
				continue;
			}

			if (in[y+i][x+j] == c) {
				out++;
			}

		}
	}

	return out;
}

vs tick(const vs &in) {

	vs out(in);

	for (size_t i = 0; i < in.size(); i++) {
		for (size_t j = 0; j < in.size(); j++) {

			int num_trees = count_around(in, j, i, '|');
			int num_lumber = count_around(in, j, i, '#');

			switch (in[i][j]) {
				case '.':
					if (num_trees >= 3) {
						out[i][j] = '|';
					}
					break;
				case '|':
					if (num_lumber >= 3) {
						out[i][j] = '#';
					}
					break;
				case '#':
					if (num_lumber < 1 || num_trees < 1) {
						out[i][j] = '.';
					}
					break;
			}
		}
	}

	return out;
}

int solve(vs input, bool part_two) {
	int PART_TWO_TICKS = 1000000000;

	vs grid(input);

	// keep track of which states we have seen
	// use to determine whether loops occur
	map<vs, int> seen_states;

	int loop_start = -1, loop_length = -1;
	int i;
	for (i = 0; i < (part_two ? PART_TWO_TICKS : 10); i++) {
		grid = tick(grid);

		// if we have seen a state before, we will cycle
		// record the cycle start and its length
		if (seen_states.count(grid) > 0) {

			if (loop_start == -1) {
				loop_start = seen_states[grid];
				loop_length = i - loop_start;
				i++;
				break;
			}
		}
		seen_states[grid] = i;
	}

	// for part two, perform PART_TWO_TICKS ticks
	if (part_two) {
		// skip a bunch of complete loops
		int num_complete_loops = (PART_TWO_TICKS - i) / loop_length;
		i += (num_complete_loops * loop_length);

		for (; i < PART_TWO_TICKS; i++) {
			grid = tick(grid);
		}
	}

	// count wood and lumber
	int num_wood = 0, num_lumber = 0;
	for (auto s : grid) {
		for (auto c : s) {
			if (c == '|') {
				num_wood++;
			}
			else if (c == '#') {
				num_lumber++;
			}
		}
	}

	return num_lumber * num_wood;
}

int main() {
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
