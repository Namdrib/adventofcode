#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/6

int solve(const vector<string> &in, bool part_two)
{
	// store all the groups' answers and sizes
	vector<map<char, int>> group_answers;
	vector<int> group_sizes;

	map<char, int> group_answer;
	int group_size = 0;
	for (auto s : in)
	{
		// a group separator
		// save the current answer and group size
		if (s == "")
		{
			group_answers.push_back(group_answer);
			group_answer.clear();

			group_sizes.push_back(group_size);
			group_size = 0;
			continue;
		}

		for (auto c : s)
		{
			group_answer[c]++;
		}
		group_size++;
	}

	// don't forget to save the last group too!
	group_answers.push_back(group_answer);
	group_sizes.push_back(group_size);

	// calculate the answer
	int sum = 0;
	if (part_two)
	{
		// return the sum of all things for which everyone answered yes
		// i.e. where the count for an answer matches the group size
		for (size_t i = 0; i < group_answers.size(); i++)
		{
			auto answer = group_answers[i];

			for (auto p : answer)
			{
				if (p.second == group_sizes[i])
				{
					sum++;
				}
			}
		}
	}
	else
	{
		// return the sum of all things for which anyone answered yes
		sum = accumulate(all(group_answers), 0, [](int acc, const map<char, int> &group_answer){
				return acc + group_answer.size();
		});
	}
	return sum;
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

