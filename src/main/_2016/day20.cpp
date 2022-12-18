#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/20

// assume blocked_ranges is sorted by first, then by second
// "merge" adjacent and overlapping ranges
// something like:
// {<1, 3>, <2, 4>, <4, 5>, <6, 7>, <9, 10>}
// becomes {<1, 7>, <9, 10>}
// - the 3 and 2 overlap
// - the 4 and 4 touch
// - the 5 and 6 are adjacent
size_t solve(const vector<pair<size_t, size_t>> &blocked_ranges, bool part_two) {
	size_t blocked = 0;
	vector<pair<size_t, size_t>> collapsed_ranges;

	pair<size_t, size_t> temp = blocked_ranges.front();

	for (size_t i = 0; i < blocked_ranges.size(); i++) {
		auto p = blocked_ranges[i];
		// they overlap
		if (p.first <= temp.second + 1) {
			temp.second = max(temp.second, p.second);
		}
		else {
			blocked += p.first - (temp.second + 1);
			collapsed_ranges.push_back(temp);
			if (i < blocked_ranges.size() - 1) {
				temp = blocked_ranges[i];
			}
		}
	}
	collapsed_ranges.push_back(temp);

	if (part_two) {
		return blocked;
	}
	return collapsed_ranges[0].second + 1;
}

int main() {
	// take input in pairs of numbers
	vector<pair<size_t, size_t>> blocked_ranges;
	for (string temp; getline(cin, temp);) {
		size_t a, b;
		sscanf(temp.c_str(), "%zu-%zu", &a, &b); // rip using c code
		blocked_ranges.push_back(make_pair(a, b));
	}

	// size_t max_ip = 9;
	size_t max_ip = 4294967295;
	blocked_ranges.push_back(make_pair(max_ip, max_ip));

	// sorting makes it easier to traverse the numbers
	// when looking for the minimum
	sort(all(blocked_ranges));

	cout << "Part 1: " << solve(blocked_ranges, false) << endl;
	cout << "Part 2: " << solve(blocked_ranges, true) << endl;
}
