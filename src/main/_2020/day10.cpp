#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/10

// recursion: look at how many ways from `pos` we can get to the end
// base case: we're at the last charger - there is only one way to the end
// every other case should just sum up the possible ways ahead of it
size_t recurse(vector<int> &in, size_t pos, map<size_t, size_t> &memory)
{
	// base case: already at end of list
	if (pos == in.size() - 1)
	{
		memory[pos] = 1;
		return memory[pos];
	}

	// early return, we already know how many combinations to end from pos
	if (memory.count(pos) > 0)
	{
		return memory[pos];
	}

	// find out how many combinations to end from pos
	size_t sum = 0;

	// look forwards from here, accumulate all the potential combinations
	for (size_t i = 1; i <= 3; i++)
	{
		// if we can skip, check the potential combinations in each of them
		if (in_bounds(in, pos + i) && (in[pos + i] - in[pos] <= 3))
		{
			sum += recurse(in, pos + i, memory);
		}
	}

	// store it for later
	memory[pos] = sum;
	return memory[pos];
}

size_t solve(vector<int> in, bool part_two)
{
	in.push_back(0); // add starting joltage
	sort(all(in));
	in.push_back(in.back() + 3); // add my device

	if (part_two)
	{
		// recursively work out how many combinations there are from a given
		// position (in this case 0) to the end. store these in a lookup
		map<size_t, size_t> combinations_to_end;
		recurse(in, 0, combinations_to_end);
		return combinations_to_end[0];
	}
	else
	{
		// count the number of one-volt and three-jolt differences
		size_t num_ones = 0;
		size_t num_threes = 0;

		for (size_t i = 0; i < in.size() - 1; i++)
		{
			size_t diff = in[i + 1] - in[i];
			if (diff == 1)
			{
				num_ones++;
			}
			else if (diff == 3)
			{
				num_threes++;
			}
		}

		return num_ones * num_threes;
	}

	return 0;
}

int main(int argc, char** argv)
{
	vector<int> input = split_istream_by_whitespace<int>(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

