#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/3

char extrapolate(const string &in, int pos)
{
	return in[pos % in.size()];
}

size_t solve(const vector<string> &in, bool part_two = false)
{
	size_t out = 1;

	// the slope combinations to search through
	const vector<int> y_inc{1, 1, 1, 1, 2};
	const vector<int> x_inc{1, 3, 5, 7, 1};

	// for part 1, only search y=1, x=3
	size_t start = (part_two) ? 0 : 1;
	size_t end = (part_two) ? y_inc.size() : 2;
	for (size_t i=start; i < end; i++)
	{
		// calculate the number of trees encountered going down a slope
		// given by y_inc[i] and x_inc[i]
		size_t num_trees = 0;
		for (int y=0, x=0; y < in.size(); y += y_inc[i], x += x_inc[i])
		{
			if (extrapolate(in[y], x) == '#')
			{
				num_trees++;
			}
		}
		out *= num_trees;
	}

	return out;
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

