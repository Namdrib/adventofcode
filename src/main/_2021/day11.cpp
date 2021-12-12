#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/11

// starting in the top left corner, going clockwise
const array<int, 8> dx = {-1, 0, 1, 1, 1, 0, -1, -1};
const array<int, 8> dy = {-1, -1, -1, 0, 1, 1, 1, 0};
// return the result of a step of in
vector<vector<int>> do_step(const vector<vector<int>> &in)
{
	// take a copy so we can modify it
	vector<vector<int>> out(in);
	vector<vector<bool>> flashed(out.size(), vector<bool>(out[0].size(), false));

	// First, the energy level of each octupus increases by 1
	for (auto &v : out)
	{
		for (auto &i : v)
		{
			++i;
		}
	}

	// Then, any octopus with an energy level greater than 9 flashes. This
	// increases the energy  level of all adjacent octopuses by 1, including
	// octopuses that are diagonally adjacent. If this causes an octopus to
	// have an energy level greater than 9, it also flashes. This process
	// continues as long as new octopuses keep having their energy level
	// increased beyond 9. (An octopus can only flash at most once per step.)
	bool new_flash = true;
	while (new_flash)
	{
		new_flash = false;
		for (size_t i = 0; i < out.size(); i++)
		{
			for (size_t j = 0; j < out[i].size(); j++)
			{
				// if we're newly-flashing
				if (out[i][j] > 9 && !flashed[i][j])
				{
					flashed[i][j] = true;
					new_flash = true;

					// for each neighbour
					for (size_t k = 0; k < dx.size(); k++)
					{
						int new_i = i + dy[k];
						int new_j = j + dx[k];

						// raise the energy by 1
						if (new_i >= 0 && static_cast<size_t>(new_i) < out.size()
								&& new_j >= 0 && static_cast<size_t>(new_j) < out[new_i].size())
						{
							out[new_i][new_j]++;
						}
					}
				}
			}
		}
	}

	// Finally, any octopus that flashed during this step has its energy
	// level set to 0, as it used all of its energy to flash.
	for (auto &v : out)
	{
		for (auto &i : v)
		{
			if (i > 9)
			{
				i = 0;
			}
		}
	}

	return out;
}

// count how many flashes occur over the first 100 steps
size_t part_one(vector<vector<int>> in)
{
	size_t num_flashes = 0;
	for (int i = 0; i < 100; i++)
	{
		in = do_step(in);

		for (auto v : in)
		{
			num_flashes += accumulate(all(v), 0, [](int acc, int i){return acc + (i == 0);});
		}
	}
	return num_flashes;
}

// find the first step where all the octopuses have flashed
size_t part_two(vector<vector<int>> in)
{
	for (int step_count = 1; true; step_count++)
	{
		in = do_step(in);

		if (all_of(all(in), [](const vector<int> &v)
					{
					return all_of(all(v), [](const int &i)
							{return i == 0;});
					}))
		{
			return step_count;
		}
	}
}

int main()
{
	vector<string> lines = split_istream_per_line(cin);
	vector<vector<int>> input;

	for (const auto &s : lines)
	{
		input.push_back(digits_of(s));
	}

	cout << "Part 1: " << part_one(input) << endl;
	cout << "Part 2: " << part_two(input) << endl;
}
