#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2016/day/18

string do_next_row(string in) {
	string out;

	for (size_t i = 0; i < in.size(); i++) {

		bool left_trap = (i >= 0 && in[i-1] == '^');
		bool right_trap = i < in.size() - 1 && in[i+1] == '^';
		bool centre_trap = in[i] == '^';

		if ((left_trap && centre_trap && !right_trap)
			|| (left_trap && !centre_trap && !right_trap)
			|| (!left_trap && centre_trap && right_trap)
			|| (!left_trap && !centre_trap && right_trap)) {
			out += "^";
		}
		else {
			out += ".";
		}
	}

	return out;
}

int solve(string input, int size, bool part_two) {

	vs grid;
	grid.push_back(input);

	// grow the thing
	while (grid.size() < size) {
		string next_row = do_next_row(grid.back());
		grid.push_back(next_row);
	}

	// cout << grid[0].size() << "x" << grid.size() << endl;
	// for (auto s : grid) {
	// 	cout << s << endl;
	// } cout << endl;

	// count safe tiles
	int out = 0;
	for (auto s : grid) {
		for (size_t i = 0; i < s.size(); i++) {
			if (s[i] == '.') {
				out++;
			}
		}
	}
	return out;
}

int main()
{
	string input;
	cin >> input;

	assert(do_next_row("..^^.") == ".^^^^");
	assert(do_next_row(".^^^^") == "^^..^");
	assert(do_next_row(".^^.^.^^^^") == "^^^...^..^");
	assert(do_next_row("^^^^..^^^.") == "^..^^^^.^^");
	assert(do_next_row(".^^^..^.^^") == "^^.^^^..^^");

	assert(solve(".^^.^.^^^^", 10, false) == 38);

	cout << "Part 1: " << solve(input, 40, false) << endl; // 4892 too high
	cout << "Part 2: " << solve(input, 400000, true) << endl;
}

/*

Then, starting with the row ..^^., you can determine the next row by applying those rules to each new tile:

The leftmost character on the next row considers the left (nonexistent, so we assume "safe"), center (the first ., which means "safe"), and right (the second ., also "safe") tiles on the previous row. Because all of the trap rules require a trap in at least one of the previous three tiles, the first tile on this new row is also safe, ..
The second character on the next row considers its left (.), center (.), and right (^) tiles from the previous row. This matches the fourth rule: only the right tile is a trap. Therefore, the next tile in this new row is a trap, ^.
The third character considers .^^, which matches the second trap rule: its center and right tiles are traps, but its left tile is not. Therefore, this tile is also a trap, ^.
The last two characters in this new row match the first and third rules, respectively, and so they are both also traps, ^.

*/
