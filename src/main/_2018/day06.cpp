#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/6

// return the number of n in v
int count_num_of(vector<vector<int>> &v, int n) {

	int out = 0;
	for (size_t i=0; i<v.size(); i++) {
		for (size_t j=0; j<v[i].size(); j++) {
			if (v[i][j] == n) {
				 out++;
			}
		}
	}
	return out;
}

int PART_TWO_DIST = 10000;

int solve(vector<pair<int, int>> input, bool part_two) {

	// locate min and max bounds of the area
	int minx, miny, maxx, maxy;
	minx = miny = numeric_limits<int>::max();
	maxx = maxy = numeric_limits<int>::min();
	for (auto p : input) {
		minx = min(minx, p.first);
		maxx = max(maxx, p.first);
		miny = min(miny, p.second);
		maxy = max(maxy, p.second);
	}

	if (part_two) {
		int out = 0;

		// for each area
		for (int i=miny; i<=maxy; i++) {
			for (int j=minx; j<=maxx; j++) {

				// cumulative distance from (j, i) to every point in input
				int cum_dist = accumulate(all(input), 0, [j, i](int a, pair<int, int> &b){
					return a + manhattan_distance(j, i, b.first, b.second);
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
		vector<vector<int>> labels;

		// for each area
		for (int i=miny; i<=maxy; i++) {
			vector<int> label_row;
			for (int j=minx; j<=maxx; j++) {

				// calculate distances from (j,i) to all other inputs
				// find the label that provides the closest distance
				int closest_label = -1;
				int closest_dist = numeric_limits<int>::max();
				bool duplicate = false;
				for (size_t k=0; k<input.size(); k++) {
					int dist = manhattan_distance(j, i, input[k].first, input[k].second);
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
		for (size_t i=0; i<input.size(); i++) {
			regions.insert(i);
		}
		for (size_t i=0; i<labels.size(); i++)
		{
			regions.erase(labels[i][0]);
			regions.erase(labels[i][labels[i].size()-1]);
		}
		for (size_t i=0; i<labels[0].size(); i++)
		{
			regions.erase(labels[0][i]);
			regions.erase(labels[labels.size()-1][i]);
		}

		// of all the valid areas, check largest area size, return that
		int largest_label_size = numeric_limits<int>::min();
		for (auto region : regions) {
			int label_size = count_num_of(labels, region);
			largest_label_size = max(largest_label_size, label_size);
		}
		return largest_label_size;
	}
	return 0;
}

int main() {
	vector<pair<int, int>> input;

	for (string line; getline(cin, line);)
	{
		size_t comma_pos = line.find(", ");
		int left = stoi(line.substr(0, comma_pos));
		int right = stoi(line.substr(comma_pos+1));
		input.push_back(make_pair(left, right));
	}

	// assert(solve("dabAcCaCBAcCcaDA", false) == 10);
	// assert(solve("dabAcCaCBAcCcaDA", true) == 4);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
