#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/22

size_t deal_into_new_stack(size_t num_elements, size_t pos)
{
	return num_elements - pos - 1;
}

size_t cut(size_t num_elements, long long pos, long long n)
{
	// return (pos - n) % num_elements;
	if (n < 0)
	{
		n += num_elements;
	}

	pos -= n;
	if (pos < 0)
	{
		pos += num_elements;
	}
	return pos;
}

// not feasible for huge numbers
size_t deal_with_increment(size_t num_elements, size_t pos, size_t n)
{
	long long current_position = 0;
	for (size_t i = 0; i < pos; i++)
	{
		current_position = (current_position + n) % num_elements;
	}
	return current_position;
}

int solve(const vector<vector<string>> &input, bool part_two)
{
	long long num_cards = part_two ? 119315717514047 : 10007;
	long long pos = part_two ? 2020 : 2019;

	for (auto instruction : input)
	{
		if (instruction[0] == "cut")
		{
			pos = cut(num_cards, pos, stoi(instruction[1]));
		}
		else
		{
			if (instruction[1] == "into")
			{
				pos = deal_into_new_stack(num_cards, pos);
			}
			else
			{
				pos = deal_with_increment(num_cards, pos, stoi(instruction[3]));
			}
		}
	}

	return pos;
}

int main()
{
	vector<vector<string>> instructions;
	for (string temp; getline(cin, temp); )
	{
		vector<string> instruction = split_str_by_whitespace<string>(temp);
		instructions.push_back(instruction);
	}

	{ // assert deal_into_new_stack
		assert(deal_into_new_stack(10, 0) == 9);
		assert(deal_into_new_stack(10, 1) == 8);
		assert(deal_into_new_stack(10, 2) == 7);
		assert(deal_into_new_stack(10, 3) == 6);
		assert(deal_into_new_stack(10, 4) == 5);
	}

	{ // assert cut positive
		assert(cut(10, 0, 3) == 7);
		assert(cut(10, 1, 3) == 8);
		assert(cut(10, 2, 3) == 9);
		assert(cut(10, 3, 3) == 0);
		assert(cut(10, 4, 3) == 1);
		assert(cut(10, 5, 3) == 2);
	}

	{ // assert cut negative
		assert(cut(10, 8, -4) == 2);
		assert(cut(10, 9, -4) == 3);
		assert(cut(10, 0, -4) == 4);
		assert(cut(10, 1, -4) == 5);
	}

	{ // assert deal_with_increment
		assert(deal_with_increment(10, 0, 3) == 0);
		assert(deal_with_increment(10, 1, 3) == 3);
		assert(deal_with_increment(10, 2, 3) == 6);
		assert(deal_with_increment(10, 3, 3) == 9);
		assert(deal_with_increment(10, 4, 3) == 2);
		assert(deal_with_increment(10, 5, 3) == 5);
		assert(deal_with_increment(10, 6, 3) == 8);
		assert(deal_with_increment(10, 7, 3) == 1);
		assert(deal_with_increment(10, 8, 3) == 4);
		assert(deal_with_increment(10, 9, 3) == 7);
	}

	cout << "Part 1: " << solve(instructions, false) << endl;
	// cout << "Part 2: " << solve(instructions, true) << endl;
}