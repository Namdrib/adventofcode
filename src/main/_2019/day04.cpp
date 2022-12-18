#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/4

// Criteria:
// - Length is exactly 6
// - Must be sorted (ascending). Duplicates allowed
// - Must have at least two adjacent digits that are the same
// - Must have at least one pair of EXACTLY two digits that are the same (part two)
bool is_valid(int input, bool part_two)
{
	string s = to_string(input);

	if (s.size() != 6)
	{
		return false;
	}

	if (!is_sorted(all(s)))
	{
		return false;
	}

	bool has_double = false;

	for (size_t i = 0; i < s.size() - 1; i++)
	{
		if (s[i] == s[i+1])
		{
			has_double = true;
			break;
		}
	}

	if (!has_double)
	{
		return false;
	}

	// there is at least one pair of EXACTLY two matching digits
	if (part_two)
	{
		bool got_exactly_two = false;
		map<char, int> freqs;
		for (size_t i = 0; i < s.size(); i++)
		{
			freqs[s[i]]++;
		}
		for (auto p : freqs)
		{
			if (p.second == 2)
			{
				got_exactly_two = true;
				break;
			}
		}

		if (!got_exactly_two)
		{
			return false;
		}
	}

	// have passed all conditions so far, input matches rules
	return true;
}

int solve(int start, int finish, bool part_two = false)
{
	int out = 0;

	for (int i = start; i <= finish; i++)
	{
		if (is_valid(i, part_two))
		{
			out++;
		}
	}

	return out;
}

int main()
{
	int low, high;
	cin >> low;
	cin.ignore();
	cin >> high;

	assert(is_valid(111111, false) == 1);
	assert(is_valid(223450, false) == 0);
	assert(is_valid(123789, false) == 0);

	assert(is_valid(112233, true) == 1);
	assert(is_valid(123444, true) == 0);
	assert(is_valid(124444, true) == 0);
	assert(is_valid(124445, true) == 0);
	assert(is_valid(144444, true) == 0);
	assert(is_valid(444445, true) == 0);
	assert(is_valid(111111, true) == 0);
	assert(is_valid(111122, true) == 1);

	cout << "Part 1: " << solve(low, high, false) << endl;
	cout << "Part 2: " << solve(low, high, true) << endl;
}
