#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/25

class star {
public:
	// int w, x, y, z;
	vector<int> coords;

	star() : star(0, 0, 0, 0) {
		;
	}

	star(int w, int x, int y, int z) {
		coords.clear();
		coords.push_back(w);
		coords.push_back(x);
		coords.push_back(y);
		coords.push_back(z);
	}

	star(vector<int> &v) : coords(v) {
		;
	}

	const bool operator < (const star &a) const {
		return coords < a.coords;
	}

	const bool operator == (star &a) const {
		return coords == a.coords;
	}

	friend ostream& operator << (ostream &os, const star &a) {
		os << "[" << a.coords << "]";
		return os;
	}
};

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
						if (manhattan_distance(a.coords, b.coords) <= 3) {
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
		stars.push_back(star(a));
	}

	cout << "Part 1: " << solve(stars, false) << endl;
	// cout << "Part 2: " << solve(stars, true) << endl;
}
