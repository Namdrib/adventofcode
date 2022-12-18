#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/17

int spring_x = 500;
int spring_y = 0;

pii x_bounds = make_pair(500, 500);
pii y_bounds = make_pair(numeric_limits<int>::max(), numeric_limits<int>::min());


// setters and getters offsetting by min bounds
void set_grid(vs &grid, int x, int y, char c) {
	grid.at(y - y_bounds.first)[x - x_bounds.first] = c;
}

char get_grid(vs &grid, int x, int y) {
	return grid.at(y - y_bounds.first)[x - x_bounds.first];
}

// dir == 0 for left, == 1 for right
bool has_wall(vs &grid, int x, int y, bool dir) {

	if (y >= y_bounds.second) {
		return false;
	}

	while (true) {

		if (x <= x_bounds.first) {
			return false;
		}

		char thing = get_grid(grid, x, y);
		if (thing == '.') {
			return false;
		}
		if (thing == '#') {
			return true;
		}

		x += (dir) ? -1 : 1;
	}
}

// dir == 0 for left, == 1 for right
void fill_water(vs &grid, int x, int y, bool dir) {

	if (y >= y_bounds.second) {
		return;
	}

	while (true) {

		if (x <= x_bounds.first) {
			return;
		}

		if (get_grid(grid, x, y) == '#' || get_grid(grid, x, y) == '.') {
			return;
		}
		set_grid(grid, x, y, '~');

		x += (dir) ? -1 : 1;
	}
}

// fill the grid with water starting from position x, y
void fill(vs &grid, int x, int y) {

	// out of bounds
	if (y >= y_bounds.second) {
		return;
	}

	// move down
	if (get_grid(grid, x, y + 1) == '.') {
		set_grid(grid, x, y + 1, '|');
		fill(grid, x, y + 1);
	}

	// can't go down any further
	char below = get_grid(grid, x, y + 1);
	if (below == '~' || below == '#') {
		// expand left
		if (get_grid(grid, x - 1, y) == '.') {
			set_grid(grid, x - 1, y, '|');
			fill(grid, x - 1, y);
		}

		// expand right
		if (get_grid(grid, x + 1, y) == '.') {
			set_grid(grid, x + 1, y, '|');
			fill(grid, x + 1, y);
		}
	}

	// turn '|' into '~' if the water is walled on both sides
	if (has_wall(grid, x, y, 0) && has_wall(grid, x, y, 1)) {
		fill_water(grid, x, y, 0);
		fill_water(grid, x, y, 1);
	}
}

int solve(vector<string> input, bool part_two) {


	vector<vector<int>> nums;
	vector<bool> x_first;
	for (string s : input) {
		nums.push_back(extract_nums_from(s));
		x_first.push_back(s[0] == 'x');
	}

	// first pass to determine bounds
	for (size_t i=0; i<nums.size(); i++) {
		pii *fixed = &((x_first[i]) ? x_bounds : y_bounds);
		pii *moving = &((x_first[i]) ? y_bounds : x_bounds);

		fixed->first = min(fixed->first, nums[i][0]);
		fixed->second = max(fixed->second, nums[i][0]);

		moving->first = min(moving->first, nums[i][1]);
		moving->second = max(moving->second, nums[i][2]);
	}
	x_bounds.first--;
	x_bounds.second++;

	// save min_y since output requires counting from the
	// lowest y that appears in input values
	// however the spring_y == 0
	int min_y, max_y;
	min_y = y_bounds.first;
	max_y = y_bounds.second;

	y_bounds.first = min(y_bounds.first, spring_y);

	// second pass to build the grid
	vector<string> grid(y_bounds.second - y_bounds.first + 1, string(x_bounds.second - x_bounds.first + 1, '.'));
	for (size_t i = 0; i < nums.size(); i++) {
		for (size_t j = nums[i][1]; j <= nums[i][2]; j++) {
			int y = ((x_first[i]) ? j : nums[i][0]);
			int x = ((x_first[i]) ? nums[i][0] : j);
			set_grid(grid, x, y, '#');
		}
	}
	set_grid(grid, spring_x, spring_y, '+');

	// now actually do work
	// simulate water dripping until overflow

	fill(grid, spring_x, spring_y);

	// calculate output values
	int num_resting = 0, num_reach = 0;

	for (size_t i = min_y; i <= max_y; i++) {

		for (char c : grid[i]) {
			if (c == '~') {
				num_resting++;
			}
			else if (c == '|') {
				num_reach++;
			}
		}
	}

	return num_resting + ((part_two) ? 0 : num_reach);
}

int main() {
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
