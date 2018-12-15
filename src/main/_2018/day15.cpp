#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/15

const regex input_regex("(\\d+) players; last marble is worth (\\d+) points");
smatch match;
// regex_search(thing, match, input_regex);

// up, left, right, down (reading order)
int delta_x[4] = {0, -1, 1, 0};
int delta_y[4] = {-1, 0, 0, 1};

class unit {
public:
	int ap;
	int hp;
	char c;

	int x, y;

	bool moved;

	unit() : unit('E') {

	}

	unit(char c) : unit(c, 0, 0) {
	}

	unit(char c, int x, int y) : unit(c, x, y, 3) {
	}

	unit(char c, int x, int y, int ap) : ap(ap), c(c), x(x), y(y) {
		hp = 200;

		moved = false;
	}

	// reading order
	friend const bool operator < (const unit &u1, const unit &u2) {
		if (u1.y == u2.y) {
			return u1.x < u2.x;
		}
		return u1.y < u2.y;
	}

	const bool operator == (const unit &u) const {
		return x == u.x && y == u.y;
	}
	const bool operator != (const unit &u) const {
		return !(*this == u);
	}
	const bool operator == (const pii &p) const {
		return x == p.first && y == p.second;
	}
	const bool operator != (const pii &p) const {
		return !(*this == p);
	}

	friend ostream& operator << (ostream &os, const unit &u) {
		os << u.c << "(" << u.hp << ") at " << u.x << "," << u.y;
		return os;
	}
};

bool unit_at(const vector<unit> &units, char c, int x, int y) {
	for (auto u : units) {
		if (u.x == x && u.y == y && u.c == c) {
			return true;
		}
	}
	return false;
}

vi get_dist(map<pii, pair<pii, int>> meta, pii state) {
	vi actions;

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

	map<pii, pair<pii, int>> meta;

	while (!fringe.empty()) {

		pii current = fringe.front();
		fringe.erase(fringe.begin());

		if (dest == current) {
			vi actions = get_dist(meta, current);
			reverse(all(actions));
			return actions;
		}

		if (src != current && (unit_at(units, src.c, current.first, current.second) || unit_at(units, dest.c, current.first, current.second))) {
			continue;
		}

		// for each direction in reading order
		for (int i = 0; i < 4; i++) {
			pii step = make_pair(current.first + delta_x[i], current.second + delta_y[i]);

			// out of bounds
			if (step.first < 0 || step.first >= field[0].size() || step.second < 0 || step.second >= field.size()) {
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
	int num_rounds = 0;
	int p_elves = count_if(all(units), [](unit a){return a.c == 'E';});
	int p_goblins = count_if(all(units), [](unit a){return a.c == 'G';});
	// run move/combat steps
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

			// if in range, no move, attack

			// check the closest targest for unit (by number of moves required)
			int min_distance_moves = min_element(all(units_in_range), [](pair<unit, vi> a, pair<unit, vi> b){
				return a.second.size() < b.second.size();
			})->second.size();
			// cout << "min_distance_moves from " << u << " is " << min_distance_moves << endl;

			// --- MOVING ---
			if (min_distance_moves > 1) {
				// consider squares in range
				// find the one with fewest steps (manhattan distance)
				// cannot move through walls or units (#, E, G)
				// ties broken in reading order
				// take a _single step_ in that direction
				// if multiple ways avail, take first in reading order

				vector<unit> nearest;
				for (auto p : units_in_range) {
					if (p.second.size() == min_distance_moves) {
						nearest.push_back(p.first);
					}
				}

				sort(all(nearest));

				int min_action = 4;
				for (auto near : nearest) {
					min_action = min(min_action, units_in_range[near][0]);
				}

				current_unit->x += delta_x[min_action];
				current_unit->y += delta_y[min_action];
			}

			// --- ATTACKING ---
			// determine all targest in range (adjacent)
			// if no targets, end turn
			// else attack target with lowest HP (ties broken by reading order)

			// deals damage == to attack power, reducing HP by that much
			// if HP <= 0, target dies, becomes .

			vector<unit*> attack_targets;
			for (size_t j = 0; j < units.size(); j++) {
				// same unit or same team
				if (i == j || current_unit->c == units[j].c) {
					continue;
				}

				if (manhattan_distance(current_unit->x, current_unit->y, units[j].x, units[j].y) == 1) {
					attack_targets.push_back(&(units[j]));
				}
			}

			if (attack_targets.empty()) {
				continue;
			}

			unit *target = *min_element(all(attack_targets), [](unit *a, unit *b){
				if (a->hp == b->hp) {
					return a < b;
				}
				return a->hp < b->hp;
			});

			target = &(*find(all(units), *target));

			target->hp -= current_unit->ap;
			if (target->hp <= 0) {
				int dist = distance(units.begin(), find(all(units), *target));
				units.erase(units.begin() + dist);
				if (dist <= i) i--;
			}


			int num_elves = count_if(all(units), [](unit a){return a.c == 'E';});
			int num_goblins = count_if(all(units), [](unit a){return a.c == 'G';});

			p_elves = num_elves;
			p_goblins = num_goblins;
			if (num_elves == 0 || num_goblins == 0) {
				if (i == units.size()-1) {
					num_rounds++;
				}
				goto end;
			}
		}
	}
	end: // lol

	int out = 0;
	out = accumulate(all(units), 0, [](int a, unit b) {
		return a + b.hp;
	});
	out *= (num_rounds);
	return out;
}

int solve(vs input, bool part_two) {

	int ap = part_two ? 4 : 3;
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

		int num_elves = count_if(all(units), [](unit a){return a.c == 'E';});

		out = battle(input_copy, units, part_two);

		int new_elves = count_if(all(units), [](unit a){return a.c == 'E';});

		if (part_two) {
			if (num_elves == new_elves) {
				cout << "required ap: " << ap << endl;
				return out;
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
