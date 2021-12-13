#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/13

// return the result of folding transparent_paper according to the fold instruction
vector<vector<bool>> fold(vector<vector<bool>> transparent_paper, const string fold_instruction)
{
	size_t equals_pos = fold_instruction.find("=");
	string dimension = fold_instruction.substr(equals_pos-1, 1);
	int fold_location = stoi(fold_instruction.substr(equals_pos+1));

	cout << "Folding on " << dimension << " at " << fold_location << endl;

	if (dimension == "y")
	{
		// merge the elements on bottom half up onto the top half
		for (size_t i = fold_location; i < transparent_paper.size(); i++)
		{
			for (size_t j = 0; j < transparent_paper[i].size(); j++)
			{
				transparent_paper[fold_location - (i - fold_location)][j] = transparent_paper[fold_location - (i - fold_location)][j] +  transparent_paper[i][j];
			}
		}

		// complete the fold by removing the bottom half
		transparent_paper.erase(transparent_paper.begin() + fold_location, transparent_paper.end());
	}

	else
	{
		// merge the elements on right half across onto the left half
		for (size_t i = 0; i < transparent_paper.size(); i++)
		{
			for (size_t j = fold_location; j < transparent_paper[i].size(); j++)
			{
				transparent_paper[i][fold_location - (j - fold_location)] = transparent_paper[i][fold_location - (j - fold_location)] +  transparent_paper[i][j];
			}
		}

		// complete the fold by removing the right half
		for (auto &v : transparent_paper)
		{
			v.erase(v.begin() + fold_location, v.end());
		}
	}

	return transparent_paper;
}

size_t part_one(vector<vector<bool>> in, const vector<string> &fold_instructions)
{
	in = fold(in, fold_instructions[0]);

	return accumulate(all(in), 0, [](int acc, const vector<bool> &v){return acc + accumulate(all(v), 0);});
}

size_t part_two(vector<vector<bool>> in, const vector<string> &fold_instructions)
{
	for (auto fold_instruction : fold_instructions)
	{
		in = fold(in, fold_instruction);
	}

	// to make it easier to read, replace 1s with '#' and 0s with ' '
	for (auto v : in)
	{
		for (auto b : v)
		{
			cout << (b ? '#' : ' ');
		} cout << endl;
	} cout << endl;
	return 0;
}

int main()
{
	// store all the co-ordinates
	set<pair<int, int>> coords;
	int max_y = numeric_limits<int>::min();
	int max_x = numeric_limits<int>::min();
	for (string s; getline(cin, s);)
	{
		if (s.empty())
		{
			break;
		}

		// store it as (x,y)
		vector<int> nums = extract_nums_from<int>(s);
		max_y = max(max_y, nums[1]);
		max_x = max(max_x, nums[0]);
		coords.insert(make_pair(nums[0], nums[1]));
	}

	// populate the transparent paper with dots
	vector<vector<bool>> transparent_paper(max_y + 1, vector<bool>(max_x + 1, false));
	for (auto p : coords)
	{
		transparent_paper[p.second][p.first] = true;
	}

	// read the fold instructions
	vector<string> fold_instructions = split_istream_per_line(cin);

	cout << "Part 1: " << part_one(transparent_paper, fold_instructions) << endl;
	cout << "Part 2: " << part_two(transparent_paper, fold_instructions) << endl;
}
