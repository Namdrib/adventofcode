#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/9

bool two_nums_sum_to(const vector<int> &search_space, int target)
{
	for (size_t i = 0; i < search_space.size() - 1; i++)
	{
		for (size_t j = i + 1; j < search_space.size(); j++)
		{
			if (search_space[i] + search_space[j] == target)
			{
				return true;
			}
		}
	}

	return false;
}

size_t solve(const vector<long> &in, bool part_two = false)
{
	const int preamble_size = 25;

	vector<int> preamble(in.begin(), in.begin() + preamble_size);

	size_t invalid_number = 0;
	size_t invalid_number_index = 0;

	// find the first number for which the rolling preabmble does NOT
	// contain two numbers that sum to it. assign this to invalid_number
	for (size_t i = preamble_size; i < in.size(); i++)
	{
		size_t target = in[i];

		bool two_nums_sum_to_target = two_nums_sum_to(preamble, target);
		if (!two_nums_sum_to_target)
		{
			invalid_number = target;
			invalid_number_index = i;
			break;
		}
		preamble.erase(preamble.begin());
		preamble.push_back(in[i]);
	}

	// this is part 1
	if (!part_two)
	{
		return invalid_number;
	}

	// part 2: find the contiguous set of 2+ nums in the list that sum to
	// invalid_number

	// from each position, accumulate the numbers leading up to invalid_number
	// use this to determine which indices mark the start/end fo the set
	for (size_t i = 0; i < in.size(); i++)
	{
		if (i == invalid_number_index)
		{
			continue;
		}

		size_t sum = in[i];
		for (size_t j = i + 1; j < in.size(); j++)
		{
			// don't search the invalid number
			if (j == invalid_number_index)
			{
				continue;
			}

			sum += in[j];

			// got the range, breaking
			if (sum == invalid_number)
			{
				// return the sum of the smallest and largest elements in that range
				auto result = minmax_element(in.begin() + i, in.begin() + j + 1);
				return *result.first + *result.second;
			}

			// everything after this will continue to be > invalid_number
			if (sum > invalid_number)
			{
				break;
			}
		}
	}

	return -1;
}


int main(int argc, char** argv)
{
	vector<long> input = split_istream_by_whitespace<long>(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

