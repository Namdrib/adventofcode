#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/22

// numeric_limits<int>::max();

class rock {
public:
	int x, y;
	int gi, el, risk; // geologic index, erosion level

	char type; // rocks = '.', wet = '=', narrow = '|'

	// for part 2 path finding
	int f, g, h;

	rock() : rock(0, 0) {
		;
	}

	rock(int x, int y) : x(x), y(y) {
		gi = el = 0;
		type = '?';

		// part 2
		f = g = numeric_limits<int>::max();
		h = 0;
	}

	void set_heuristic(pii target) {
		h = manhattan_distance(x, y, target.first, target.second);
	}

	void set_cost() {
		f = g + h;
	}
};

class state {
public:
	int x, y, eq;

	state() : state(0, 0, 1) {
		;
	}

	state(pii &p) : state(p.first, p.second, 1) {
		;
	}

	state(pii &p, int eq) : state(p.first, p.second, eq) {
		;
	}

	state(int x, int y, int eq) : x(x), y(y), eq(eq) {
		;
	}

	const bool operator == (const state &a) const {
		return x == a.x && y == a.y && eq == a.eq;
	}

	const bool operator < (const state &a) const {
		if (x == a.x) {
			if (y == a.y) {
				return eq < a.eq;
			}
			return y < a.y;
		}
		return x < a.x;
	}

	const bool operator == (const pii &a) const {
		return x == a.first && y == a.second;
	}
};

// up, down, left, right
int dir_x[] = {0, 0, -1, 1};
int dir_y[] = {-1, 1, 0, 0};


// perform A* where the heuristic is manhattan distance
int pathfind(vector<vector<rock>> &grid, pii start, pii target) {

	// equipment
	// 0 = neither, 1 = torch, 2 = climbing

	const auto compare_state = [&grid](const state &a, const state &b) {
		return grid[a.y][a.x].f < grid[b.y][b.x].f;
	};

	vector<state> fringe; // need to know the equipment when at a location
	set<state> closed; // maybe revert to set<pii>

	fringe.push_back(state(start, 1)); // start w/ torch

	grid[start.second][start.first].f = 0;
	grid[start.second][start.first].g = 0;

	// set grid heuristics
	for (size_t i = 0; i < grid.size(); i++) {
		for (size_t j = 0; j < grid[0].size(); j++) {
			grid[i][j].set_heuristic(target);
		}
	}

	while (!fringe.empty()) {

		// sort by grid cost
		sort(all(fringe), compare_state);

		// get element with lowest cost
		state current = fringe.front();
		fringe.erase(fringe.begin());

		if (current == target) {
			if (current.eq != 1) {
				grid[target.second][target.first].f += 7;
			}
			return grid[target.second][target.first].f;
		}

		// for each direction
		for (int i = 0; i < 4; i++) {
			pii step = make_pair(current.x + dir_x[i], current.y + dir_y[i]);

			// out of bounds
			if (step.first < 0 || step.first >= (int) grid[0].size() ||
					step.second < 0 || step.second >= (int) grid.size()) {
				continue;
			}

			if (closed.count(state(step, current.eq))) {
				continue;
			}

			// for each tool
			for (int j = 0; j < 3; j++) {

				state neighbour(step, j);

				if (grid[neighbour.y][neighbour.x].risk == j) {
					continue;
				}

				// update costs (minutes)
				int step_cost = 1;

				// calculate cost (if any) of changing equipment
				if (j != current.eq) {
					step_cost += 7;
				}

				// apply cumulative and heuristic cost
				grid[neighbour.y][neighbour.x].g = grid[current.y][current.x].g + step_cost;
				grid[neighbour.y][neighbour.x].set_cost();

				if (find(all(fringe), neighbour) == fringe.end()) {
					fringe.push_back(neighbour);
				}
			}
		}

		closed.insert(current);
	}

	return numeric_limits<int>::max();
}

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

	// el, risk, type
	grid[y][x].el = (grid[y][x].gi + depth) % 20183;
	grid[y][x].risk = grid[y][x].el % 3;
	grid[y][x].type = ".=|"[grid[y][x].risk];
}

int solve(vs &input, bool part_two) {

	int depth = extract_nums_from(input[0])[0];
	vi temp_target = extract_nums_from(input[1]);
	pii target = make_pair(temp_target[0], temp_target[1]);

	// pii dim_limits = make_pair(max(1000, target.first + 1), max(1000, target.second + 1));
	pii dim_limits = make_pair(target.first + 100, target.second + 100);

	// build the grid
	vector<vector<rock>> grid;
	for (int i = 0; i < dim_limits.second; i++) {
		vector<rock> temp;
		for (int j = 0; j < dim_limits.first; j++) {
			temp.push_back(rock(j, i));
		}
		grid.push_back(temp);
	}

	// calculate attributes for each location
	for (size_t i = 0; i < grid.size(); i++) {
		for (size_t j = 0; j < grid[0].size(); j++) {
			calc_rock_attr(grid, j, i, depth, target);
		}
	}

	int out = 0;
	if (part_two) {

		// perform a* or dijkstras to work out the cost from 0,0 to target

		// on rocky, must use either climbing or torch
		// on wet, must use climbing or neither
		// on narrow, must use torch or neither
		out = pathfind(grid, make_pair(0, 0), target);
	}
	else {

		for (int i = 0; i <= target.second; i++) {
			for (int j = 0; j <= target.first; j++) {
				out += grid[i][j].risk;
			}
		}
	}

	return out;
}

int main() {
	vs input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
