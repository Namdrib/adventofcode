#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/19

int solve(int input, bool part_two)
{
	// create list with that number of elves
	list<int> elves;
	for (int i = 1; i <= input; i++)
	{
		elves.push_back(i);
	}

	auto it = elves.begin();
	while (elves.size() > 1)
	{
		// advance and wrap-around
		auto next = it;
		if (++next == elves.end())
		{
			next = elves.begin();
		}

		// steal presents and wrap-around if necessary
		elves.erase(next);
		if (++it == elves.end())
		{
			it = elves.begin();
		}
	}

	return *elves.begin();
}

int main()
{
	int input;
	cin >> input;

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}
