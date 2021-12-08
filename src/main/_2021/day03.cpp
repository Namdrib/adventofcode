#include <bits/stdc++.h>
#include "../util/helpers.cpp"
using namespace std;

// https://adventofcode.com/2021/day/3

// return the most common value in bit `pos` of in all the elements of `in`
char most_common_bit(const vector<string> &in, size_t pos)
{
	map<char, size_t> char_count;

	for (auto s : in)
	{
		char_count[s[pos]]++;
	}

	return (char_count['1'] >= char_count['0']) ? '1' : '0';
}

int part_one(const vector<string> &in)
{
	// gamma is the most common digit in each bit position of in
	// epsilon is least common digit
	string gamma, epsilon;

	// for each position
	for (size_t i = 0; i < in[0].size(); i++)
	{
		if (most_common_bit(in, i) == '1')
		{
			gamma += "1";
			epsilon += "0";
		}
		else
		{
			gamma += "0";
			epsilon += "1";
		}
	}

	cout << "g: " << gamma << ", e: " << epsilon << endl;

	return binary_to_decimal(gamma) * binary_to_decimal(epsilon);
}

int part_two(const vector<string> &in)
{
	// calculate oxygen generator rating
	vector<string> oxygen_strings(in);

	for (size_t i = 0; i < in[0].size() && !oxygen_strings.empty(); i++)
	{
		char the_most_common_bit = most_common_bit(oxygen_strings, i);

		// only keep the ones where s[i] == the_most_common_bit
		oxygen_strings.erase(remove_if(oxygen_strings.begin(), oxygen_strings.end(),
					[the_most_common_bit, i]
					(string s)
					{return s[i] != the_most_common_bit;}
		), oxygen_strings.end());
	}
	string oxygen_generator_rating = oxygen_strings[0];


	// calculate co2 scrubber rating
	vector<string> co2_strings(in);

	for (size_t i = 0; i < in[0].size() && !co2_strings.empty(); i++)
	{
		char the_most_common_bit = most_common_bit(co2_strings, i);

		// only keep the ones where s[i] != the_most_common_bit
		co2_strings.erase(remove_if(co2_strings.begin(), co2_strings.end(),
					[the_most_common_bit, i]
					(string s)
					{return s[i] == the_most_common_bit;}
		), co2_strings.end());
	}
	string co2_scrubber_rating = co2_strings[0];

	return binary_to_decimal(oxygen_generator_rating) * binary_to_decimal(co2_scrubber_rating);
}

int main()
{
	vector<string> input = split_istream_per_line(cin);

	cout << "Part 1: " << part_one(input) << endl;
	cout << "Part 2: " << part_two(input) << endl;
}
