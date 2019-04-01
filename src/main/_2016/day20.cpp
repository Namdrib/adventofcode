#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// assume blocked_ranges has already been sorted by first then by second (if aplicable)
int solve(const vector<pair<size_t, size_t>> &blocked_ranges, bool part_two) {
	size_t current = 0;

	for (size_t i = 0; i < blocked_ranges.size(); i++) {

		if (current >= blocked_ranges[i].first && current <= blocked_ranges[i].second) {
			current = blocked_ranges[i].second + 1;

			if (i < blocked_ranges.size() - 1 && blocked_ranges[i+1].first > current) {
				return current;
			}
		}
	}

	return current;
}

int main() {
	// take input in pairs of numbers
	vector<pair<size_t, size_t>> blocked_ranges;
	for (string temp; getline(cin, temp);) {
		size_t a, b;
		sscanf(temp.c_str(), "%zu-%zu", &a, &b); // rip using c code
		blocked_ranges.push_back(make_pair(a, b));
	}

	// sorting makes it easier to traverse the numbers
	// when looking for the minimum
	sort(all(blocked_ranges));

	cout << "Part 1: " << solve(blocked_ranges, false) << endl;
}
