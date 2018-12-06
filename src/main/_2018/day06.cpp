#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2018/day/6

int manhattan_distance(int x1, int y1, int x2, int y2)
{
	return abs(x1 - x2) + abs(y1 - y2);
}

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

	int minx, miny, maxx, maxy;
	minx = miny = numeric_limits<int>::max();
	maxx = maxy = numeric_limits<int>::min();
	for (auto p : input) {
		minx = min(minx, p.first);
		maxx = max(maxx, p.first);
		miny = min(miny, p.second);
		maxy = max(maxy, p.second);
	}

	vector<vector<int>> labels; // labels[x][y] = 1 means position x, y belongs to input[1]

	if (part_two) {
		set<pair<int, int>> region;

		// for each area
		for (int i=miny; i<=maxy; i++) {
			vector<int> label_row;
			for (int j=minx; j<=maxx; j++) {

				int dist_to_all = 0;
				for (auto p : input) {
					dist_to_all += manhattan_distance(j, i, p.first, p.second);
				}
				if (dist_to_all < PART_TWO_DIST) {
					region.insert(make_pair(j, i));
				}
			}
		}

		cout << region << endl;

		return region.size();
	}
	else {
		// for each area
		for (int i=miny; i<=maxy; i++) {
			vector<int> label_row;
			for (int j=minx; j<=maxx; j++) {

				// find closest match, or -1 if none
				vector<int> distances;
				int closest_dist = numeric_limits<int>::min();
				int closest_label;
				for (size_t k=0; k<input.size(); k++) {
					int dist = manhattan_distance(j, i, input[k].first, input[k].second);
					distances.push_back(dist);
				}

				closest_dist = *min_element(all(distances));
				bool got = false;
				bool duplicate = false;
				for (size_t k=0; k<distances.size(); k++) {
					if (distances[k] == closest_dist) {
						if (got == true) {
							duplicate = true;
							break;
						}
						closest_label = k;
						got = true;
					}
				}

				if (duplicate) {
					label_row.push_back(-1);
				}
				else {
					label_row.push_back(closest_label);
				}
			}
			labels.push_back(label_row);
		}

		for (auto label : labels) {
			cout << label << endl;
		}

		// don't count any that touch the edges
		set<int> dont_count;
		for (size_t i=0; i<labels.size(); i++)
		{
			dont_count.insert(labels[i][0]);
			dont_count.insert(labels[i][labels[i].size()-1]);
		}
		for (size_t i=0; i<labels[0].size(); i++)
		{
			dont_count.insert(labels[0][i]);
			dont_count.insert(labels[labels.size()-1][i]);
		}

		cout << "dont count " << dont_count << endl;

		int largest_label;
		int largest_label_size = numeric_limits<int>::min();
		for (int i=0; i<input.size(); i++) {
			if (dont_count.count(i) == 0) {
				int label_size = count_num_of(labels, i);
				if (label_size > largest_label_size) {
					largest_label_size = label_size;
					largest_label = i;
				}
			}
		}

		return largest_label_size;
		// size of largest non-infinite area

	}
	return 0;
}

int main() {
	// string input;
	// ifstream ifs("src/test/_2018/day06_01.in");
	// if (!ifs.is_open())
	// {
	// 	cout << "not open" << endl;
	// }
	vector<pair<int, int>> input;

	for (string line; getline(cin, line);)
	{
		size_t comma_pos = line.find(", ");
		int left = stoi(line.substr(0, comma_pos));
		int right = stoi(line.substr(comma_pos+1));
		cout << "l,r:" << left << "," << right << endl;
		input.push_back(make_pair(left, right));
	}

	// assert(solve("dabAcCaCBAcCcaDA", false) == 10);
	// assert(solve("dabAcCaCBAcCcaDA", true) == 4);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
