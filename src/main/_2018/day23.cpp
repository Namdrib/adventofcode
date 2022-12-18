#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/23

// numeric_limits<int>::max();

int solve(vvi &input, bool part_two) {

	vvi distances;
	vector<vb> in_range;
	for (const vi &a : input) {
		vi temp1;
		vb temp2;

		for (const vi &b : input) {
			int dist = manhattan_distance(vector<int>(a.begin(), a.begin()+3), vector<int>(b.begin(), b.begin()+3));
			temp1.push_back(dist);
			temp2.push_back(dist <= a[3]);
		}

		distances.push_back(temp1);
		in_range.push_back(temp2);
	}

	auto max_range_it = max_element(all(input), [](vi &a, vi &b){
		return a[3] < b[3];
	});
	int max_range = (*max_range_it)[3];
	cout << "max_range = " << max_range << endl;
	int max_range_index = distance(input.begin(), max_range_it);

	int out = 0;

	if (part_two) {

	}
	else {
		for (bool b : in_range[max_range_index]) {
			out += b;
		}
	}

	return out;
}

int main() {
	vs input = split_istream_per_line(cin);

	vvi bots;

	for (auto s : input) {
		bots.push_back(extract_nums_from(s));
	}

	cout << "Part 1: " << solve(bots, false) << endl;
	// cout << "Part 2: " << solve(bots, true) << endl;
}
