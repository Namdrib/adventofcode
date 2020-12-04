#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2020/day/4

vector<string> required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"};
vector<string> valid_eye_colours = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"};
class passport
{
	public:
		map<string, string> fields;

		// returns whether a passport is valid on part onw conditions
		// each field (except cid) must be present
		bool is_valid_part_one()
		{
			for (auto s : required_fields)
			{
				if (fields.count(s) <= 0)
				{
					return false;
				}
			}
			return true;
		}

		// returns whether a passport is valid on part two conditions
		// each field has certain restrictions
		bool is_valid_part_two()
		{
			if (!is_valid_part_one())
			{
				return false;
			}

			int byr = extract_nums_from<int>(fields["byr"])[0];
			if (byr < 1920 || byr > 2002)
			{
				return false;
			}

			int iyr = extract_nums_from<int>(fields["iyr"])[0];
			if (iyr < 2010 || iyr > 2020)
			{
				return false;
			}

			int eyr = extract_nums_from<int>(fields["eyr"])[0];
			if (eyr < 2020 || eyr > 2030)
			{
				return false;
			}

			const regex hgt_pattern("^(\\d)+(in|cm)");
			if (!regex_match(fields["hgt"], hgt_pattern))
			{
				return false;
			}

			string hgt_str = fields["hgt"];
			int hgt = extract_nums_from(hgt_str)[0];
			string hgt_unit = hgt_str.substr(hgt_str.size() - 2);

			if (hgt_unit == "cm")
			{
				if (hgt < 150 || hgt > 193)
				{
					return false;
				}
			}
			else if (hgt_unit == "in")
			{
				if (hgt < 59 || hgt > 76)
				{
					return false;
				}
			}
			else
			{
				return false;
			}

			const regex hex_colour("^#[0-9a-f]{6}$");
			if (!regex_match(fields["hcl"], hex_colour))
			{
				return false;
			}

			string ecl = fields["ecl"];
			if (all_of(all(valid_eye_colours), [ecl](const string &s){return ecl != s;}))
			{
				return false;
			}

			string pid = fields["pid"];
			string digits = "0123456789";
			if (pid.size() != 9 || all_of(all(digits), [pid](char c){return pid.find(c) != string::npos;}))
			{
				return false;
			}

			return true;
		}
};

// output a passport
ostream& operator << (ostream &os, const passport &p)
{
	for (auto field : p.fields)
	{
		os << "{" << field.first << ": " << field.second << "}, ";
	}
	os << endl;
	return os;
}

// parse inputs to extract passports from them based on new lines
vector<passport> make_passports_from_input(vector<string> &input)
{
	vector<passport> out;

	passport p;
	for (auto line : input)
	{
		vector<string> raw_fields = split_str_by_whitespace<string>(line);

		for (string s : raw_fields)
		{
			size_t colon_pos = s.find(':');

			string field = s.substr(0, colon_pos);
			string value = s.substr(colon_pos+1);

			p.fields[field] = value;
		}

		if (line == "")
		{
			out.push_back(p);
			p.fields.clear();
		}
	}

	out.push_back(p);

	return out;
}

size_t solve(vector<passport> &in, bool part_two = false)
{
	size_t out = 0;

	for (auto p : in)
	{
		if (part_two ? p.is_valid_part_two() : p.is_valid_part_one())
		{
			out++;
		}
	}

	return out;
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	vector<passport> passports = make_passports_from_input(input);

	cout << "Part 1: " << solve(passports, false) << endl;
	cout << "Part 2: " << solve(passports, true) << endl;
}

