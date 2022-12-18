#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/17

size_t num_active_neighbours(const map<int, map<int, map<int, char>>> &grid,
		int x, int y, int z)
{
	size_t out = 0;
	for (int zi = z - 1; zi <= z + 1; zi++)
	{
		if (grid.count(zi) <= 0)
		{
			continue;
		}

		for (int xi = x - 1; xi <= x + 1; xi++)
		{
			if (grid[zi].count(xi) <= 0)
			{
				continue;
			}

			for (int yi = y - 1; yi <= y + 1; y++)
			{
				if (grid[zi][xi].count(yi) <= 0)
				{
					continue;
				}

				// don't look at current spot
				if (xi == 0 && yi == 0 && zi == 0)
				{
					continue;
				}

				// check if grid[z][x][y]:
				// - exists at all
				// - is a '#'
				if (grid[zi][xi][yi] == '#')
				{
					out++;
				}
			}
		}
	}

	return out;
}

// perform a step cycle on the grid
map<int, map<int, map<int, char>>> grid step(map<int, map<int, map<int, char>>> &grid)
{
	map<int, map<int, map<int, char>>> out;

	// TODO: take into account things not in the current grid that neighbour the grid
	// as the grid will need to expand into cubes it does not currently occupy
	for (auto z_layer : grid)
	{
		for (auto x_layer : z_layer)
		{
			for (auto y_layer : x_layer)
			{
				size_t active_neighbours = num_active_neighbours(grid, z_layer.first, x_layer.first, y_layer.first);

				char cell_state = y_layer.second;
				if (cell_state == '#')
				{
					if (active_neighbours == 2 || active_neighbours == 3)
					{
						cell_state = '#';
					}
					else
					{
						cell_state = '.';
					}
				}
				else if (cell_state == '.')
				{
					if (active_neighbors == 3)
					{
						cell_state = '#';
					}
					else
					{
						cell_state = '.';
					}
				}
				out[z_layer.first][x_layer.first][y_layer.first] = cell_state;
			}
		}
	}

	return out;
}

size_t solve(const vector<string> &in, bool part_two)
{
	size_t out = 0;

	// z, x, y
	map<int, map<int, map<int, char>>> grid;

	for (size_t i = 0; i < in.size(); i++)
	{
		for (size_t j = 0; j < in[i].size(); j++)
		{
			grid[0][i][j] = in[i][j];
		}
	}

	size_t cycles = 0;


	for (size_t i = 0; i < in.size(); i++)
	{
		size_t sum = evaluate(in[i]);
		cout << "sum of " << in[i] << " = " << sum << endl;
		out += sum;
	}

	return out;
}

int main(int argc, char** argv)
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

