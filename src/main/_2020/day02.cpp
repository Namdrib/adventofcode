#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/2

class password_policy_info
{
public:
	// these mean something diff for part 1 and 2
	int num1;
	int num2;

	char letter;

	string password;

	// there are between num1 and num2 instances of letter in password
	bool part_one_match()
	{
		int letter_matches = 0;
		for (auto c : password)
		{
			if (c == letter)
			{
				letter_matches++;
			}
		}

		return (num1 <= letter_matches && letter_matches <= num2);
	}

	// exactly one of the password positions specified by num1 and num2 match letter
	bool part_two_match()
	{
		return (password[num1] == letter) + (password[num2] == letter) == 1;
	}
};

vector<password_policy_info> get_policies_from_input(const vector<string> &in)
{
	vector<password_policy_info> out;
	for (const auto& raw_pw_entry : in)
	{
		// parse the string to get the components
		size_t dash_pos = raw_pw_entry.find('-');
		size_t first_space_pos = raw_pw_entry.find(' ');
		size_t colon_pos = raw_pw_entry.find(':');

		// store in an object
		password_policy_info ppi;
		ppi.num1 = stoi(raw_pw_entry.substr(0, dash_pos));
		ppi.num2 = stoi(raw_pw_entry.substr(dash_pos + 1, first_space_pos));
		ppi.letter = raw_pw_entry[colon_pos - 1];
		ppi.password = raw_pw_entry.substr(colon_pos + 1);

		out.push_back(ppi);
	}

	return out;
}

int solve(const vector<password_policy_info> &in, bool part_two = false)
{
	int valid_passwords = 0;

	for (auto ppi : in)
	{
		if (part_two ? ppi.part_two_match() : ppi.part_one_match())
		{
			valid_passwords++;
		}
	}

	return valid_passwords;
}

int main()
{
	vector<string> input = split_istream_per_line(cin);
	vector<password_policy_info> policies = get_policies_from_input(input);

	cout << "Part 1: " << solve(policies, false) << endl;
	cout << "Part 2: " << solve(policies, true) << endl;
}
