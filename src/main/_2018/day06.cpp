#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/6

int PART_TWO_DIST = 10000;

int solve(vvi input, bool part_two) {

	// locate min and max bounds of the area
	int minx, miny, maxx, maxy;
	minx = miny = numeric_limits<int>::max();
	maxx = maxy = numeric_limits<int>::min();
	for (auto p : input) {
		minx = min(minx, p[0]);
		maxx = max(maxx, p[0]);
		miny = min(miny, p[1]);
		maxy = max(maxy, p[1]);
	}

	if (part_two) {
		int out = 0;

		// for each area
		for (int i = miny; i <= maxy; i++) {
			for (int j = minx; j <= maxx; j++) {
				vi temp = {j, i};

				// cumulative distance from (j, i) to every point in input
				int cum_dist = accumulate(all(input), 0, [temp](int a, vi &b) {
					return a + manhattan_distance(temp, b);
				});

				if (cum_dist < PART_TWO_DIST) {
					out++;
				}
			}
		}

		return out;
	}
	else {
		// labels[x][y] = 1 means position x, y belongs to input[1]
		vvi labels;

		// for each area
		for (int i = miny; i <= maxy; i++) {
			vi label_row;
			for (int j = minx; j <= maxx; j++) {
				vi temp = {j, i};

				// calculate distances from (j,i) to all other inputs
				// find the label that provides the closest distance
				int closest_label = -1;
				int closest_dist = numeric_limits<int>::max();
				bool duplicate = false;
				for (size_t k = 0; k < input.size(); k++) {
					int dist = manhattan_distance(temp, input[k]);
					if (dist < closest_dist) {
						closest_dist = dist;
						closest_label = k;
						duplicate = false;
					}
					else if (dist == closest_dist) {
						duplicate = true;
					}
				}

				label_row.push_back(duplicate ? -1 : closest_label);
			}
			labels.push_back(label_row);
		}

		// don't count any that touch the edges - they are infinite
		set<int> regions;
		for (size_t i = 0; i < input.size(); i++) {
			regions.insert(i);
		}
		for (size_t i = 0; i < labels.size(); i++) {
			regions.erase(labels[i][0]);
			regions.erase(labels[i][labels[i].size()-1]);
		}
		for (size_t i = 0; i < labels[0].size(); i++) {
			regions.erase(labels[0][i]);
			regions.erase(labels[labels.size()-1][i]);
		}

		// of all the valid areas, check largest area size, return that
		int largest_label_size = numeric_limits<int>::min();
		for (auto region : regions) {
			// count the num appearances of region in labels
			int label_size = accumulate(all(labels), 0, [region](int a, const vi &b) {
				return a + count(all(b), region);
			});
			largest_label_size = max(largest_label_size, label_size);
		}
		return largest_label_size;
	}
	return 0;
}

int main() {
	vvi input;

	for (string line; getline(cin, line);) {
		size_t comma_pos = line.find(", ");
		int left = stoi(line.substr(0, comma_pos));
		int right = stoi(line.substr(comma_pos+1));
		input.push_back(vector<int>{left, right});
	}

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
