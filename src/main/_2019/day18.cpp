#include <bits/stdc++.h>
#include <unistd.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/18

int solve(vector<int> v, bool part_two)
{
	int num_phases = 100;

	vector<int> base_pattern = {0, 1, 0, -1};

	// build the real signal (original signal repeated 10k times)
	if (part_two)
	{
		vector<int> temp(v);
		v.resize(v.size() * 10000);
		for (size_t i = 0; i < v.size(); i++)
		{
			v[i] = temp[i % temp.size()];
		}
	}

	for (int i = 0; i < num_phases; i++)
	{
		cout << "doing phase " << i + 1 << endl;
		v = do_phase(v, base_pattern, i + 1);
		// cout << "after " << i + 1 << " phase: " << v << endl;
	}

	// calculate offset for part 2
	int offset = 0;
	if (part_two)
	{
		string temp_offset = "";
		for (int i = 0; i < 7; i++)
		{
			temp_offset += v[i] + '0';
		}
		offset = stoi(temp_offset);
	}
	
	// extract the message
	int out = 0;
	return out;
}

int main()
{
	string s;
	getline(cin, s);
	vector<int> v;
	for (auto c : s)
	{
		v.push_back(c - '0');
	}

	cout << "Part 1: " << solve(v, false) << endl;
	// cout << "Part 2: " << solve(v, true) << endl;
}
