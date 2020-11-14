#include <bits/stdc++.h>
#include <unistd.h>
#include "../util/helpers.cpp"
using namespace std;

// http://adventofcode.com/2019/day/13

vector<int> do_phase(const vector<int> &v, const vector<int> &base_pattern, int phase_num)
{
	vector<int> out;
	for (size_t i = 0; i < v.size(); i++)
	{
		int temp = 0;

		// build the full pattern for this rotation
		vector<int> pattern;
		int counter = 0;
		for (size_t j = 0; counter <= v.size(); j++)
		{
			// cout << "j = " << j << ", counter = " << counter << endl;
			size_t k = 0;
			do
			{
				if (j == 0 && k == 0)
				{
					// skip the first in the pattern
				}
				else
				{
					// cout << "counter = " << counter << endl;
					// cout << "  " << v[counter - 1] << " * " << base_pattern[j % base_pattern.size()] << "  + ";
					temp += v[counter - 1] * base_pattern[j % base_pattern.size()];
				}

				counter++;
				k++;
			} while (k <= i && counter <= v.size());
		}

		temp = abs(temp);
		// cout << "  = " << temp << endl;
		out.push_back(temp % 10);
	}

	return out;
}

string solve(vector<int> v, bool part_two)
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
	string out = "";
	for (int i = 0; i < 8; i++)
	{
		out += v[(i + offset) % v.size()] + '0';
	}
	return out;
}

int main()
{
	string s;
	getline(cin, s);
	// s = "12345678";
	// s = "19617804207202209144916044189917";
	// s = "03036732577212944063491565474664";
	vector<int> v;
	for (auto c : s)
	{
		v.push_back(c - '0');
	}

	// cout << "Part 1: \n" << solve(v, false) << endl;
	cout << "Part 2: " << solve(v, true) << endl;
}