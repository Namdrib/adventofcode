#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/25

class star {
public:
	int w, x, y, z;

	star() : star(0, 0, 0, 0) {
		;
	}

	star(int w, int x, int y, int z) : w(w), x(x), y(y), z(z) {
		;
	}

	const bool operator < (const star &a) const {
		if (w == a.w) {
			if (x == a.x) {
				if (y == a.y) {
					return z < a.z;
				}
				return y < a.y;
			}
			return x < a.x;
		}
		return w < a.w;
	}

	const bool operator == (star &a) const {
		return w == a.w && x == a.x && y == a.y && z == a.z;
	}

	friend ostream& operator << (ostream &os, const star &a) {
		os << "[" << a.w << "," << a.x << "," << a.y << "," << a.z << "]";
		return os;
	}
};

int manhattan_distance_4d(int w1, int w2, int x1, int x2, int y1, int y2, int z1, int z2) {
	return abs(w2 - w1) + abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1);
}

// use a disjoint set data structure to hold each constellation
// once a star is found that merges multiple constellations,
// merge the sets together
int solve(vector<star> input, bool part_two)
{
	// keep track of all constellations
	// set<star> = constellation
	vector<set<star>> constellations;

	// initialise each star in its own constellation
	for (star s : input) {
		set<star> temp;
		temp.insert(s);
		constellations.push_back(temp);
	}

	// for each constellation
	for (size_t i = 0; i < constellations.size(); i++) {

		// for each other constellation
		for (size_t j = 0; j < constellations.size(); j++) {
			if (i == j) {
				continue;
			}

			// if any of the stars in con1 are in range of anything in con2
			// merge con2 into con1 and delete con2
			if (any_of(all(constellations[i]), [j, &constellations](const star &a) {
					for (star b : constellations[j]) {
						if (manhattan_distance_4d(a.w, b.w, a.x, b.x, a.y, b.y, a.z, b.z) <= 3) {
							return true;
						}
					}
					return false;
				})) {
				for (auto &it : constellations[j]) {
					constellations[i].insert(it);
				}

				auto it = constellations.erase(constellations.begin() + j);
				j = distance(constellations.begin(), it) - 1;
				if (i) {
					i--;
				}
			}
		}
	}

	return constellations.size();
}

int main() {
	vs input = split_istream_per_line(cin);
	vector<star> stars;

	for (auto &s : input) {
		vi a = extract_nums_from(s);
		stars.push_back(star(a[0], a[1], a[2], a[3]));
	}

	cout << "Part 1: " << solve(stars, false) << endl;
	// cout << "Part 2: " << solve(stars, true) << endl;
}
