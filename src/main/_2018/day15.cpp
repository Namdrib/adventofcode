#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/15

// up, left, right, down (reading order)
int delta_x[4] = {0, -1, 1, 0};
int delta_y[4] = {-1, 0, 0, 1};

class unit {
public:
	int ap;
	int hp;
	char c;

	int x, y;

	unit() : unit('E') {

	}

	unit(char c) : unit(c, 0, 0) {
	}

	unit(char c, int x, int y) : unit(c, x, y, 3) {
	}

	unit(char c, int x, int y, int ap) : ap(ap), c(c), x(x), y(y) {
		hp = 200;
	}

	void move_by(int dx, int dy) {
		x += dx;
		y += dy;
	}

	// reading order
	friend const bool operator < (const unit &a, const unit &b) {
		if (a.y == b.y) {
			return a.x < b.x;
		}
		return a.y < b.y;
	}

	const bool operator == (const unit &a) const {
		return x == a.x && y == a.y;
	}
	const bool operator != (const unit &a) const {
		return !(*this == a);
	}
	const bool operator == (const pii &a) const {
		return x == a.first && y == a.second;
	}
	const bool operator != (const pii &a) const {
		return !(*this == a);
	}

	friend ostream& operator << (ostream &os, const unit &u) {
		os << u.c << "(" << u.hp << ") at " << u.x << "," << u.y;
		return os;
	}
};

// returns true if there is a unit at (x,y), with faction c
bool unit_at(const vector<unit> &units, char c, int x, int y) {
	return any_of(all(units), [c, x, y](unit a){
		return a.c == c && a.x == x && a.y == y;
	});
}

vi get_dist(map<pii, pair<pii, int>> meta, pii state) {
	vi actions;

	// trace back from dest to source
	while (meta.count(state)) {
		auto temp = meta[state];
		state = temp.first;
		actions.push_back(temp.second);
	}

	return actions;
}

// use bfs to determine distance from src to dest (there is an open path)
// if there is no open path, return -1
// return that distance
vi distance_to(const vs &field, const vector<unit> &units, const unit &src, const unit &dest) {

	vector<pii> fringe;
	set<pii> closed;

	fringe.push_back(make_pair(src.x, src.y));

	// <state, <parent, direction>>
	map<pii, pair<pii, int>> meta;

	while (!fringe.empty()) {

		pii current = fringe.front();
		fringe.erase(fringe.begin());

		if (dest == current) {
			vi actions = get_dist(meta, current);
			reverse(all(actions));
			return actions;
		}

		if (src != current && (unit_at(units, src.c, current.first, current.second) ||
				unit_at(units, dest.c, current.first, current.second))) {
			continue;
		}

		// for each direction in reading order
		for (int i = 0; i < 4; i++) {
			pii step = make_pair(current.first + delta_x[i], current.second + delta_y[i]);

			// out of bounds
			if (step.first < 0 || step.first >= (int) field[0].size() ||
					step.second < 0 || step.second >= (int) field.size()) {
				continue;
			}

			// can't walk through walls
			if (field[step.second][step.first] == '#') {
				continue;
			}

			if (unit_at(units, src.c, step.first, step.second)) {
				continue;
			}

			if (closed.count(step)) {
				continue;
			}

			if (find(all(fringe), step) == fringe.end()) {
				fringe.push_back(step);
				meta[step] = make_pair( make_pair(current.first, current.second), i );
			}
		}
		closed.insert(current);
	}

	return vi();
}


int battle(const vs &input, vector<unit> &units, bool part_two) {
	// run move/combat steps
	int num_rounds = 0;
	for (;; num_rounds++) {
		sort(all(units));

		// every unit
		for (size_t i = 0; i < units.size(); i++) {
			unit *current_unit = &(units[i]);

			// identify other units with adjacent squares next to them
			// and moves required to get to that unit
			// empty vector if cannot get to them
			map<unit, vi> units_in_range;
			for (size_t j = 0; j < units.size(); j++) {
				// same unit or same team
				if (i == j || current_unit->c == units[j].c) {
					continue;
				}

				// compute moves, store them
				vi moves = distance_to(input, units, *current_unit, units[j]);
				if (!moves.empty()) {
					units_in_range[units[j]] = moves;
				}
			}

			// cannot get to anyone, end turn
			if (units_in_range.empty()) {
				continue;
			}


			// check the closest targest for unit (by number of moves required)
			const size_t min_distance_moves = min_element(all(units_in_range),
					[](const pair<unit, vi> &a, const pair<unit, vi> &b){
				return a.second.size() < b.second.size();
			})->second.size();

			// --- MOVING ---
			// if in range, don't move, just attack
			if (min_distance_moves > 1) {
				// consider squares in range
				// find the one with fewest steps (manhattan distance)
				// cannot move through walls or units (#, E, G)
				// ties broken in reading order
				// take a _single step_ in that direction
				// if multiple ways avail, take first in reading order

				set<unit> nearest;
				for (auto p : units_in_range) {
					if (p.second.size() == min_distance_moves) {
						nearest.insert(p.first);
					}
				}

				unit nearest_unit = *min_element(all(nearest),
						[&units_in_range](const unit &a, const unit &b){
					return units_in_range.at(a)[0] < units_in_range.at(b)[0];
				});
				int min_action = units_in_range[nearest_unit][0];

				current_unit->move_by(delta_x[min_action], delta_y[min_action]);
			}

			// --- ATTACKING ---

			// determine all targest in range (adjacent)
			vector<unit> attack_targets;
			for (size_t j = 0; j < units.size(); j++) {
				// same unit or same team
				if (i == j || current_unit->c == units[j].c) {
					continue;
				}

				if (manhattan_distance(current_unit->x, current_unit->y, units[j].x, units[j].y) == 1) {
					attack_targets.push_back(units[j]);
				}
			}

			// no targets, end turn
			if (attack_targets.empty()) {
				continue;
			}

			// attack target with lowest HP (ties broken by reading order)
			auto target_it = min_element(all(attack_targets),
					[](const unit &a, const unit &b){
				if (a.hp == b.hp) {
					return a < b;
				}
				return a.hp < b.hp;
			});

			// find the target in units
			// this is necessary since we are potentially deleting it from units
			target_it = find(all(units), *target_it);

			// deals damage == to AP, reducing HP by that much
			// if HP <= 0, target dies
			target_it->hp -= current_unit->ap;
			if (target_it->hp <= 0) {
				size_t dist = distance(units.begin(), target_it);
				units.erase(units.begin() + dist);
				if (dist <= i) i--;
			}

			// end the loop when no targets left
			int num_elves = count_if(all(units), [](const unit &a){return a.c == 'E';});
			int num_goblins = count_if(all(units), [](const unit &a){return a.c == 'G';});
			if (num_elves == 0 || num_goblins == 0) {
				if (i == units.size() - 1) {
					num_rounds++;
				}
				goto end;
			}
		}
	}
	end: // lol

	int out = accumulate(all(units), 0, [](int a, unit b) {
		return a + b.hp;
	});
	out *= (num_rounds);
	return out;
}

int solve(vs input, bool part_two) {

	int ap = 3;
	int out = 0;
	do {
		// build units
		vector<unit> units;
		vs input_copy = input;
		for (size_t i = 0; i < input_copy.size(); i++) {
			for (size_t j = 0; j < input_copy[i].size(); j++) {
				if (input_copy[i][j] == 'G') {
					units.push_back(unit(input_copy[i][j], j, i));
					input_copy[i][j] = '.';
				}
				else if (input_copy[i][j] == 'E') {
					units.push_back(unit(input_copy[i][j], j, i, ap));
					input_copy[i][j] = '.';
				}
			}
		}

		int p_elves = count_if(all(units), [](const unit &a){return a.c == 'E';});

		out = battle(input_copy, units, part_two);

		int new_elves = count_if(all(units), [](const unit &a){return a.c == 'E';});

		if (part_two) {
			// no elves died
			if (p_elves == new_elves) {
				break;
			}
		}
		ap++;
	} while (part_two);

	return out;
}

int main() {
	vs input = split_istream_per_line(cin);

	// examples
	vs e0 = {
		"#######",
		"#.G...#",
		"#...EG#",
		"#.#.#G#",
		"#..G#E#",
		"#.....#",
		"#######",
	};

	vs e1 = {
		"#######",
		"#G..#E#",
		"#E#E.E#",
		"#G.##.#",
		"#...#E#",
		"#...E.#",
		"#######",
	};

	vs e2 = {
		"#######",
		"#E..EG#",
		"#.#G.E#",
		"#E.##E#",
		"#G..#.#",
		"#..E#.#",
		"#######",
	};

	vs e3 = {
		"#######",
		"#E.G#.#",
		"#.#G..#",
		"#G.#.G#",
		"#G..#.#",
		"#...E.#",
		"#######",
	};

	vs e4 = {
		"#######",
		"#.E...#",
		"#.#..G#",
		"#.###.#",
		"#E#G#G#",
		"#...#G#",
		"#######",
	};

	vs e5 = {
		"#########",
		"#G......#",
		"#.E.#...#",
		"#..##..G#",
		"#...##..#",
		"#...#...#",
		"#.G...G.#",
		"#.....G.#",
		"#########",
	};

	assert(solve(e0, false) == 27730);
	assert(solve(e1, false) == 36334);
	assert(solve(e2, false) == 39514);
	assert(solve(e3, false) == 27755);
	assert(solve(e4, false) == 28944);
	assert(solve(e5, false) == 18740);

	assert(solve(e0, true) == 4988); // 15 power
	assert(solve(e2, true) == 31284); // 4 power
	assert(solve(e3, true) == 3478); // 15 power
	assert(solve(e4, true) == 6474); // 12 power
	assert(solve(e5, true) == 1140); // 34 power


	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl; // 17 power
}
