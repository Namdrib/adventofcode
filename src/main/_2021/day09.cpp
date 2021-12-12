#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/9

const array<int, 4> dy = {-1, 1, 0, 0};
const array<int, 4> dx = {0, 0, -1, 1};

// a low point is defined as a location that is lower than all of its adjacaent locations
// not includinng diagonals
vector<pair<int, int>> get_all_low_points(const vector<vector<int>> &in)
{
	vector<pair<int, int>> out;

	// for each point
	for (size_t i = 0; i < in.size(); i++)
	{
		for (size_t j = 0; j < in[i].size(); j++)
		{
			// for each neighbour
			if (i != 0)
			{
				if (in[i-1][j] <= in[i][j])
				{
					continue;
				}
			}
			if (i < in.size() - 1)
			{
				if (in[i+1][j] <= in[i][j])
				{
					continue;
				}
			}
			if (j != 0)
			{
				if (in[i][j-1] <= in[i][j])
				{
					continue;
				}
			}
			if (j < in[i].size() - 1)
			{
				if (in[i][j+1] <= in[i][j])
				{
					continue;
				}
			}

			/* cout << "Low point at " << j << ", " << i << endl; */
			out.push_back(make_pair(i, j));
		}
	}

	return out;
}

// perform dfs on the heatmap, stopping at 9s
void get_basin_size(const vector<vector<int>> &heatmap, pair<int, int> current_point, set<pair<int, int>> &seen)
{
	// for each neighbour of the current point
	// if it is not seen, and it is not a 9, add it to the seen list

	int x = current_point.second;
	int y = current_point.first;

	// look in each direction of the current point
	for (size_t i = 0; i < dx.size(); i++)
	{
		int new_x = x + dx[i];
		int new_y = y + dy[i];

		// if it is in bounds
		if (new_y >= 0 && static_cast<size_t>(new_y) < heatmap.size() && new_x >= 0 && static_cast<size_t>(new_x) < heatmap[new_y].size())
		{
			auto target = make_pair(new_y, new_x);
			if (heatmap[new_y][new_x] != 9 && seen.find(target) == seen.end())
			{
				// add it to the current basin
				seen.insert(target);
				get_basin_size(heatmap, target, seen);
			}
		}
	}
}

// get the basin size for a specific low point
// using depth-first search, sprawl out until we hit 9s
size_t get_basin_size(const vector<vector<int>> &heatmap, pair<int, int> low_point)
{
	set<pair<int, int>> basin = {low_point};
	get_basin_size(heatmap, low_point, basin);
	return basin.size();
}

// find the risk sum of all low points in the heatmap
size_t part_one(const vector<vector<int>> &heatmap)
{
	auto all_low_points = get_all_low_points(heatmap);

	return accumulate(all(all_low_points), static_cast<size_t>(0),
			[&heatmap]
			(size_t acc, const pair<int, int> &low_point)
			{return acc + heatmap[low_point.first][low_point.second] + 1;}
	);
}

// find the product of the three largest basins
// where a basin is a location that eventually flows downward to a single low point
size_t part_two(const vector<vector<int>> &heatmap)
{
	vector<size_t> basin_sizes;

	auto all_low_points = get_all_low_points(heatmap);

	for (auto p : all_low_points)
	{
		size_t basin_size = get_basin_size(heatmap, p);
		basin_sizes.push_back(basin_size);
	}

	sort(rall(basin_sizes));

	return basin_sizes[0] * basin_sizes[1] * basin_sizes[2];
}

int main()
{
	vector<string> input = split_istream_per_line(cin);
	vector<vector<int>> heatmap;
	for (string s : input)
	{
		heatmap.push_back(digits_of(s));
	}

	cout << "Part 1: " << part_one(heatmap) << endl;
	cout << "Part 2: " << part_two(heatmap) << endl;
}
