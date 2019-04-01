#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/19

// every iteration, current_elf steals all the presents from steal_from
// elves without presents are out
// return the last elf remaining
int solve(int input, int part_two)
{
	// create elves from 1 to input
	list<int> elves(input);
	iota(all(elves), 1);

	auto current_elf = elves.begin();
	auto steal_from = next(current_elf, part_two ? elves.size()/2 : 1);

	while (elves.size() > 1)
	{
		// steal presents and wrap-around if necessary
		steal_from = elves.erase(steal_from);
		if (steal_from == elves.end())
		{
			steal_from = elves.begin();
		}

		// advance steal_from unless (part two and odd size remaining)
		if (!(part_two && (elves.size() & 1)))
		{
			if (++steal_from == elves.end())
			{
				steal_from = elves.begin();
			}
		}

		// advance current_elf and wrap-around
		if (++current_elf == elves.end())
		{
			current_elf = elves.begin();
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
