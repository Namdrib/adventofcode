#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/1

int part_one(const vector<int> &in)
{
	int count = 0;

	for (size_t i = 1; i < in.size(); i++)
	{
		if (in[i] > in[i-1])
		{
			count++;
		}
	}

	return count;
}

int part_two(const vector<int> &in)
{

	// construct a second vector that is the sum of every adjacent 3 elements
	vector<int> threes;

	for (size_t i = 0; i < in.size() - 2; i++)
	{
		threes.push_back(in[i] + in[i+1] + in[i+2]);
	}

	// code re-use ftw
	return part_one(threes);
}

int main()
{
	vector<int> input = split_istream_by_whitespace<int>(cin);

	cout << "Part 1: " << part_one(input) << endl;
	cout << "Part 2: " << part_two(input) << endl;
}
