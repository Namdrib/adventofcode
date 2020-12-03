#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/1

int part_one(const vector<int> &in, int target)
{
	vector<int> v(in);
	sort(all(v));

	// start at the ends of the sorted vector
	int start = 0;
	int end = v.size() - 1;

	// tick in from the ends until the sum is right
	while (true)
	{
		if (start >= end)
		{
			break;
		}

		if (v[start] + v[end] < target)
		{
			start++;
		}
		else if (v[start] + v[end] > target)
		{
			end--;
		}
		else
		{
			return v[start] * v[end];
		}
	}

	// did not find a result
	return -1;
}

int part_two(const vector<int> &in, int target)
{
	vector<int> v(in);
	sort(all(v));

	for (size_t i = 0; i < v.size() - 2; i++)
	{
		for (size_t j = i + 1; j < v.size() - 1; j++)
		{
			// if the sum of two is already larger than target, don't bother with more
			int sum_i_j = v[i] + v[j];
			if (sum_i_j > target)
			{
				continue;
			}

			// check the sum of three
			for (size_t k = j + 1; k  <v.size(); k++)
			{
				if (sum_i_j + v[k] == target)
				{
					return v[i] * v[j] * v[k];
				}
			}
		}
	}

	return -1;
}

int main()
{
	vector<int> input = split_istream_by_whitespace<int>(cin);

	cout << "Part 1: " << part_one(input, 2020) << endl;
	cout << "Part 2: " << part_two(input, 2020) << endl;
}
