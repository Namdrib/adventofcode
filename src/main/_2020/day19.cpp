#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/19

class rule
{
	public:
		vector<vector<size_t>> matches;

		vector<string> str_matches;
};

// populate the str_matches of all the rules
void preprocess(map<size_t, rule> rules)
{
	cout << "raw rules:" << endl;
	for (auto rule : rules)
	{
		cout << rule.first << ": ";
		for (auto v : rule.second.matches)
		{
			cout << v << endl;
		}
	}

	// make n passes, don't care about this index
	for (size_t n = 0; n < rules.size(); n++)
	{
		// for each rule
		for (auto &rule : rules)
		{
			if (!rule.second.str_matches.empty())
			{
				continue;
			}
			// if all of the child rule matches have been populated
			bool all_matches_available = true;
			for (size_t j = 0; j < rule.second.matches.size(); j++)
			{
				for (auto match_num : rule.second.matches[j])
				{
					if (rules[match_num].str_matches.empty())
					{
						all_matches_available = false;
						break;
					}
				}
			}

			// populate the string matches for this rule
			if (all_matches_available)
			{
				cout << "populating rule " << rule.first << endl;
				// populate the str_matches string
				for (size_t j = 0; j < rule.second.matches.size(); j++)
				{
				string s;
					for (auto match_num : rule.second.matches[j])
					{
						for (auto s2 : rules[match_num].str_matches)
						{
							s += s2;
						}
					}
				rule.second.str_matches.push_back(s);
				cout << s << endl;

				}
			}
		}
	}
}

size_t match(const map<size_t, rule> &rules, string s, size_t rule_num = 0)
{
	return 0;
}

size_t solve(const vector<string> &in, bool part_two)
{
	size_t out = 0;

	// parse the rules into objects
	map<size_t, rule> rules;
	size_t i;
	for (i = 0; i < in.size(); i++)
	{
		if (in[i].empty())
		{
			break;
		}

		// extract the id
		size_t colon_pos = in[i].find(":");
		string raw_id = in[i].substr(0, colon_pos);
		size_t id = stoull(raw_id);

		// extract the rule
		rule temp;
		size_t quote_pos = in[i].find("\"");
		if (quote_pos == string::npos)
		{
			// read raw rule numbers
			string rhs = in[i].substr(colon_pos + 2);

			size_t pipe_pos = rhs.find("|");
			if (pipe_pos == string::npos)
			{
				vector<size_t> rule_nums = extract_nums_from<size_t>(rhs);

				temp.matches.push_back(rule_nums);
			}
			else
			{
				string rhs_l = rhs.substr(0, pipe_pos);
				string rhs_r = rhs.substr(pipe_pos);
				vector<size_t> rule_nums_lhs = extract_nums_from<size_t>(rhs_l);
				vector<size_t> rule_nums_rhs = extract_nums_from<size_t>(rhs_r);

				temp.matches.push_back(rule_nums_lhs);
				temp.matches.push_back(rule_nums_rhs);
			}
		}
		else
		{
			size_t matching_quote_pos = in[i].find_last_of("\"");
			string str_matches = in[i].substr(quote_pos + 1, matching_quote_pos - quote_pos - 1);

			temp.str_matches.push_back(str_matches);
		}

		// store the id and rule
		rules[id] = temp;
	}

	// read the messages
	vector<string> msgs;
	for (; i < in.size(); i++)
	{
		msgs.push_back(in[i]);
	}

	// preprocess the rules to populate their string matches
	// e.g. "ab", "ba"
	preprocess(rules);

	// count how many msgs match rule 0
	size_t num_matching_zero = 0;
	for (size_t i = 0; i < msgs.size(); i++)
	{
		if (match(rules, msgs[i], 0))
		{
			num_matching_zero++;
		}
	}
	return num_matching_zero;

	return out;
}

int main(int argc, char** argv)
{
	vector<string> input = split_istream_per_line(cin);
	//vector<int> input = split_istream_by_whitespace(cin);

	cout << "Part 1: " << solve(input, false) << endl;
	cout << "Part 2: " << solve(input, true) << endl;
}

