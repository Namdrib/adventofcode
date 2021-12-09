#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/5

typedef vector<pair<pair<int, int>, pair<int, int>>> vent_lines_t;
typedef vector<vector<int>> vent_map_t;

// read each of the vent lines and plot them on a 2D plane (vent map)
vent_map_t create_vent_map(vent_lines_t vent_lines, bool do_diagonals)
{
	// calculate how large the plane needs to be
	int max_x = 0;
	int max_y = 0;

	for (auto v : vent_lines)
	{
		max_x = max(max_x, max(v.first.first, v.second.first));
		max_y = max(max_y, max(v.first.second, v.second.second));
	}

	// create an empty map of the right size
	vent_map_t vent_map(max_y + 1, vector<int>(max_x + 1, 0));

	// populate vent_map with elements from the vents
	for (auto vent_line : vent_lines)
	{
		// make the co-ordinates more human-readable
		int x1 = vent_line.first.first;
		int x2 = vent_line.second.first;
		int y1 = vent_line.first.second;
		int y2 = vent_line.second.second;

		// determine whether to map the line
		if (x1 == x2 || y1 == y2 || do_diagonals)
		{
			// start at the beginning of the line, and step towards the end of the line
			// plotting each point along the way
			// note that lines can move "backwards"
			for (int i = y1, j = x1; i != y2 || j != x2; /* nothing */)
			{
				vent_map[i][j]++;

				// only update the indices that need to be updated
				if (i < y2)
				{
					i++;
				}
				if (i > y2)
				{
					i--;
				}
				if (j < x2)
				{
					j++;
				}
				if (j > x2)
				{
					j--;
				}
			}
			// the last point is missed, so add it in manually
			vent_map[y2][x2]++;
		}
	}

	return vent_map;
}

// return the number of points covered by two or more points
int part_one(const vent_map_t &in)
{
	int count = 0;

	for (const auto &v : in)
	{
		for (auto i : v)
		{
			if (i >= 2)
			{
				count++;
			}
		}
	}
	return count;
}

// same as part_one, but including diagonals
int part_two(const vent_map_t &in)
{
	return part_one(in);
}

int main()
{
	vector<string> input = split_istream_per_line(cin);
	vent_lines_t vents;

	for (const auto &v : input)
	{
		vector<int> nums = extract_nums_from<int>(v);
		vents.push_back(
				make_pair(
					make_pair(nums[0], nums[1]),
					make_pair(nums[2], nums[3])
				)
		);
	}

	vent_map_t vent_map = create_vent_map(vents, false);
	cout << "Part 1: " << part_one(vent_map) << endl;

	vent_map = create_vent_map(vents, true);
	cout << "Part 2: " << part_two(vent_map) << endl;
}
