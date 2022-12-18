#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2016/day/6

// Search for the most common letter in m
// (or least common, for part 2)
char desired_freq_in(const map<char, int> &m, bool part_two)
{
	int count = part_two ? numeric_limits<int>::max() : numeric_limits<int>::min();
	char out = 'a';

	for (auto it=m.begin(); it!=m.end(); it++)
	{
		if (part_two ? it->second < count : it->second > count) 
		{
			out = it->first;
			count = it->second;
		}
	}
	return out;
}

// Return the correctly-encoded word
string correct(const vector<string> &in, bool part_two)
{
	string out;
	for (size_t i=0; i<in[0].size(); i++) // Across
	{
		map<char, int> char_count;
		// Find the most common char in this column
		for (auto s : in) // Down
		{
			char_count[s[i]]++;
		}
		out += desired_freq_in(char_count, part_two);
	}
	return out;
}

int main()
{
	vector<string> input;
	for (string temp; getline(cin, temp);)
	{
		input.push_back(temp);
	}

	cout << "Part 1: " << correct(input, false) << endl;
	cout << "Part 2: " << correct(input, true) << endl;
}
