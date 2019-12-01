#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/1

int calculate_fuel(int mass)
{
	return floor(mass/3) - 2;
}

long solve(vector<int> modules, bool part_two = false)
{
	long sum = 0;

	for (auto module : modules)
	{
		int mass = calculate_fuel(module);
		sum += mass;

		if (part_two)
		{
			while (mass > 0)
			{
				mass = calculate_fuel(mass);
				if (mass > 0)
				{
					sum += mass;
				}
			}
		}
	}

	return sum;
}

int main()
{
	vector<int> modules = split_istream_by_whitespace<int>(cin);

	cout << "Part 1: " << solve(modules, false) << endl;
	cout << "Part 2: " << solve(modules, true) << endl;
}
