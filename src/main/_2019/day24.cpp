#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/24

const int adj_x[4] = {0, 0, -1, 1};
const int adj_y[4] = {-1, 1, 0, 0};

// apply the following rules:
// - a bug dies unless there is exactly one adjacent bug
// - empty space becomes infested if there are exactly one or two adjacent bugs
vector<string> tick(const vector<string> &grid)
{
	vector<string> out(grid);

	for (size_t y = 0; y < grid.size(); y++)
	{
		for (size_t x = 0; x < grid[y].size(); x++)
		{
			// count number of adjacent bugs
			int num_adjacent = 0;
			for (int k = 0; k < 4; k++)
			{
				int target_y = y + adj_y[k];
				if (!in_bounds(grid, target_y))
				{
					continue;
				}
				int target_x = x + adj_x[k];
				if (!in_bounds(grid, target_x))
				{
					continue;
				}

				if (grid[target_y][target_x] == '#')
				{
					num_adjacent++;
				}
			}

			if (out[y][x] == '#')
			{
				if (num_adjacent != 1)
				{
					out[y][x] = '.';
				}
			}
			else
			{
				if (num_adjacent == 1 || num_adjacent == 2)
				{
					out[y][x] = '#';
				}
			}
		}
	}

	return out;
}


// each location in the grid (starting top-left), moving left
// has a biodiversity rating increasing in powers of two
size_t get_biodiversity_rating_of(const vector<string> &grid)
{
	size_t out = 0;

	for (size_t i = 0; i < grid.size(); i++)
	{
		for (size_t j = 0; j < grid[i].size(); j++)
		{
			if (grid[i][j] == '#')
			{
				out += pow(2, i * grid[i].size() + j);
			}
		}
	}

	return out;
}


int solve(const vector<string> &input, bool part_two)
{
	set<vector<string>> previous_grids;
	vector<string> grid = input;

	while (previous_grids.count(grid) == 0)
	{
		previous_grids.insert(grid);
		grid = tick(grid);
	}

	return get_biodiversity_rating_of(grid);
}

int main()
{
	vector<string> grid;
	for (string temp; getline(cin, temp); )
	{
		grid.push_back(temp);
	}

	cout << "Part 1: " << solve(grid, false) << endl;
	// cout << "Part 2: " << solve(grid, true) << endl;
}
