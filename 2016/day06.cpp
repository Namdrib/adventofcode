#include <iostream>
#include <map>
#include <vector>
using namespace std;

// http://adventofcode.com/2016/day/6

// Search for the most common letter in m
// (or least common, for part 2)
char mostCommonIn(map<char, int> &m)
{
	int count = 99;
	char mostCommon = 'a';
	for (auto it=m.begin(); it!=m.end(); it++)
	{
		// Flip the sign for parts
		// 1: >
		// 2: <
		if (it->second < count) 
		{
			mostCommon = it->first;
			count = it->second;
		}
	}
	return mostCommon;
}

// Return the correctly-encoded word
string correct(const vector<string> &in)
{
	string out;
	for (size_t i=0; i<in[0].size(); i++) // Across
	{
		map<char, int> charCount;
		// Find the most common char in this column
		for (size_t j=0; j<in.size(); j++) // Down
		{
			charCount[in[j][i]]++;
		}
		out += mostCommonIn(charCount);
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
	
	cout << correct(input) << endl; // Part 1
}
