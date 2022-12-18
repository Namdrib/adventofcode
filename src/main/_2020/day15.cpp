#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/15
//
// figure out how long we need to wait until we can depart
size_t solve(const vector<int> &in, bool part_two)
{
	// map a spoken number to the last first/last/second last turn it was spoken
	map<int, size_t> first_spoken;
	map<int, size_t> last_spoken;
	map<int, size_t> second_last_spoken;

	// the most recently spoken number
	int mrs = 0;

	// seed the initial set
	size_t turn_num = 1;
	for (size_t i = 0; i < in.size(); i++)
	{
		mrs = in[i];
		last_spoken[mrs] = turn_num;
		first_spoken[mrs] = turn_num;
		turn_num++;
	}

	// part two is just longer compute time
	// brute force runs in about 20 seconds
	for (; turn_num <= (part_two ? 30000000 : 2020); turn_num++)
	{
		// mrs is new, next is 0
		if (first_spoken[mrs] == turn_num - 1)
		{
			mrs = 0;
		}
		// mrs has been spoken, get time since last time it was spoken
		else
		{
			mrs = last_spoken[mrs] - second_last_spoken[mrs];
		}

		// update bookkeeping information
		second_last_spoken[mrs] = last_spoken[mrs];
		last_spoken[mrs] = turn_num;
		if (first_spoken.count(mrs) <= 0)
		{
			first_spoken[mrs] = turn_num;
		}
	}

	// return the number spoken at turn X
	return mrs;
}

int main(int argc, char** argv)
{
	string s;
	getline(cin, s);
	vector<int> input = extract_nums_from<int>(s);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

