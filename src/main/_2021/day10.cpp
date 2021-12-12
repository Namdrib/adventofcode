#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/10

const map<char, size_t> illegal_character_scores = {
	{')', 3},
	{']', 57},
	{'}', 1197},
	{'>', 25137}
};

class bracket_string
{
	stack<char> s;

	map<char, char> matching_bracket = {
		{'(', ')'},
		{'[', ']'},
		{'{', '}'},
		{'<', '>'},
	};

	map<char, int> completion_points = {
		{')', 1},
		{']', 2},
		{'}', 3},
		{'>', 4}
	};

	char get_match() const
	{
		return matching_bracket.at(s.top());
	}

	bool is_match(char c) const
	{
		return c == get_match();
	}

	public:

		// add character c to s
		// return true iff it was successful
		// openings are added
		// closings are successful iff it matches the most current opening
		bool add_char(char c)
		{
			if (c == '(' || c == '[' || c == '{' || c == '<')
			{
				s.push(c);
				return true;
			}
			else if (c == ')' || c == ']' || c == '}' || c == '>')
			{
				if (is_match(c))
				{
					s.pop();
					return true;
				}
				else
				{
					return false;
				}
			}
			else
			{
				return false;
			}
		}

		// completes the rest of s and returns the score of the completion
		size_t complete()
		{
			size_t out = 0;
			while (!s.empty())
			{
				char c = get_match();
				out *= 5;
				out += completion_points.at(c);
				add_char(c);
			}

			return out;
		}
};

size_t part_one(const vector<string> &in, bool part_two)
{
	size_t corrupted_score_sum = 0;
	vector<size_t> incomplete_scores;
	for (auto s : in)
	{
		bracket_string bs;
		bool corrupted = false;

		for (auto c : i)
		{
			// bs is corrupted
			if (!bs.add_char(c))
			{
				corrupted_score_sum += illegal_character_scores.at(c);
				corrupted = true;
				break;
			}
		}

		if (corrupted)
		{
			continue;
		}

		// we got this far, that means bs is not corrupted - just incomplete
		// now complete it
		if (part_two)
		{
			incomplete_scores.push_back(bs.complete());
		}
	}

	if (part_two)
	{
		// return the middle score
		sort(all(incomplete_scores));
		return incomplete_scores[incomplete_scores.size() / 2];
	}
	else
	{
		return corrupted_score_sum;
	}
}

size_t part_two(const vector<string> &in, bool part_two)
{
	return part_one(in, part_two);
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << part_one(input, false) << endl;
	cout << "Part 2: " << part_two(input, true) << endl;
}
