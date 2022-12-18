#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/13

// digits = \s*(-?\d+)
// const regex input_regex(R"(\s*(-?\d+))");
// smatch match;

// up, left, down, right;
const int delta_x[4] = {0, -1, 0, 1};
const int delta_y[4] = {-1, 0, 1, 0};

// <<x, y>, c>
map<pair<int, int>, char> arrows {
	{{ 0, -1}, '^'},
	{{-1,  0}, '<'},
	{{ 0,  1}, 'v'},
	{{ 1,  0}, '>'},
};

class cart {

public:
	size_t x, y;
	int intersect; // 0=left, 1=straight, 2=right, wraparound

	int direction;

	bool crashed;

	cart() : cart(0, 0) {
		;
	}

	cart(size_t x, size_t y) : cart(x, y, 0) {
		;
	}

	cart(size_t x, size_t y, int direction) : x(x), y(y), direction(direction) {
		intersect = 0;
		crashed = false;
	}

	const char print_direction() const {
		return (crashed) ? 'X' : arrows[make_pair(delta_x[direction], delta_y[direction])];
	}

	const bool operator == (const cart &c) const {
		return x == c.x && y == c.y;
	}

	// order by row then column
	friend const bool operator < (const cart &a, const cart &c) {
		if (a.y == c.y) {
			return a.x < c.x;
		}
		return a.y < c.y;
	}

	friend ostream& operator << (ostream &os, cart &c) {
		os << c.x << "," << c.y;
		return os;
	}

};

// returns true iff we should continue ticking next round
// returns false if there is a crash
bool tick(const vector<string> &input, vector<cart> &carts, bool part_two) {
	sort(all(carts));

	int num_carts = accumulate(all(carts), 0, [](int a, const cart &c){
		return a + !c.crashed;
	});

	if (num_carts <= 1) {
		return false;
	}
	for (auto it = carts.begin(); it != carts.end(); ++it) {

		// move current cart
		char track = input[it->y][it->x];
		switch (track) {
			case '+':
			case '-':
			case '|':
			case '/':
			case '\\':
				it->x += delta_x[it->direction];
				it->y += delta_y[it->direction];
				break;
			default:
				cerr << "bad track " << track << " at " << *it << endl;
				exit(1);
				break;
		}

		// rotate temp if arrive at turn or intersection
		char next = input[it->y][it->x];
		switch (next) {
			case '+':
				switch (it->intersect) {
					case 0:
						it->direction++;
						break;
					case 1:
						break;
					case 2:
						it->direction += 3;
						break;

					default:
						cerr << "bad intersect " << it->intersect << endl;
				}
				it->intersect = (it->intersect + 1) % 3;
				break;

			case '/':
				if (it->direction & 1) {
					it->direction++;
				}
				else {
					it->direction += 3;
				}
				break;

			case '\\':
				if (it->direction & 1) {
					it->direction += 3;
				}
				else {
					it->direction++;
				}
				break;
		}
		it->direction %= 4;

		// detect collision, if applicable
		for (auto it2 = carts.begin(); it2 != carts.end(); ++it2) {
			if (it == it2 || it->crashed || it2->crashed) {
				continue;
			}
			if (*it == *it2) {
				it->crashed = it2->crashed = true;

				if (!part_two) {
					return false;
				}
			}
		}
	}

	return true;
}

string solve(vector<string> input, bool part_two) {

	vector<string> input_copy(input);

	// build carts
	vector<cart> carts;
	for (size_t i=0; i<input.size(); i++) {
		for (size_t j=0; j<input[i].size(); j++) {
			char temp = input[i][j];
			int direction = -1;
			if (temp == '^') {
				direction = 0;
				input_copy[i][j] = '|';
			}
			else if (temp == '<') {
				direction = 1;
				input_copy[i][j] = '-';
			}
			else if (temp == 'v') {
				direction = 2;
				input_copy[i][j] = '|';
			}
			else if (temp == '>') {
				direction = 3;
				input_copy[i][j] = '-';
			}

			if (direction >= 0) {
				carts.push_back(cart(j, i, direction));
			}
		}
	}

	for (size_t i=0; tick(input_copy, carts, part_two); i++) {
		;
	}

	ostringstream oss;
	for (cart &c : carts) {
		if (part_two != c.crashed) {
			oss << c;
			break;
		}
	}

	return oss.str();
}

int main() {
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl; // not 113,78 or 106,86 or 55,40
	cout << "Part 2: " << solve(input, true) << endl;
}
