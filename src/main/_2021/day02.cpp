#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/2

int parse(const vector<string> &in, bool part_two)
{
	int horizontal = 0;
	int depth = 0;
	int aim = 0;

	for (auto s : in)
	{
		vector<string> tokens = split_str_by_whitespace<string>(s);

		string command = tokens[0];
		int scale = stoi(tokens[1]);

		if (command == "forward")
		{
			horizontal += scale;
			if (part_two)
			{
				depth += (aim * scale);
			}
		}
		else if (command == "down")
		{
			(part_two ? aim : depth) += scale;
		}
		else if (command == "up")
		{
			(part_two ? aim : depth) -= scale;
		}
	}

	return horizontal * depth;

}

int part_one(const vector<string> &in)
{
	return parse(in, false);
}

int part_two(const vector<string> &in)
{
	return parse(in, true);
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << part_one(input) << endl;
	cout << "Part 2: " << part_two(input) << endl;
}
