#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2016/day/19

// every iteration, current_elf steals all the presents from target_elf
// elves without presents are out
// return the last elf remaining
int solve(int input, int part_two)
{
	// create elves from 1 to input
	list<int> elves(input);
	iota(all(elves), 1);

	auto current_elf = elves.begin();
	auto target_elf = current_elf;

	if (part_two)
	{
		advance(target_elf, elves.size()/2);
	}

	while (elves.size() > 1)
	{
		// advance and wrap-around
		if (!part_two)
		{
			target_elf = current_elf;
			if (++target_elf == elves.end())
			{
				target_elf = elves.begin();
			}
		}

		// steal presents and wrap-around if necessary
		target_elf = elves.erase(target_elf);
		if (target_elf == elves.end())
		{
			target_elf = elves.begin();
		}
		if (part_two)
		{
			if (elves.size() % 2 == 0)
			{
				if (++target_elf == elves.end())
				{
					target_elf = elves.begin();
				}
			}
		}

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
