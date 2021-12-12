#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/7

// calculate how much fuel it takes to move every crab to target_pos
// for part one, the cost to move from a position pos to target_pos is linear
// for part two, every step costs one more (e.g. 1 -> 2 -> 3 ...)
size_t get_fuel_cost(const vector<size_t> &in, size_t target_pos, bool part_two)
{
		size_t fuel_to_use = accumulate(all(in), (size_t)0, [target_pos, part_two](size_t acc, size_t pos)
				{
					size_t cost = (target_pos < pos ? pos - target_pos : target_pos - pos);;
					if (part_two)
					{
						cost = cost * (cost + 1) / 2;
					}
					return acc += cost;
				}
		);

		return fuel_to_use;
}

size_t part_one(const vector<size_t> &in, bool part_two)
{
	size_t min_pos = *min_element(all(in));
	size_t max_pos = *max_element(all(in));

	size_t min_fuel_to_best_pos = numeric_limits<size_t>::max();

	// find the horizontal position that requires the least movement
	// to align all the crabs to
	for (size_t i = min_pos; i <= max_pos; i++)
	{
		size_t fuel_to_use = get_fuel_cost(in, i, part_two);

		if (fuel_to_use < min_fuel_to_best_pos)
		{
			min_fuel_to_best_pos = fuel_to_use;
		}
	}

	return min_fuel_to_best_pos;
}

size_t part_two(const vector<size_t> &in, bool part_two)
{
	return part_one(in, part_two);
}

int main()
{
	string s;
	getline(cin, s);
	vector<size_t> input = extract_nums_from<size_t>(s);

	cout << "Part 1: " << part_one(input, false) << endl;
	cout << "Part 2: " << part_two(input, true) << endl;
}
